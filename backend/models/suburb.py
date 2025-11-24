"""
Suburb Data Transfer Objects
"""
from dataclasses import dataclass
from typing import Optional


@dataclass
class SuburbSearchResultDTO:
    """DTO for suburb search results"""
    id: str
    name: str
    state: str
    postcode: str
    population: int = 0
    median_age: int = 0
    median_house_price: int = 0
    median_rent: int = 0
    amenities_count: int = 0
    schools_count: int = 0
    development_apps: int = 0

    def to_dict(self) -> dict:
        """Convert to dictionary for JSON serialization"""
        return {
            'id': self.id,
            'name': self.name,
            'state': self.state,
            'postcode': self.postcode,
            'population': self.population,
            'medianAge': self.median_age,
            'medianHousePrice': self.median_house_price,
            'medianRent': self.median_rent,
            'amenitiesCount': self.amenities_count,
            'schoolsCount': self.schools_count,
            'developmentApps': self.development_apps,
        }

    @classmethod
    def from_dict(cls, data: dict) -> 'SuburbSearchResultDTO':
        """Create from dictionary"""
        return cls(
            id=data.get('id', ''),
            name=data.get('name', ''),
            state=data.get('state', ''),
            postcode=data.get('postcode', ''),
            population=data.get('population', 0),
            median_age=data.get('median_age', 0),
            median_house_price=data.get('median_house_price', 0),
            median_rent=data.get('median_rent', 0),
            amenities_count=data.get('amenities_count', 0),
            schools_count=data.get('schools_count', 0),
            development_apps=data.get('development_apps', 0),
        )


@dataclass
class SuburbDTO:
    """DTO for detailed suburb information"""
    id: str
    name: str
    state: str
    postcode: str
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    area_sqkm: Optional[float] = None
    population: int = 0
    population_density: Optional[float] = None
    median_age: int = 0
    median_income: Optional[int] = None
    unemployment_rate: Optional[float] = None

    # Market data
    median_house_price: int = 0
    median_unit_price: int = 0
    median_rent: int = 0
    price_growth_1y: Optional[float] = None
    price_growth_5y: Optional[float] = None
    rental_yield: Optional[float] = None

    # Counts
    amenities_count: int = 0
    schools_count: int = 0
    development_apps: int = 0

    def to_dict(self) -> dict:
        """Convert to dictionary for JSON serialization"""
        return {
            'id': self.id,
            'name': self.name,
            'state': self.state,
            'postcode': self.postcode,
            'latitude': self.latitude,
            'longitude': self.longitude,
            'areaSqkm': self.area_sqkm,
            'population': self.population,
            'populationDensity': self.population_density,
            'medianAge': self.median_age,
            'medianIncome': self.median_income,
            'unemploymentRate': self.unemployment_rate,
            'medianHousePrice': self.median_house_price,
            'medianUnitPrice': self.median_unit_price,
            'medianRent': self.median_rent,
            'priceGrowth1y': self.price_growth_1y,
            'priceGrowth5y': self.price_growth_5y,
            'rentalYield': self.rental_yield,
            'amenitiesCount': self.amenities_count,
            'schoolsCount': self.schools_count,
            'developmentApps': self.development_apps,
        }

    @classmethod
    def from_dict(cls, data: dict) -> 'SuburbDTO':
        """Create from dictionary"""
        return cls(
            id=data.get('id', ''),
            name=data.get('name', ''),
            state=data.get('state', ''),
            postcode=data.get('postcode', ''),
            latitude=data.get('latitude'),
            longitude=data.get('longitude'),
            area_sqkm=data.get('area_sqkm'),
            population=data.get('population', 0),
            population_density=data.get('population_density'),
            median_age=data.get('median_age', 0),
            median_income=data.get('median_income'),
            unemployment_rate=data.get('unemployment_rate'),
            median_house_price=data.get('median_house_price', 0),
            median_unit_price=data.get('median_unit_price', 0),
            median_rent=data.get('median_rent', 0),
            price_growth_1y=data.get('price_growth_1y'),
            price_growth_5y=data.get('price_growth_5y'),
            rental_yield=data.get('rental_yield'),
            amenities_count=data.get('amenities_count', 0),
            schools_count=data.get('schools_count', 0),
            development_apps=data.get('development_apps', 0),
        )
