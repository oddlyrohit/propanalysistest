"""
File Repository Implementation
Fetches data from local JSON files (fallback mechanism)
"""
import json
import logging
from typing import List, Optional, Dict, Any
from .base import SuburbRepository
from config import config

logger = logging.getLogger(__name__)


class FileSuburbRepository(SuburbRepository):
    """Repository that fetches data from local JSON files"""

    def __init__(self):
        """Initialize file repository"""
        self.data_dir = config.DATA_DIR

    def _load_file(self, filename: str) -> Optional[Dict[str, Any]]:
        """
        Load data from JSON file

        Args:
            filename: JSON filename

        Returns:
            Parsed JSON data or None
        """
        try:
            file_path = config.get_data_path(filename)
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                logger.debug(f"Loaded data from file: {filename}")
                return data
        except FileNotFoundError:
            logger.debug(f"File not found: {filename}")
            return None
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse JSON from {filename}: {str(e)}")
            return None
        except Exception as e:
            logger.error(f"Failed to load file {filename}: {str(e)}")
            return None

    def search_suburbs(self, query: str) -> List[Dict[str, Any]]:
        """Search for suburbs in local data"""
        data = self._load_file('suburbs.json')
        if not data:
            return []

        suburbs = data.get('suburbs', [])
        if query:
            query_lower = query.lower()
            suburbs = [
                s for s in suburbs
                if query_lower in s.get('name', '').lower()
            ]

        return suburbs[:10]

    def get_suburb_info(self, suburb_id: str, geojson: bool = True) -> Optional[Dict[str, Any]]:
        """Get basic suburb information from file"""
        data = self._load_file('suburb_info.json')
        if data:
            return data.get(suburb_id)
        return None

    def get_suburb_summary(self, suburb_id: str) -> Optional[Dict[str, Any]]:
        """Get suburb summary from file"""
        data = self._load_file('suburb_summary.json')
        if data:
            return data.get(suburb_id)
        return None

    def get_demographics(self, suburb_id: str) -> Optional[Dict[str, Any]]:
        """Get demographics data from file"""
        data = self._load_file('demographics.json')
        if data and suburb_id in data:
            return {suburb_id: data[suburb_id]}
        
        # If suburb_id not found, use first available suburb's data
        if data:
            first_key = next(iter(data.keys()))
            logger.info(f"Using fallback data from {first_key} for {suburb_id}")
            return {suburb_id: data[first_key]}
        
        # Return empty structure
        return {suburb_id: {'ageDistribution': [], 'ethnicity': []}}

    def get_amenities(self, suburb_id: str) -> Optional[Dict[str, Any]]:
        """Get amenities data from file"""
        data = self._load_file('amenities.json')
        if data and suburb_id in data:
            return {suburb_id: data[suburb_id]}
        
        # If suburb_id not found, use first available suburb's data
        if data:
            first_key = next(iter(data.keys()))
            logger.info(f"Using fallback data from {first_key} for {suburb_id}")
            return {suburb_id: data[first_key]}
        
        # Return empty structure
        return {suburb_id: {'categories': [], 'total': 0}}

    def get_market_trends(self, suburb_id: str) -> Optional[Dict[str, Any]]:
        """Get market trends from file"""
        data = self._load_file('market_trends.json')
        if data and suburb_id in data:
            return {suburb_id: data[suburb_id]}
        
        # If suburb_id not found, use first available suburb's data
        if data:
            first_key = next(iter(data.keys()))
            logger.info(f"Using fallback data from {first_key} for {suburb_id}")
            return {suburb_id: data[first_key]}
        
        # Return empty structure
        return {suburb_id: {
            'priceHistory': [],
            'quarterlyGrowth': 0,
            'rentalYield': 0,
            'daysOnMarket': 0
        }}

    def get_schools(self, suburb_id: str) -> Optional[Dict[str, Any]]:
        """Get schools data from file"""
        data = self._load_file('schools.json')
        if data and suburb_id in data:
            return {suburb_id: data[suburb_id]}
        
        # If suburb_id not found, use first available suburb's data
        if data:
            first_key = next(iter(data.keys()))
            logger.info(f"Using fallback data from {first_key} for {suburb_id}")
            return {suburb_id: data[first_key]}
        
        # Return empty structure
        return {suburb_id: {'schools': [], 'total': 0}}

    def get_developments(self, suburb_id: str) -> Optional[Dict[str, Any]]:
        """Get development applications from file"""
        data = self._load_file('developments.json')
        if data and suburb_id in data:
            return {suburb_id: data[suburb_id]}
        
        # If suburb_id not found, use first available suburb's data
        if data:
            first_key = next(iter(data.keys()))
            logger.info(f"Using fallback data from {first_key} for {suburb_id}")
            return {suburb_id: data[first_key]}
        
        # Return empty structure
        return {suburb_id: {'developments': [], 'total': 0, 'showing': 0}}

    def get_market_insights(
        self,
        suburb_id: str,
        metric: Optional[str] = None,
        property_type: Optional[str] = None
    ) -> Optional[Dict[str, Any]]:
        """Get market insights from file"""
        data = self._load_file('market_insights.json')
        if data:
            return {suburb_id: data.get(suburb_id, {})}
        return {suburb_id: {}}

    def get_pocket_insights(
        self,
        suburb_id: str,
        geojson: bool = True,
        property_type: Optional[str] = None
    ) -> Optional[Dict[str, Any]]:
        """Get pocket insights from file"""
        data = self._load_file('pocket_insights.json')
        if data:
            return {suburb_id: data.get(suburb_id, {})}
        return {suburb_id: {}}

    def get_street_insights(
        self,
        suburb_id: str,
        geojson: bool = True,
        property_type: Optional[str] = None
    ) -> Optional[Dict[str, Any]]:
        """Get street insights from file"""
        data = self._load_file('street_insights.json')
        if data:
            return {suburb_id: data.get(suburb_id, {})}
        return {suburb_id: {}}

    def get_risk_factors(
        self,
        suburb_id: str,
        geojson: bool = True
    ) -> Optional[Dict[str, Any]]:
        """Get risk factors from file"""
        data = self._load_file('risk_factors.json')
        if data:
            return {suburb_id: data.get(suburb_id, {})}
        return {suburb_id: {}}

    def get_school_catchments(
        self,
        suburb_id: str,
        geojson: bool = True
    ) -> Optional[Dict[str, Any]]:
        """Get school catchments from file"""
        data = self._load_file('school_catchments.json')
        if data:
            return {suburb_id: data.get(suburb_id, [])}
        return {suburb_id: []}

    def get_zoning(
        self,
        suburb_id: str,
        geojson: bool = True
    ) -> Optional[Dict[str, Any]]:
        """Get zoning information from file"""
        data = self._load_file('zoning.json')
        if data:
            return {suburb_id: data.get(suburb_id, {})}
        return {suburb_id: {}}

    def get_similar_suburbs(
        self,
        suburb_id: str,
        geojson: bool = True
    ) -> Optional[Dict[str, Any]]:
        """Get similar suburbs from file"""
        data = self._load_file('similar_suburbs.json')
        if data:
            return {suburb_id: data.get(suburb_id, [])}
        return {suburb_id: []}
        
    def get_street_rankings(
        self,
        suburb_id: str,
        property_type: Optional[str] = None
    ) -> Optional[Dict[str, Any]]:
        """Get street rankings - not implemented in file repository"""
        return None

