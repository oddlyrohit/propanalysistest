"""
Amenities Data Transfer Objects
"""
from dataclasses import dataclass
from typing import List, Optional


@dataclass
class AmenityDTO:
    """Single amenity data"""
    name: str
    category: str
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    address: Optional[str] = None
    rating: Optional[float] = None
    distance_km: Optional[float] = None

    def to_dict(self) -> dict:
        return {
            'name': self.name,
            'category': self.category,
            'latitude': self.latitude,
            'longitude': self.longitude,
            'address': self.address,
            'rating': self.rating,
            'distanceKm': self.distance_km,
        }

    @classmethod
    def from_dict(cls, data: dict) -> 'AmenityDTO':
        return cls(
            name=data.get('name', ''),
            category=data.get('category', ''),
            latitude=data.get('latitude'),
            longitude=data.get('longitude'),
            address=data.get('address'),
            rating=data.get('rating'),
            distance_km=data.get('distance_km', data.get('distanceKm')),
        )


@dataclass
class AmenitiesDTO:
    """Complete amenities data for a suburb"""
    suburb_id: str
    cafes: List[AmenityDTO]
    restaurants: List[AmenityDTO]
    parks: List[AmenityDTO]
    gyms: List[AmenityDTO]
    shopping_centers: List[AmenityDTO]
    public_transport: List[AmenityDTO]

    def to_dict(self) -> dict:
        return {
            self.suburb_id: {
                'cafes': [cafe.to_dict() for cafe in self.cafes],
                'restaurants': [rest.to_dict() for rest in self.restaurants],
                'parks': [park.to_dict() for park in self.parks],
                'gyms': [gym.to_dict() for gym in self.gyms],
                'shoppingCenters': [shop.to_dict() for shop in self.shopping_centers],
                'publicTransport': [trans.to_dict() for trans in self.public_transport],
                'totalCount': (
                    len(self.cafes) + len(self.restaurants) + len(self.parks) +
                    len(self.gyms) + len(self.shopping_centers) + len(self.public_transport)
                ),
            }
        }

    @classmethod
    def from_dict(cls, suburb_id: str, data: dict) -> 'AmenitiesDTO':
        """Create from dictionary"""
        suburb_data = data.get(suburb_id, data)

        return cls(
            suburb_id=suburb_id,
            cafes=[AmenityDTO.from_dict(item) for item in suburb_data.get('cafes', [])],
            restaurants=[AmenityDTO.from_dict(item) for item in suburb_data.get('restaurants', [])],
            parks=[AmenityDTO.from_dict(item) for item in suburb_data.get('parks', [])],
            gyms=[AmenityDTO.from_dict(item) for item in suburb_data.get('gyms', [])],
            shopping_centers=[AmenityDTO.from_dict(item) for item in suburb_data.get('shoppingCenters', suburb_data.get('shopping_centers', []))],
            public_transport=[AmenityDTO.from_dict(item) for item in suburb_data.get('publicTransport', suburb_data.get('public_transport', []))],
        )
