"""
Models Package
Data Transfer Objects (DTOs) for structured data
"""
from .suburb import SuburbDTO, SuburbSearchResultDTO
from .demographics import DemographicsDTO, AgeDistributionDTO, EthnicityDTO
from .amenities import AmenitiesDTO, AmenityDTO

__all__ = [
    'SuburbDTO',
    'SuburbSearchResultDTO',
    'DemographicsDTO',
    'AgeDistributionDTO',
    'EthnicityDTO',
    'AmenitiesDTO',
    'AmenityDTO',
]
