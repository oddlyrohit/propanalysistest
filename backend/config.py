"""
Configuration Module
Manages application settings and environment variables
"""
import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Application configuration class"""
    
    # Microburbs API Configuration
    MICROBURBS_API_BASE_URL = os.getenv(
        'MICROBURBS_API_BASE_URL',
        'https://www.microburbs.com.au/report_generator/api'
    )
    MICROBURBS_API_TOKEN = os.getenv('MICROBURBS_API_TOKEN', 'test')
    
    # API request timeout (seconds)
    API_TIMEOUT = int(os.getenv('API_TIMEOUT', '10'))
    
    # Force use of static mock data (for debugging)
    USE_MOCK_DATA = os.getenv('USE_MOCK_DATA', 'False').lower() == 'true'
    
    # Data directory path
    DATA_DIR = os.path.join(os.path.dirname(__file__), 'data')
    
    # Logging level
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
    
    # Flask configuration
    FLASK_DEBUG = os.getenv('FLASK_DEBUG', 'True') == 'True'
    FLASK_PORT = int(os.getenv('PORT', '5001'))
    
    @classmethod
    def get_data_path(cls, filename):
        """Get full path to data file"""
        return os.path.join(cls.DATA_DIR, filename)
    
    @classmethod
    def get_api_headers(cls):
        """Get API request headers"""
        return {
            'Authorization': f'Bearer {cls.MICROBURBS_API_TOKEN}',
            'Content-Type': 'application/json'
        }

# Global configuration instance
config = Config()
