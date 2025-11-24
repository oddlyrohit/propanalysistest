"""
Base Repository Interface
Defines the contract for suburb data access
"""
from abc import ABC, abstractmethod
from typing import List, Optional, Dict, Any


class SuburbRepository(ABC):
    """Abstract base class for suburb data repositories"""

    @abstractmethod
    def search_suburbs(self, query: str) -> List[Dict[str, Any]]:
        """
        Search for suburbs by name

        Args:
            query: Search query string

        Returns:
            List of suburb dictionaries
        """
        pass

    @abstractmethod
    def get_suburb_info(self, suburb_id: str, geojson: bool = True) -> Optional[Dict[str, Any]]:
        """
        Get basic suburb information

        Args:
            suburb_id: Suburb identifier
            geojson: Whether to include GeoJSON data (default: True)

        Returns:
            Suburb info dictionary or None
        """
        pass

    @abstractmethod
    def get_suburb_summary(self, suburb_id: str) -> Optional[Dict[str, Any]]:
        """
        Get suburb summary with scores

        Args:
            suburb_id: Suburb identifier

        Returns:
            Suburb summary dictionary or None
        """
        pass

    @abstractmethod
    def get_demographics(self, suburb_id: str) -> Optional[Dict[str, Any]]:
        """
        Get demographics data for a suburb

        Args:
            suburb_id: Suburb identifier

        Returns:
            Demographics dictionary or None
        """
        pass

    @abstractmethod
    def get_amenities(self, suburb_id: str) -> Optional[Dict[str, Any]]:
        """
        Get amenities data for a suburb

        Args:
            suburb_id: Suburb identifier

        Returns:
            Amenities dictionary or None
        """
        pass

    @abstractmethod
    def get_market_trends(self, suburb_id: str) -> Optional[Dict[str, Any]]:
        """
        Get market trends for a suburb

        Args:
            suburb_id: Suburb identifier

        Returns:
            Market trends dictionary or None
        """
        pass

    @abstractmethod
    def get_schools(self, suburb_id: str) -> Optional[Dict[str, Any]]:
        """
        Get schools data for a suburb

        Args:
            suburb_id: Suburb identifier

        Returns:
            Schools dictionary or None
        """
        pass

    @abstractmethod
    def get_developments(self, suburb_id: str) -> Optional[Dict[str, Any]]:
        """
        Get development applications for a suburb

        Args:
            suburb_id: Suburb identifier

        Returns:
            Developments dictionary or None
        """
        pass

    @abstractmethod
    def get_market_insights(
        self,
        suburb_id: str,
        metric: Optional[str] = None,
        property_type: Optional[str] = None
    ) -> Optional[Dict[str, Any]]:
        """
        Get market insights with optional filters

        Args:
            suburb_id: Suburb identifier
            metric: Optional metric filter
            property_type: Optional property type filter

        Returns:
            Market insights dictionary or None
        """
        pass

    @abstractmethod
    def get_pocket_insights(
        self,
        suburb_id: str,
        geojson: bool = True,
        property_type: Optional[str] = None
    ) -> Optional[Dict[str, Any]]:
        """
        Get pocket-level insights

        Args:
            suburb_id: Suburb identifier
            geojson: Whether to include GeoJSON data
            property_type: Optional property type filter

        Returns:
            Pocket insights dictionary or None
        """
        pass

    @abstractmethod
    def get_street_insights(
        self,
        suburb_id: str,
        geojson: bool = True,
        property_type: Optional[str] = None
    ) -> Optional[Dict[str, Any]]:
        """
        Get street-level insights

        Args:
            suburb_id: Suburb identifier
            geojson: Whether to include GeoJSON data
            property_type: Optional property type filter

        Returns:
            Street insights dictionary or None
        """
        pass

    @abstractmethod
    def get_risk_factors(
        self,
        suburb_id: str,
        geojson: bool = True
    ) -> Optional[Dict[str, Any]]:
        """
        Get risk factors for a suburb

        Args:
            suburb_id: Suburb identifier
            geojson: Whether to include GeoJSON data

        Returns:
            Risk factors dictionary or None
        """
        pass

    @abstractmethod
    def get_school_catchments(
        self,
        suburb_id: str,
        geojson: bool = True
    ) -> Optional[Dict[str, Any]]:
        """
        Get school catchment areas

        Args:
            suburb_id: Suburb identifier
            geojson: Whether to include GeoJSON data

        Returns:
            School catchments dictionary or None
        """
        pass

    @abstractmethod
    def get_zoning(
        self,
        suburb_id: str,
        geojson: bool = True
    ) -> Optional[Dict[str, Any]]:
        """
        Get zoning information

        Args:
            suburb_id: Suburb identifier
            geojson: Whether to include GeoJSON data

        Returns:
            Zoning dictionary or None
        """
        pass

    @abstractmethod
    def get_similar_suburbs(
        self,
        suburb_id: str,
        geojson: bool = True
    ) -> Optional[Dict[str, Any]]:
        """
        Get similar suburbs

        Args:
            suburb_id: Suburb identifier
            geojson: Whether to include GeoJSON data

        Returns:
            Similar suburbs dictionary or None
        """
        pass

    @abstractmethod
    def get_street_rankings(
        self,
        suburb_id: str,
        property_type: Optional[str] = None
    ) -> Optional[Dict[str, Any]]:
        """Get street rankings"""
        pass