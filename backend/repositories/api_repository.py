"""
API Repository Implementation
Fetches data from external Microburbs API
"""
import logging
from typing import List, Optional, Dict, Any
from .base import SuburbRepository
from services.microburbs_api import MicroburbsApiService

logger = logging.getLogger(__name__)


class ApiSuburbRepository(SuburbRepository):
    """Repository that fetches data from Microburbs API"""

    def __init__(self, api_service: MicroburbsApiService = None):
        """
        Initialize API repository

        Args:
            api_service: MicroburbsApiService instance (optional, creates new if None)
        """
        self.api_service = api_service or MicroburbsApiService()

    def _extract_suburb_name(self, suburb_id: str) -> str:
        """Extract suburb name from suburb_id"""
        parts = suburb_id.split('-')
        if len(parts) > 1 and parts[-1].isdigit():
            parts = parts[:-1]
        suburb_name = ' '.join(parts)
        return suburb_name.title()

    def search_suburbs(self, query: str) -> List[Dict[str, Any]]:
        """Search for suburbs"""
        result = self.api_service.search_suburbs(query)
        if result and 'results' in result:
            return result['results'][:10]
        return []

    def get_suburb_info(self, suburb_id: str, geojson: bool = True) -> Optional[Dict[str, Any]]:
        """Get basic suburb information"""
        suburb_name = self._extract_suburb_name(suburb_id)
        return self.api_service.get_suburb_info(suburb_name, geojson)

    def get_suburb_summary(self, suburb_id: str) -> Optional[Dict[str, Any]]:
        """Get suburb summary with scores"""
        suburb_name = self._extract_suburb_name(suburb_id)
        return self.api_service.get_suburb_summary(suburb_name)

    def get_demographics(self, suburb_id: str) -> Optional[Dict[str, Any]]:
        """Get demographics data including ethnicity"""
        suburb_name = self._extract_suburb_name(suburb_id)
        
        # Get demographics data (age brackets)
        data = self.api_service.get_suburb_demographics(suburb_name)
        if not data:
            return None
        
        # Get ethnicity data separately
        ethnicity_data = self.api_service.get_suburb_ethnicity(suburb_name)
        
        # Merge ethnicity data into demographics if available
        if ethnicity_data:
            # If ethnicity data has 'results' key, merge it
            if 'results' in ethnicity_data:
                if 'results' not in data:
                    data['results'] = ethnicity_data['results']
            # If ethnicity data has 'ethnicities' key, add it
            elif 'ethnicities' in ethnicity_data:
                data['ethnicities'] = ethnicity_data['ethnicities']
        
        # Wrap in suburb_id key to match frontend expectations
        return {suburb_id: data}

    def get_amenities(self, suburb_id: str) -> Optional[Dict[str, Any]]:
        """Get amenities data"""
        suburb_name = self._extract_suburb_name(suburb_id)
        data = self.api_service.get_suburb_amenities(suburb_name)
        # Wrap in suburb_id key to match frontend expectations
        return {suburb_id: data} if data else None

    def get_market_trends(self, suburb_id: str) -> Optional[Dict[str, Any]]:
        """Get market trends"""
        suburb_name = self._extract_suburb_name(suburb_id)
        data = self.api_service.get_suburb_market_data(suburb_name)
        # Wrap in suburb_id key to match frontend expectations
        return {suburb_id: data} if data else None

    def get_schools(self, suburb_id: str) -> Optional[Dict[str, Any]]:
        """Get schools data"""
        suburb_name = self._extract_suburb_name(suburb_id)
        data = self.api_service.get_suburb_schools(suburb_name)
        # Wrap in suburb_id key to match frontend expectations
        return {suburb_id: data} if data else None

    def get_developments(self, suburb_id: str) -> Optional[Dict[str, Any]]:
        """Get development applications"""
        suburb_name = self._extract_suburb_name(suburb_id)
        data = self.api_service.get_suburb_development(suburb_name)
        # Wrap in suburb_id key to match frontend expectations
        return {suburb_id: data} if data else None

    def get_market_insights(
        self,
        suburb_id: str,
        metric: Optional[str] = None,
        property_type: Optional[str] = None
    ) -> Optional[Dict[str, Any]]:
        """Get market insights"""
        suburb_name = self._extract_suburb_name(suburb_id)
        return self.api_service.get_suburb_market_insights(suburb_name, metric, property_type)

    def get_pocket_insights(
        self,
        suburb_id: str,
        geojson: bool = True,
        property_type: Optional[str] = None
    ) -> Optional[Dict[str, Any]]:
        """Get pocket-level insights"""
        suburb_name = self._extract_suburb_name(suburb_id)
        return self.api_service.get_suburb_pocket_insights(suburb_name, geojson, property_type)

    def get_street_insights(
        self,
        suburb_id: str,
        geojson: bool = True,
        property_type: Optional[str] = None
    ) -> Optional[Dict[str, Any]]:
        """Get street-level insights"""
        suburb_name = self._extract_suburb_name(suburb_id)
        data = self.api_service.get_suburb_street_insights(suburb_name, property_type)
        # Wrap in suburb_id key to match frontend expectations
        return {suburb_id: data} if data else None

    def get_risk_factors(
        self,
        suburb_id: str,
        geojson: bool = True
    ) -> Optional[Dict[str, Any]]:
        """Get risk factors"""
        suburb_name = self._extract_suburb_name(suburb_id)
        return self.api_service.get_suburb_risk(suburb_name)

    def get_school_catchments(
        self,
        suburb_id: str,
        geojson: bool = True
    ) -> Optional[Dict[str, Any]]:
        """Get school catchment areas"""
        suburb_name = self._extract_suburb_name(suburb_id)
        return self.api_service.get_suburb_catchments(suburb_name, geojson)

    def get_zoning(
        self,
        suburb_id: str,
        geojson: bool = True
    ) -> Optional[Dict[str, Any]]:
        """Get zoning information"""
        suburb_name = self._extract_suburb_name(suburb_id)
        return self.api_service.get_suburb_zoning(suburb_name, geojson)

    def get_similar_suburbs(
        self,
        suburb_id: str,
        geojson: bool = True
    ) -> Optional[Dict[str, Any]]:
        """Get similar suburbs"""
        suburb_name = self._extract_suburb_name(suburb_id)
        return self.api_service.get_similar_suburbs(suburb_name, geojson)
    def get_street_rankings(
        self,
        suburb_id: str,
        property_type: Optional[str] = None
    ) -> Optional[Dict[str, Any]]:
        """Get street rankings - not implemented in base API, will be handled by data aggregator"""
        # This method is implemented in DataAggregatorService
        # It processes street insights data to create rankings
        return None
