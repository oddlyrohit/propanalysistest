"""
Composite Repository Implementation
Combines API and File repositories with fallback mechanism
"""
import logging
from typing import List, Optional, Dict, Any
from .base import SuburbRepository
from .api_repository import ApiSuburbRepository
from .file_repository import FileSuburbRepository

logger = logging.getLogger(__name__)


class CompositeSuburbRepository(SuburbRepository):
    """
    Repository that tries API first, falls back to file if API fails
    """

    def __init__(
        self,
        api_repo: ApiSuburbRepository = None,
        file_repo: FileSuburbRepository = None
    ):
        """
        Initialize composite repository

        Args:
            api_repo: API repository instance (creates new if None)
            file_repo: File repository instance (creates new if None)
        """
        self.api_repo = api_repo or ApiSuburbRepository()
        self.file_repo = file_repo or FileSuburbRepository()

    def _try_api_then_file(
        self,
        method_name: str,
        *args,
        **kwargs
    ) -> Optional[Dict[str, Any]]:
        """
        Try API repository first, fallback to file repository

        Args:
            method_name: Name of the repository method to call
            *args: Positional arguments for the method
            **kwargs: Keyword arguments for the method

        Returns:
            Data from API or file, or None
        """
        # Try API first
        try:
            api_method = getattr(self.api_repo, method_name)
            result = api_method(*args, **kwargs)
            if result:
                logger.debug(f"Data retrieved from API: {method_name}")
                return result
            logger.debug(f"API returned no data for: {method_name}")
        except Exception as e:
            logger.warning(f"API call failed for {method_name}: {str(e)}")

        # Fallback to file
        try:
            file_method = getattr(self.file_repo, method_name)
            result = file_method(*args, **kwargs)
            if result:
                logger.info(f"Data retrieved from file fallback: {method_name}")
                return result
            logger.debug(f"File fallback returned no data for: {method_name}")
        except Exception as e:
            logger.error(f"File fallback failed for {method_name}: {str(e)}")

        return None

    def search_suburbs(self, query: str) -> List[Dict[str, Any]]:
        """Search for suburbs (API first, then file)"""
        result = self._try_api_then_file('search_suburbs', query)
        return result if result else []

    def get_suburb_info(self, suburb_id: str, geojson: bool = True) -> Optional[Dict[str, Any]]:
        """Get suburb info (API first, then file)"""
        return self._try_api_then_file('get_suburb_info', suburb_id, geojson=geojson)

    def get_suburb_summary(self, suburb_id: str) -> Optional[Dict[str, Any]]:
        """Get suburb summary (API first, then file)"""
        return self._try_api_then_file('get_suburb_summary', suburb_id)

    def get_demographics(self, suburb_id: str) -> Optional[Dict[str, Any]]:
        """Get demographics (API first, then file)"""
        return self._try_api_then_file('get_demographics', suburb_id)

    def get_amenities(self, suburb_id: str) -> Optional[Dict[str, Any]]:
        """Get amenities (API first, then file)"""
        return self._try_api_then_file('get_amenities', suburb_id)

    def get_market_trends(self, suburb_id: str) -> Optional[Dict[str, Any]]:
        """Get market trends (API first, then file)"""
        return self._try_api_then_file('get_market_trends', suburb_id)

    def get_schools(self, suburb_id: str) -> Optional[Dict[str, Any]]:
        """Get schools (API first, then file)"""
        return self._try_api_then_file('get_schools', suburb_id)

    def get_developments(self, suburb_id: str) -> Optional[Dict[str, Any]]:
        """Get developments (API first, then file)"""
        return self._try_api_then_file('get_developments', suburb_id)

    def get_market_insights(
        self,
        suburb_id: str,
        metric: Optional[str] = None,
        property_type: Optional[str] = None
    ) -> Optional[Dict[str, Any]]:
        """Get market insights (API first, then file)"""
        return self._try_api_then_file(
            'get_market_insights',
            suburb_id,
            metric=metric,
            property_type=property_type
        )

    def get_pocket_insights(
        self,
        suburb_id: str,
        geojson: bool = True,
        property_type: Optional[str] = None
    ) -> Optional[Dict[str, Any]]:
        """Get pocket insights (API first, then file)"""
        return self._try_api_then_file(
            'get_pocket_insights',
            suburb_id,
            geojson=geojson,
            property_type=property_type
        )

    def get_street_insights(
        self,
        suburb_id: str,
        geojson: bool = True,
        property_type: Optional[str] = None
    ) -> Optional[Dict[str, Any]]:
        """Get street insights (API first, then file)"""
        return self._try_api_then_file(
            'get_street_insights',
            suburb_id,
            geojson=geojson,
            property_type=property_type
        )

    def get_risk_factors(
        self,
        suburb_id: str,
        geojson: bool = True
    ) -> Optional[Dict[str, Any]]:
        """Get risk factors (API first, then file)"""
        return self._try_api_then_file(
            'get_risk_factors',
            suburb_id,
            geojson=geojson
        )

    def get_school_catchments(
        self,
        suburb_id: str,
        geojson: bool = True
    ) -> Optional[Dict[str, Any]]:
        """Get school catchments (API first, then file)"""
        return self._try_api_then_file(
            'get_school_catchments',
            suburb_id,
            geojson=geojson
        )

    def get_zoning(
        self,
        suburb_id: str,
        geojson: bool = True
    ) -> Optional[Dict[str, Any]]:
        """Get zoning (API first, then file)"""
        return self._try_api_then_file(
            'get_zoning',
            suburb_id,
            geojson=geojson
        )

    def get_similar_suburbs(
        self,
        suburb_id: str,
        geojson: bool = True
    ) -> Optional[Dict[str, Any]]:
        """Get similar suburbs (API first, then file)"""
        return self._try_api_then_file(
            'get_similar_suburbs',
            suburb_id,
            geojson=geojson
        )

    def get_street_rankings(
        self,
        suburb_id: str,
        property_type: Optional[str] = None
    ) -> Optional[Dict[str, Any]]:
        """Get street rankings (API first, then file)"""
        return self._try_api_then_file(
            'get_street_rankings',
            suburb_id,
            property_type=property_type
        )
    
    def get_street_rankings(
        self,
        suburb_id: str,
        property_type: Optional[str] = None
    ) -> Optional[Dict[str, Any]]:
        """Get street rankings"""
        # Try API repository first
        result = self.api_repo.get_street_rankings(suburb_id, property_type)
        if result:
            return result
        
        # Fall back to file repository
        return self.file_repo.get_street_rankings(suburb_id, property_type)
