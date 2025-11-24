"""
Demographics Data Transfer Objects
"""
from dataclasses import dataclass
from typing import List


@dataclass
class AgeDistributionDTO:
    """Age distribution data"""
    age_range: str
    percentage: float
    count: int = 0

    def to_dict(self) -> dict:
        return {
            'ageRange': self.age_range,
            'percentage': self.percentage,
            'count': self.count,
        }

    @classmethod
    def from_dict(cls, data: dict) -> 'AgeDistributionDTO':
        return cls(
            age_range=data.get('age_range', data.get('ageRange', '')),
            percentage=data.get('percentage', 0.0),
            count=data.get('count', 0),
        )


@dataclass
class EthnicityDTO:
    """Ethnicity data"""
    ethnicity: str
    percentage: float
    count: int = 0

    def to_dict(self) -> dict:
        return {
            'ethnicity': self.ethnicity,
            'percentage': self.percentage,
            'count': self.count,
        }

    @classmethod
    def from_dict(cls, data: dict) -> 'EthnicityDTO':
        return cls(
            ethnicity=data.get('ethnicity', ''),
            percentage=data.get('percentage', 0.0),
            count=data.get('count', 0),
        )


@dataclass
class DemographicsDTO:
    """Complete demographics data for a suburb"""
    suburb_id: str
    age_distribution: List[AgeDistributionDTO]
    ethnicity: List[EthnicityDTO]
    median_age: int = 0
    median_income: int = 0
    unemployment_rate: float = 0.0
    education_level_bachelor_plus: float = 0.0

    def to_dict(self) -> dict:
        return {
            self.suburb_id: {
                'ageDistribution': [age.to_dict() for age in self.age_distribution],
                'ethnicity': [eth.to_dict() for eth in self.ethnicity],
                'medianAge': self.median_age,
                'medianIncome': self.median_income,
                'unemploymentRate': self.unemployment_rate,
                'educationLevelBachelorPlus': self.education_level_bachelor_plus,
            }
        }

    @classmethod
    def from_dict(cls, suburb_id: str, data: dict) -> 'DemographicsDTO':
        """Create from dictionary"""
        suburb_data = data.get(suburb_id, data)

        age_dist = [
            AgeDistributionDTO.from_dict(item)
            for item in suburb_data.get('ageDistribution', suburb_data.get('age_distribution', []))
        ]

        ethnicity = [
            EthnicityDTO.from_dict(item)
            for item in suburb_data.get('ethnicity', [])
        ]

        return cls(
            suburb_id=suburb_id,
            age_distribution=age_dist,
            ethnicity=ethnicity,
            median_age=suburb_data.get('medianAge', suburb_data.get('median_age', 0)),
            median_income=suburb_data.get('medianIncome', suburb_data.get('median_income', 0)),
            unemployment_rate=suburb_data.get('unemploymentRate', suburb_data.get('unemployment_rate', 0.0)),
            education_level_bachelor_plus=suburb_data.get('educationLevelBachelorPlus', suburb_data.get('education_level_bachelor_plus', 0.0)),
        )
