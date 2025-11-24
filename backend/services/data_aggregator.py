"""
Data Aggregator Service
Aggregates multiple API calls, transforms data formats, and provides fallback mechanisms
"""
import json
import logging
import sys
import os
from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from repositories.composite_repository import CompositeSuburbRepository
from config import config

logger = logging.getLogger(__name__)


class DataAggregatorService:
    """Service for data aggregation and transformation"""

    def __init__(self, repository=None):
        """
        Initialize data aggregator service

        Args:
            repository: Optional SuburbRepository instance for dependency injection
        """
        # Use Repository pattern instead of direct API service
        self.repo = repository or CompositeSuburbRepository()
        self.use_mock_data = config.USE_MOCK_DATA

    def search_suburbs(self, query: str) -> List[Dict[str, Any]]:
        """
        Search for suburbs

        Args:
            query: Search keyword

        Returns:
            List of suburbs
        """
        results = self.repo.search_suburbs(query)
        if not results:
            return []
        
        # Convert API format to frontend format
        return self._convert_suburb_search_results(results)

    def _convert_suburb_search_results(self, results: List[Dict]) -> List[Dict[str, Any]]:
        """
        Convert API search results to frontend format

        Args:
            results: API search results (from real Microburbs API)

        Returns:
            Converted suburb list matching fallback format
        """
        converted = []
        for item in results:
            # Real API format: area_name, information.poa, information.state
            area_name = item.get('area_name', '')
            information = item.get('information', {})
            postcode = information.get('poa', '')
            state = information.get('state', '')

            # Create suburb_id in format: name-postcode (lowercase, hyphenated)
            name_parts = area_name.replace(' (', '-').replace(')', '').split()
            suburb_name = ' '.join([p for p in name_parts if not p.isupper() or len(p) <= 3])
            suburb_id = f"{suburb_name.lower().replace(' ', '-')}-{postcode}"

            converted.append({
                'id': suburb_id,
                'name': suburb_name,
                'state': state,
                'postcode': postcode,
                'population': 0,  # Not available in search results
                'medianAge': 0,  # Not available in search results
                'medianHousePrice': 0,  # Not available in search results
                'medianRent': 0,  # Not available in search results
                'amenitiesCount': 0,  # Not available in search results
                'schoolsCount': 0,  # Not available in search results
                'developmentApps': 0  # Not available in search results
            })
        return converted

    def get_suburb_details(self, suburb_id: str) -> Optional[Dict[str, Any]]:
        """
        Get detailed suburb information

        Args:
            suburb_id: Suburb ID

        Returns:
            Suburb details dictionary
        """
        # Repository handles API/fallback automatically
        info_data = self.repo.get_suburb_info(suburb_id)
        summary_data = self.repo.get_suburb_summary(suburb_id)
        market_data = self.repo.get_market_trends(suburb_id)

        # If all fail, return None
        if not info_data and not summary_data and not market_data:
            return None

        # Aggregate multiple API responses
        return self._aggregate_suburb_data(suburb_id, info_data, summary_data, market_data)

    def _aggregate_suburb_data(
        self,
        suburb_id: str,
        info_data: Optional[Dict],
        summary_data: Optional[Dict],
        market_data: Optional[Dict]
    ) -> Dict[str, Any]:
        """
        Aggregate suburb data from multiple API responses

        Args:
            suburb_id: Suburb ID
            info_data: Basic info data
            summary_data: Summary data
            market_data: Market data

        Returns:
            Aggregated suburb data
        """
        # Extract suburb name from ID
        parts = suburb_id.split('-')
        if len(parts) > 1 and parts[-1].isdigit():
            parts = parts[:-1]
        suburb_name = ' '.join(parts).title()

        result = {
            'id': suburb_id,
            'name': suburb_name,
            'state': '',
            'postcode': '',
            'medianHousePrice': 0,
            'medianRent': 0,
            'population': 0,
            'medianAge': 0,
            'schoolsCount': 0,
            'amenitiesCount': 0,
            'developmentApps': 0
        }

        # Merge info data - API returns {'information': {...}}
        if info_data and 'information' in info_data:
            info = info_data['information']
            geo_div = info.get('geo_divisions', {})
            result['state'] = geo_div.get('state', '')
            result['postcode'] = geo_div.get('poa', '')

        # Merge summary data - API returns {'results': [...]}
        if summary_data and 'results' in summary_data:
            summary_results = summary_data['results']
            if isinstance(summary_results, list):
                for item in summary_results:
                    if isinstance(item, dict):
                        # Extract relevant summary information
                        pass

        # Merge market data - API returns {'results': [[...]]} (nested list)
        if market_data and 'results' in market_data:
            market_results = market_data['results']
            if isinstance(market_results, list) and len(market_results) > 0:
                # First level is a list
                if isinstance(market_results[0], list) and len(market_results[0]) > 0:
                    # Second level contains actual data
                    for item in market_results[0]:
                        if isinstance(item, dict):
                            if item.get('metric') == 'sell_price':
                                result['medianHousePrice'] = int(item.get('value', 0))
                            elif item.get('metric') == 'rent_price':
                                result['medianRent'] = int(item.get('value', 0))

        return result

    def _transform_demographics_data(self, suburb_id: str, raw_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Transform raw API demographics data to frontend format
        
        Args:
            suburb_id: Suburb ID
            raw_data: Raw API data (may contain age_brackets, ethnicities, etc.)
            
        Returns:
            Transformed data in frontend format
        """
        if not raw_data:
            return {}
            
        transformed = {
            'ageDistribution': [],
            'ethnicity': []
        }
        
        # Transform age_brackets to ageDistribution
        if 'age_brackets' in raw_data:
            # Group by age range (persons only, ignore gender breakdown)
            age_groups = {}
            for bracket in raw_data['age_brackets']:
                if bracket.get('gender') == 'persons':
                    age = bracket.get('age', '')
                    proportion = bracket.get('proportion', 0)
                    age_groups[age] = {
                        'age': age,
                        'population': 0,  # Not available from API
                        'percentage': round(proportion * 100, 1)
                    }
            transformed['ageDistribution'] = list(age_groups.values())
        
        # Transform ethnicities to ethnicity
        if 'ethnicities' in raw_data:
            for eth in raw_data['ethnicities'][:10]:  # Top 10
                transformed['ethnicity'].append({
                    'name': eth.get('ethnicity', eth.get('name', '')),
                    'percentage': round(eth.get('proportion', eth.get('percentage', 0)) * 100, 1)
                })
        # Handle new API format with results array
        elif 'results' in raw_data:
            # Aggregate ethnicity data from all SA1 areas
            ethnicity_totals = {}
            count = 0

            for result in raw_data['results']:
                if 'ethnicity' in result and isinstance(result['ethnicity'], dict):
                    count += 1
                    for eth_name, proportion in result['ethnicity'].items():
                        if eth_name not in ethnicity_totals:
                            ethnicity_totals[eth_name] = 0
                        ethnicity_totals[eth_name] += proportion

            # Calculate averages and sort by percentage
            if count > 0:
                ethnicity_list = []
                for eth_name, total in ethnicity_totals.items():
                    avg_proportion = total / count
                    ethnicity_list.append({
                        'name': eth_name,
                        'percentage': round(avg_proportion * 100, 1)
                    })

                # Sort by percentage descending and take top 10
                ethnicity_list.sort(key=lambda x: x['percentage'], reverse=True)
                transformed['ethnicity'] = ethnicity_list[:10]
        
        return transformed

    def get_demographics(self, suburb_id: str) -> Optional[Dict[str, Any]]:
        """
        Get demographics data for a suburb

        Args:
            suburb_id: Suburb ID

        Returns:
            Demographics data dictionary
        """
        data = self.repo.get_demographics(suburb_id)
        if not data or suburb_id not in data:
            return data

        raw_data = data[suburb_id]

        # If data is already in frontend format, return as is
        if 'ageDistribution' in raw_data:
            return data

        # Transform API format to frontend format
        transformed = self._transform_demographics_data(suburb_id, raw_data)
        return {suburb_id: transformed}

    def _transform_amenities_data(self, suburb_id: str, raw_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Transform raw API amenities data to frontend format
        
        Args:
            suburb_id: Suburb ID
            raw_data: Raw API data (may contain results array)
            
        Returns:
            Transformed data in frontend format
        """
        if not raw_data:
            return {'categories': [], 'total': 0}
        
        # If API format with 'results' array
        if 'results' in raw_data:
            results = raw_data['results']
            # Count by category
            category_counts = {}
            for item in results:
                category = item.get('category', 'Other')
                category_counts[category] = category_counts.get(category, 0) + 1
            
            total = len(results)
            categories = [
                {
                    'name': cat,
                    'count': count,
                    'percentage': round((count / total * 100) if total > 0 else 0, 1)
                }
                for cat, count in sorted(category_counts.items(), key=lambda x: x[1], reverse=True)
            ]
            
            return {
                'categories': categories,
                'total': total
            }
        
        # Already in correct format
        return raw_data

    def get_amenities(self, suburb_id: str) -> Optional[Dict[str, Any]]:
        """
        Get amenities data for a suburb

        Args:
            suburb_id: Suburb ID

        Returns:
            Amenities data dictionary
        """
        data = self.repo.get_amenities(suburb_id)
        if not data or suburb_id not in data:
            return data
        
        raw_data = data[suburb_id]
        
        # If data is already in frontend format, return as is
        if 'categories' in raw_data and isinstance(raw_data['categories'], list):
            if not raw_data['categories'] or 'name' in raw_data['categories'][0]:
                return data
        
        # Transform API format to frontend format
        transformed = self._transform_amenities_data(suburb_id, raw_data)
        return {suburb_id: transformed}

    def _extract_price_series(self, results: List[Dict]) -> List[Dict]:
        """
        Extract time series data from API results
        
        Args:
            results: Raw API results array
            
        Returns:
            List of {date, suburb, cr, sa3} dictionaries
        """
        # Group data by date
        price_by_date = {}
        
        for item in results:
            if not isinstance(item, dict):
                continue
            
            # Only process sell_price for house type
            if item.get('metric') != 'sell_price' or item.get('property_type') != 'house':
                continue
            
            date = item.get('date', '')
            if not date:
                continue
            
            suburb_price = float(item.get('value', 0))
            cr_price = float(item.get('cr', {}).get('value', 0))
            sa3_price = float(item.get('sa3', {}).get('value', 0))
            
            if date not in price_by_date:
                price_by_date[date] = {
                    'date': date,
                    'suburb': suburb_price,
                    'cr': cr_price,
                    'sa3': sa3_price
                }
        
        # Sort by date and return as list
        sorted_data = sorted(price_by_date.values(), key=lambda x: x['date'])
        return sorted_data
    
    
    def _calculate_current_metrics(self, series: List[Dict]) -> Dict:
        """
        Calculate current price and growth metrics
        
        Args:
            series: Time series data
            
        Returns:
            Dictionary with price and growth metrics
        """
        if not series:
            return {'price': 0, 'growth_1y': 0, 'growth_5y': 0, 'growth_total': 0}
        
        current_price = series[-1]['suburb']
        
        # Find prices from 1 year ago and 5 years ago
        from datetime import datetime, timedelta
        current_date = datetime.strptime(series[-1]['date'], '%Y-%m-%d')
        one_year_ago = current_date - timedelta(days=365)
        five_years_ago = current_date - timedelta(days=365*5)
        
        price_1y_ago = current_price
        price_5y_ago = current_price
        
        for data_point in series:
            point_date = datetime.strptime(data_point['date'], '%Y-%m-%d')
            if point_date >= one_year_ago and data_point['suburb'] > 0:
                price_1y_ago = data_point['suburb']
                break
        
        for data_point in series:
            point_date = datetime.strptime(data_point['date'], '%Y-%m-%d')
            if point_date >= five_years_ago and data_point['suburb'] > 0:
                price_5y_ago = data_point['suburb']
                break
        
        price_earliest = series[0]['suburb'] if series[0]['suburb'] > 0 else current_price
        
        # Calculate growth percentages
        growth_1y = ((current_price - price_1y_ago) / price_1y_ago * 100) if price_1y_ago > 0 else 0
        growth_5y = ((current_price - price_5y_ago) / price_5y_ago * 100) if price_5y_ago > 0 else 0
        growth_total = ((current_price - price_earliest) / price_earliest * 100) if price_earliest > 0 else 0
        
        return {
            'price': int(current_price),
            'growth_1y': round(growth_1y, 2),
            'growth_5y': round(growth_5y, 2),
            'growth_total': round(growth_total, 2)
        }
    
    def _calculate_regional_comparison(self, series: List[Dict]) -> Dict:
        """
        Calculate regional price comparison
        
        Args:
            series: Time series data
            
        Returns:
            Dictionary with cr and sa3 comparison data
        """
        if not series:
            return {
                'cr': {'price': 0, 'difference': 0, 'status': 'below'},
                'sa3': {'price': 0, 'difference': 0, 'status': 'below'}
            }
        
        latest = series[-1]
        suburb_price = latest['suburb']
        cr_price = latest['cr']
        sa3_price = latest['sa3']
        
        cr_diff = ((suburb_price - cr_price) / cr_price * 100) if cr_price > 0 else 0
        sa3_diff = ((suburb_price - sa3_price) / sa3_price * 100) if sa3_price > 0 else 0
        
        return {
            'cr': {
                'price': int(cr_price),
                'difference': round(cr_diff, 1),
                'status': 'below' if cr_diff < 0 else 'above'
            },
            'sa3': {
                'price': int(sa3_price),
                'difference': round(sa3_diff, 1),
                'status': 'below' if sa3_diff < 0 else 'above'
            }
        }
    
    def _calculate_volatility(self, prices: List[float]) -> float:
        """
        Calculate price volatility (coefficient of variation)
        
        Args:
            prices: List of price values
            
        Returns:
            Volatility coefficient
        """
        if not prices or len(prices) < 2:
            return 0.0
        
        import statistics
        mean = statistics.mean(prices)
        if mean == 0:
            return 0.0
        
        stdev = statistics.stdev(prices)
        return stdev / mean
    
    def _detect_trend(self, recent_series: List[Dict]) -> str:
        """
        Detect price trend from recent data
        
        Args:
            recent_series: Recent time series data (last 6 months)
            
        Returns:
            'rising', 'stable', or 'declining'
        """
        if not recent_series or len(recent_series) < 2:
            return 'stable'
        
        prices = [p['suburb'] for p in recent_series if p['suburb'] > 0]
        if len(prices) < 2:
            return 'stable'
        
        # Calculate trend using first and last price
        first_price = prices[0]
        last_price = prices[-1]
        change_pct = ((last_price - first_price) / first_price * 100) if first_price > 0 else 0
        
        if change_pct > 2:
            return 'rising'
        elif change_pct < -2:
            return 'declining'
        else:
            return 'stable'
    
    def _calculate_investment_score(self, series: List[Dict], comparison: Dict) -> Dict:
        """
        Calculate investment analysis score and insights
        
        Args:
            series: Time series data
            comparison: Regional comparison data
            
        Returns:
            Dictionary with score, volatility, trend, and insights
        """
        if not series:
            return {
                'score': 0,
                'volatility': 'low',
                'trend': 'stable',
                'insights': []
            }
        
        prices = [p['suburb'] for p in series if p['suburb'] > 0]
        volatility = self._calculate_volatility(prices)
        
        # Detect trend from last 6 data points
        recent_data = series[-6:] if len(series) >= 6 else series
        trend = self._detect_trend(recent_data)
        
        # Calculate investment score
        # Growth potential (40%): based on price appreciation
        growth_ratio = series[-1]['suburb'] / series[0]['suburb'] if series[0]['suburb'] > 0 else 1
        growth_score = min(growth_ratio, 3) * 3.33  # Cap at 3x = 10 points
        
        # Value score (30%): based on regional comparison
        cr_diff = comparison['cr']['difference']
        if cr_diff < -10:
            value_score = 10
        elif cr_diff < -5:
            value_score = 8
        elif cr_diff < 0:
            value_score = 6
        else:
            value_score = 4
        
        # Stability score (30%): based on volatility
        if volatility < 0.1:
            stability_score = 10
        elif volatility < 0.15:
            stability_score = 7
        else:
            stability_score = 5
        
        total_score = growth_score * 0.4 + value_score * 0.3 + stability_score * 0.3
        
        # Generate insights
        insights = []
        if cr_diff < -10:
            insights.append(f"Excellent value - {abs(cr_diff):.1f}% below regional average")
        elif cr_diff < -5:
            insights.append(f"Good value - {abs(cr_diff):.1f}% below regional average")
        
        if trend == 'rising':
            insights.append("Positive price momentum in recent months")
        elif trend == 'declining':
            insights.append("Price declining in recent months")
        
        if volatility < 0.1:
            insights.append("Stable market with low volatility")
        elif volatility > 0.2:
            insights.append("High price volatility - higher risk")
        
        if growth_ratio > 2:
            insights.append(f"Strong long-term growth of {(growth_ratio-1)*100:.0f}%")
        
        return {
            'score': round(total_score, 1),
            'volatility': 'low' if volatility < 0.15 else ('medium' if volatility < 0.25 else 'high'),
            'trend': trend,
            'insights': insights
        }
    
    def _transform_market_trends_data(self, suburb_id: str, raw_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Transform raw API market trends data to frontend format
        
        Args:
            suburb_id: Suburb ID
            raw_data: Raw API data (may contain results array)
            
        Returns:
            Transformed data in frontend format
        """
        if not raw_data or 'results' not in raw_data:
            return {
                'priceHistory': [],
                'currentPrice': 0,
                'priceGrowth': {'1year': 0, '5year': 0, 'total': 0},
                'regionalComparison': {
                    'cr': {'price': 0, 'difference': 0, 'status': 'below'},
                    'sa3': {'price': 0, 'difference': 0, 'status': 'below'}
                },
                'investmentScore': 0,
                'analytics': {
                    'volatility': 'low',
                    'trend': 'stable',
                    'insights': []
                }
            }
        
        results = raw_data['results']
        if isinstance(results, list) and len(results) > 0 and isinstance(results[0], list):
            results = results[0]
        
        # Extract time series data (suburb, cr, sa3 prices over time)
        price_history = self._extract_price_series(results)
        
        if not price_history:
            # Fallback to old simple format
            return {
                'priceHistory': [],
                'rentHistory': [],
                'currentPrice': 0,
                'priceGrowth': {'1year': 0, '5year': 0, 'total': 0},
                'regionalComparison': {
                    'cr': {'price': 0, 'difference': 0, 'status': 'below'},
                    'sa3': {'price': 0, 'difference': 0, 'status': 'below'}
                },
                'investmentScore': 0,
                'analytics': {
                    'volatility': 'low',
                    'trend': 'stable',
                    'insights': []
                }
            }
        
        # Calculate current metrics
        current_data = self._calculate_current_metrics(price_history)
        
        # Calculate regional comparison
        regional_comparison = self._calculate_regional_comparison(price_history)

        # Calculate investment analysis
        investment_analysis = self._calculate_investment_score(price_history, regional_comparison)

        # TODO: Extract rent history from API data when available
        rent_history = []

        return {
            'priceHistory': price_history,
            'rentHistory': rent_history,  # Add rent history
            'currentPrice': current_data['price'],
            'priceGrowth': {
                '1year': current_data['growth_1y'],
                '5year': current_data['growth_5y'],
                'total': current_data['growth_total']
            },
            'regionalComparison': regional_comparison,
            'investmentScore': investment_analysis['score'],
            'analytics': {
                'volatility': investment_analysis['volatility'],
                'trend': investment_analysis['trend'],
                'insights': investment_analysis['insights']
            }
        }

    def get_market_trends(self, suburb_id: str) -> Optional[Dict[str, Any]]:
        """
        Get market trends data for a suburb

        Args:
            suburb_id: Suburb ID

        Returns:
            Market trends data dictionary
        """
        data = self.repo.get_market_trends(suburb_id)
        if not data or suburb_id not in data:
            return data
        
        raw_data = data[suburb_id]
        
        # If data is already in frontend format, return as is
        if 'priceHistory' in raw_data:
            return data
        
        # Transform API format to frontend format
        transformed = self._transform_market_trends_data(suburb_id, raw_data)
        return {suburb_id: transformed}

    def _transform_schools_data(self, suburb_id: str, raw_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Transform raw API schools data to frontend format
        
        Args:
            suburb_id: Suburb ID
            raw_data: Raw API data (may contain results array)
            
        Returns:
            Transformed data in frontend format
        """
        if not raw_data:
            return {'schools': [], 'total': 0}
        
        # If API format with 'results' array
        if 'results' in raw_data:
            results = raw_data['results']
            schools = []
            for item in results:
                if not isinstance(item, dict):
                    continue
                
                school = {
                    'name': item.get('name', ''),
                    'type': item.get('school_level_type', 'Unknown'),
                    'sector': item.get('school_sector_type', 'Unknown'),
                }
                
                # Add optional fields if available
                if 'naplan' in item:
                    school['naplanScore'] = item.get('naplan')
                    school['rating'] = round(item.get('naplan', 0) * 5, 1)  # Convert 0-1 to 0-5
                if 'naplan_rank' in item:
                    school['naplanRank'] = item.get('naplan_rank')
                if 'socioeconomic' in item:
                    school['socioeconomicScore'] = item.get('socioeconomic')
                if 'socioeconomic_rank' in item:
                    school['socioeconomicRank'] = item.get('socioeconomic_rank')
                if 'attendance_rate' in item:
                    school['attendanceRate'] = item.get('attendance_rate')
                
                # Add student count if available
                boys = item.get('boys', 0)
                girls = item.get('girls', 0)
                if boys or girls:
                    school['students'] = {
                        'boys': boys,
                        'girls': girls,
                        'total': boys + girls
                    }
                
                schools.append(school)
            
            return {
                'schools': schools,
                'total': len(schools)
            }
        
        # Already in correct format
        return raw_data

    def get_schools(self, suburb_id: str) -> Optional[Dict[str, Any]]:
        """
        Get schools data for a suburb

        Args:
            suburb_id: Suburb ID

        Returns:
            Schools data dictionary
        """
        data = self.repo.get_schools(suburb_id)
        if not data or suburb_id not in data:
            return data
        
        raw_data = data[suburb_id]
        
        # If data is already in frontend format, return as is
        if 'schools' in raw_data and isinstance(raw_data['schools'], list):
            if not raw_data['schools'] or 'name' in raw_data['schools'][0]:
                return data
        
        # Transform API format to frontend format
        transformed = self._transform_schools_data(suburb_id, raw_data)
        return {suburb_id: transformed}

    def _transform_developments_data(self, suburb_id: str, raw_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Transform raw API developments data to frontend format
        
        Args:
            suburb_id: Suburb ID
            raw_data: Raw API data (may contain results array)
            
        Returns:
            Transformed data in frontend format
        """
        if not raw_data:
            return {'developments': [], 'total': 0, 'showing': 0}
        
        # If API format with 'results' array
        if 'results' in raw_data:
            results = raw_data['results']
            developments = []
            for idx, item in enumerate(results[:50]):  # Limit to 50
                if not isinstance(item, dict):
                    continue

                development = {
                    'id': item.get('id', f'dev-{idx}'),
                    'name': item.get('description', item.get('name', 'Development Application')),
                    'type': item.get('category', item.get('development_type', 'Residential')),
                    'status': item.get('status', 'Unknown'),
                    'units': item.get('units', 0),
                    'address': item.get('area_name', item.get('address', '')),
                    'applicant': item.get('applicant', 'Unknown'),
                    'submittedDate': item.get('date', item.get('lodgement_date', item.get('submitted_date', '')))
                }
                developments.append(development)
            
            return {
                'developments': developments,
                'total': len(results),
                'showing': len(developments)
            }
        
        # Already in correct format
        return raw_data

    def get_developments(self, suburb_id: str) -> Optional[Dict[str, Any]]:
        """
        Get development applications for a suburb

        Args:
            suburb_id: Suburb ID

        Returns:
            Development applications dictionary
        """
        data = self.repo.get_developments(suburb_id)
        if not data or suburb_id not in data:
            return data
        
        raw_data = data[suburb_id]
        
        # If data is already in frontend format, return as is
        if 'developments' in raw_data and isinstance(raw_data['developments'], list):
            if not raw_data['developments'] or 'id' in raw_data['developments'][0]:
                return data
        
        # Transform API format to frontend format
        transformed = self._transform_developments_data(suburb_id, raw_data)
        return {suburb_id: transformed}

    # Additional endpoints for advanced API features

    def get_market_insights(self, suburb_id: str, metric: str = None, property_type: str = None) -> Optional[Dict[str, Any]]:
        """
        Get market insights with optional filters

        Args:
            suburb_id: Suburb ID
            metric: Optional metric filter
            property_type: Optional property type filter

        Returns:
            Market insights dictionary
        """
        return self.repo.get_market_insights(suburb_id, metric, property_type)

    def get_pocket_insights(self, suburb_id: str, geojson: bool = True, property_type: str = None) -> Optional[Dict[str, Any]]:
        """
        Get pocket-level market insights

        Args:
            suburb_id: Suburb ID
            geojson: Whether to include GeoJSON data
            property_type: Optional property type filter

        Returns:
            Pocket insights dictionary
        """
        return self.repo.get_pocket_insights(suburb_id, geojson, property_type)

    def get_street_insights(self, suburb_id: str, geojson: bool = True, property_type: str = None) -> Optional[Dict[str, Any]]:
        """
        Get street-level market insights

        Args:
            suburb_id: Suburb ID
            geojson: Whether to include GeoJSON data (not supported by this endpoint)
            property_type: Optional property type filter

        Returns:
            Street insights dictionary
        """
        return self.repo.get_street_insights(suburb_id, geojson, property_type)

    def get_street_rankings(self, suburb_id: str, property_type: str = None) -> Optional[Dict[str, Any]]:
        """
        Get street rankings for a suburb

        Note: This is a stub implementation. Returns street insights data.
        TODO: Implement proper street rankings aggregation and sorting

        Args:
            suburb_id: Suburb ID
            property_type: Optional property type filter

        Returns:
            Street rankings data (currently returns street insights)
        """
        # For now, return street insights data
        # The frontend expects an array of street data
        insights = self.get_street_insights(suburb_id, False, property_type)

        if not insights or suburb_id not in insights:
            return []

        # Extract and flatten the results
        raw_data = insights.get(suburb_id, {})

        # Handle nested results structure from API: { "results": [[...]] }
        if isinstance(raw_data, dict) and 'results' in raw_data:
            results = raw_data['results']
            # Flatten nested arrays
            if isinstance(results, list) and len(results) > 0:
                if isinstance(results[0], list):
                    # Flatten [[...]] to [...]
                    return results[0] if len(results[0]) > 0 else []
                return results
            return []

        # If it's already an array, return as is
        if isinstance(raw_data, list):
            return raw_data

        return []

    def get_risk_factors(self, suburb_id: str, geojson: bool = True) -> Optional[Dict[str, Any]]:
        """
        Get risk factors for a suburb

        Args:
            suburb_id: Suburb ID
            geojson: Whether to include GeoJSON data

        Returns:
            Risk factors dictionary
        """
        return self.repo.get_risk_factors(suburb_id, geojson)

    def get_suburb_info(self, suburb_id: str, geojson: bool = True) -> Optional[Dict[str, Any]]:
        """
        Get suburb basic geographical information

        Args:
            suburb_id: Suburb ID
            geojson: Whether to include GeoJSON data

        Returns:
            Suburb info dictionary
        """
        return self.repo.get_suburb_info(suburb_id, geojson)

    def get_suburb_summary(self, suburb_id: str) -> Optional[Dict[str, Any]]:
        """
        Get AI-generated suburb summary and scores

        Args:
            suburb_id: Suburb ID

        Returns:
            Suburb summary dictionary wrapped in suburb_id key
        """
        data = self.repo.get_suburb_summary(suburb_id)
        if not data:
            return None
        
        # If data is already wrapped in suburb_id, return as is
        if suburb_id in data:
            return data
        
        # Wrap the data in suburb_id key for consistent frontend format
        return {suburb_id: data}

    def get_school_catchments(self, suburb_id: str, geojson: bool = True) -> Optional[Dict[str, Any]]:
        """
        Get school catchment areas for a suburb

        Args:
            suburb_id: Suburb ID
            geojson: Whether to include GeoJSON data

        Returns:
            Catchment areas dictionary
        """
        return self.repo.get_school_catchments(suburb_id, geojson)

    def get_zoning(self, suburb_id: str, geojson: bool = True) -> Optional[Dict[str, Any]]:
        """
        Get zoning information for a suburb

        Args:
            suburb_id: Suburb ID
            geojson: Whether to include GeoJSON data

        Returns:
            Zoning information dictionary
        """
        return self.repo.get_zoning(suburb_id, geojson)

    def get_similar_suburbs(self, suburb_id: str, geojson: bool = True) -> Optional[Dict[str, Any]]:
        """
        Get similar suburbs to the specified suburb

        Args:
            suburb_id: Suburb ID
            geojson: Whether to include GeoJSON data

        Returns:
            Similar suburbs dictionary
        """
        return self.repo.get_similar_suburbs(suburb_id, geojson)
