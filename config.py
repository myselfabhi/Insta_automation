"""
Configuration management for Instagram automation
"""
import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Application configuration"""
    
    # Instagram credentials
    INSTAGRAM_USERNAME = os.getenv('INSTAGRAM_USERNAME', '')
    INSTAGRAM_PASSWORD = os.getenv('INSTAGRAM_PASSWORD', '')
    
    # Posting schedule
    POSTING_TIME = os.getenv('POSTING_TIME', '09:00')
    
    # Content sources
    NASA_API_KEY = os.getenv('NASA_API_KEY', 'DEMO_KEY')  # Free API key from api.nasa.gov
    SPACE_NEWS_RSS = 'https://www.space.com/feeds/all'
    
    # Reel settings
    REEL_DURATION = 15  # seconds
    REEL_FPS = 30
    PROFILE_PIC_PATH = os.getenv('PROFILE_PIC_PATH', 'profile_pic.jpg')
    
    # Hashtags
    BASE_HASHTAGS = [
        '#space', '#astronomy', '#nasa', '#spacex', '#universe', 
        '#cosmos', '#astrophysics', '#spaceexploration', '#ventureuniverse',
        '#spacenews', '#science', '#galaxy', '#stars', '#spacefacts'
    ]
    
    @classmethod
    def validate(cls):
        """Validate required configuration"""
        if not cls.INSTAGRAM_USERNAME or not cls.INSTAGRAM_PASSWORD:
            raise ValueError("Instagram credentials must be set in .env file")
        return True
