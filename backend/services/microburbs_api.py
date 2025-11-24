"""
Microburbs API Service
Handles all external Microburbs API calls
"""
import requests
import logging
import sys
import os
from typing import Dict, Any, Optional

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import config

logger = logging.getLogger(__name__)


class MicroburbsApiService:
    """Service for calling Microburbs API endpoints"""
    
    def __init__(self):
        self.base_url = config.MICROBURBS_API_BASE_URL
        self.headers = config.get_api_headers()
        self.timeout = config.API_TIMEOUT
    
    def _make_request(self, endpoint: str, params: Optional[Dict[str, Any]] = None) -> Optional[Dict[str, Any]]:
        """
        Make HTTP request to Microburbs API
        
        Args:
            endpoint: API endpoint path (e.g. '/suburb/info')
            params: Query parameters dictionary
        
        Returns:
            JSON response data, or None if request fails
        """
        url = f"{self.base_url}{endpoint}"
        
        try:
            logger.info(f"Calling Microburbs API: {url} with params: {params}")
            response = requests.get(
                url,
                params=params,
                headers=self.headers,
                timeout=self.timeout
            )
            response.raise_for_status()
            data = response.json()
            logger.info(f"API call successful: {endpoint}")
            return data
        
        except requests.exceptions.Timeout:
            logger.error(f"API request timeout: {url}")
            return None
        
        except requests.exceptions.ConnectionError:
            logger.error(f"API connection failed: {url}")
            return None
        
        except requests.exceptions.HTTPError as e:
            logger.error(f"API HTTP error: {url}, status code: {e.response.status_code}")
            return None
        
        except requests.exceptions.RequestException as e:
            logger.error(f"API request exception: {url}, error: {str(e)}")
            return None
        
        except ValueError as e:
            logger.error(f"API response parsing failed: {url}, error: {str(e)}")
            return None
    
    def get_suburb_info(self, suburb: str, geojson: bool = True) -> Optional[Dict[str, Any]]:
        """
        Get suburb basic information

        Args:
            suburb: Suburb name (e.g. "Melbourne")
            geojson: Whether to include GeoJSON boundary data

        Returns:
            Suburb basic info dictionary
        """
        params = {'suburb': suburb}
        if geojson:
            params['geojson'] = 'true'
        return self._make_request('/suburb/info', params)
    
    def get_suburb_summary(self, suburb: str) -> Optional[Dict[str, Any]]:
        """
        Get suburb summary (including livability scores)
        
        Args:
            suburb: Suburb name
        
        Returns:
            Suburb summary dictionary
        """
        return self._make_request('/suburb/summary', {'suburb': suburb})
    
    def get_suburb_demographics(self, suburb: str) -> Optional[Dict[str, Any]]:
        """
        Get suburb demographics data

        Args:
            suburb: Suburb name

        Returns:
            Demographics data dictionary
        """
        return self._make_request('/suburb/demographics', {'suburb': suburb})

    def get_suburb_ethnicity(self, suburb: str) -> Optional[Dict[str, Any]]:
        """
        Get suburb ethnicity data

        Args:
            suburb: Suburb name

        Returns:
            Ethnicity data dictionary
        """
        return self._make_request('/suburb/ethnicity', {'suburb': suburb})

    def get_suburb_amenities(self, suburb: str) -> Optional[Dict[str, Any]]:
        """
        Get suburb amenities data (cafes, restaurants, parks, etc.)
        
        Args:
            suburb: Suburb name
        
        Returns:
            Amenities data dictionary
        """
        return self._make_request('/suburb/amenity', {'suburb': suburb})
    
    def get_suburb_market_data(self, suburb: str) -> Optional[Dict[str, Any]]:
        """
        Get suburb market data (prices, growth rates, etc.)
        
        Args:
            suburb: Suburb name
        
        Returns:
            Market data dictionary
        """
        return self._make_request('/suburb/market', {'suburb': suburb})
    
    def get_suburb_risk(self, suburb: str) -> Optional[Dict[str, Any]]:
        """
        Get suburb risk factors
        
        Args:
            suburb: Suburb name
        
        Returns:
            Risk factors dictionary
        """
        return self._make_request('/suburb/risk', {'suburb': suburb})
    
    def get_suburb_properties(self, suburb: str) -> Optional[Dict[str, Any]]:
        """
        Get property listings for a suburb
        
        Args:
            suburb: Suburb name
        
        Returns:
            Properties list dictionary
        """
        return self._make_request('/suburb/properties', {'suburb': suburb})
    
    def search_suburbs(self, query: str) -> Optional[Dict[str, Any]]:
        """
        Search for suburbs by name
        
        Args:
            query: Search query string
        
        Returns:
            Search results dictionary
        """
        return self._make_request('/suburb/suburbs', {'suburb': query})
    
    def get_suburb_development(self, suburb: str) -> Optional[Dict[str, Any]]:
        """
        Get development applications for a suburb
        
        Args:
            suburb: Suburb name
        
        Returns:
            Development applications dictionary
        """
        return self._make_request('/suburb/development', {'suburb': suburb})
    
    def get_suburb_market_insights(self, suburb: str, metric: str = None, property_type: str = None) -> Optional[Dict[str, Any]]:
        """
        Get market insights with optional filters
        
        Args:
            suburb: Suburb name
            metric: Optional metric filter (e.g. 'median_price')
            property_type: Optional property type filter (e.g. 'house')
        
        Returns:
            Market insights dictionary
        """
        params = {'suburb': suburb}
        if metric:
            params['metric'] = metric
        if property_type:
            params['property_type'] = property_type
        return self._make_request('/suburb/market', params)
    
    def get_suburb_pocket_insights(self, suburb: str, geojson: bool = True, property_type: str = None) -> Optional[Dict[str, Any]]:
        """
        Get pocket-level market insights
        
        Args:
            suburb: Suburb name
            geojson: Whether to include GeoJSON data
            property_type: Optional property type filter
        
        Returns:
            Pocket insights dictionary
        """
        params = {
            'suburb': suburb,
            'geojson': 'true' if geojson else 'false'
        }
        if property_type:
            params['property_type'] = property_type
        return self._make_request('/suburb/pocket', params)
    
    def get_suburb_street_insights(self, suburb: str, property_type: str = None) -> Optional[Dict[str, Any]]:
        """
        Get street-level market insights
        
        Note: This endpoint does not support geojson parameter
        
        Args:
            suburb: Suburb name
            property_type: Optional property type filter
        
        Returns:
            Street insights dictionary
        """
        params = {'suburb': suburb}
        if property_type:
            params['property_type'] = property_type
        return self._make_request('/suburb/streets', params)
    
    def get_suburb_schools(self, suburb: str, geojson: bool = True) -> Optional[Dict[str, Any]]:
        """
        Get schools in a suburb
        
        Args:
            suburb: Suburb name
            geojson: Whether to include GeoJSON data
        
        Returns:
            Schools dictionary
        """
        params = {
            'suburb': suburb,
            'geojson': 'true' if geojson else 'false'
        }
        return self._make_request('/suburb/schools', params)
    
    def get_suburb_catchments(self, suburb: str, geojson: bool = True) -> Optional[Dict[str, Any]]:
        """
        Get school catchment areas for a suburb
        
        Args:
            suburb: Suburb name
            geojson: Whether to include GeoJSON data
        
        Returns:
            Catchment areas dictionary
        """
        params = {
            'suburb': suburb,
            'geojson': 'true' if geojson else 'false'
        }
        return self._make_request('/suburb/catchments', params)
    
    def get_suburb_zoning(self, suburb: str, geojson: bool = True) -> Optional[Dict[str, Any]]:
        """
        Get zoning information for a suburb
        
        Args:
            suburb: Suburb name
            geojson: Whether to include GeoJSON data
        
        Returns:
            Zoning information dictionary
        """
        params = {
            'suburb': suburb,
            'geojson': 'true' if geojson else 'false'
        }
        return self._make_request('/suburb/zoning', params)
    
    def get_similar_suburbs(self, suburb: str, geojson: bool = True) -> Optional[Dict[str, Any]]:
        """
        Get similar suburbs to the specified suburb
        
        Args:
            suburb: Suburb name
            geojson: Whether to include GeoJSON data
        
        Returns:
            Similar suburbs dictionary
        """
        params = {
            'suburb': suburb,
            'geojson': 'true' if geojson else 'false'
        }
        return self._make_request('/suburb/similar', params)
