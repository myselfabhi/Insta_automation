"""
Optimized content generator for trending space and astronomy topics
"""
import requests
import feedparser
from datetime import datetime, timedelta
from typing import Optional, Dict, Any
from functools import lru_cache
import logging
from utils import retry, logger

class ContentGenerator:
    """Generates trending space/astronomy content for reels with caching"""
    
    def __init__(self, nasa_api_key: str = 'DEMO_KEY', cache_ttl: int = 3600):
        self.nasa_api_key = nasa_api_key
        self.nasa_apod_url = 'https://api.nasa.gov/planetary/apod'
        self.space_news_rss = 'https://www.space.com/feeds/all'
        self.cache_ttl = cache_ttl  # Cache TTL in seconds
        self._cache: Dict[str, tuple] = {}  # Simple in-memory cache
        
        # Use session for connection pooling
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
        })
    
    def _get_cached(self, key: str) -> Optional[Any]:
        """Get cached value if not expired"""
        if key in self._cache:
            value, timestamp = self._cache[key]
            if datetime.now() - timestamp < timedelta(seconds=self.cache_ttl):
                return value
            else:
                del self._cache[key]
        return None
    
    def _set_cache(self, key: str, value: Any):
        """Set cache value with timestamp"""
        self._cache[key] = (value, datetime.now())
    
    @retry(max_attempts=3, delay=2.0)
    def get_nasa_apod(self) -> Optional[Dict[str, Any]]:
        """Get NASA's Astronomy Picture of the Day with caching"""
        cache_key = f"nasa_apod_{datetime.now().strftime('%Y-%m-%d')}"
        
        # Check cache first
        cached = self._get_cached(cache_key)
        if cached:
            logger.debug("Returning cached NASA APOD")
            return cached
        
        try:
            params = {'api_key': self.nasa_api_key}
            response = self.session.get(
                self.nasa_apod_url, 
                params=params, 
                timeout=10
            )
            response.raise_for_status()
            data = response.json()
            
            result = {
                'title': data.get('title', 'Space Discovery'),
                'explanation': data.get('explanation', ''),
                'image_url': data.get('url', ''),
                'date': data.get('date', datetime.now().strftime('%Y-%m-%d'))
            }
            
            # Cache the result
            self._set_cache(cache_key, result)
            logger.info(f"Fetched NASA APOD: {result['title']}")
            return result
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Error fetching NASA APOD: {e}")
            return None
        except Exception as e:
            logger.error(f"Unexpected error fetching NASA APOD: {e}")
            return None
    
    @retry(max_attempts=2, delay=2.0)
    def get_trending_space_news(self) -> Optional[Dict[str, Any]]:
        """Get trending space news from RSS feeds"""
        cache_key = "space_news"
        
        # Check cache (shorter TTL for news)
        cached = self._get_cached(cache_key)
        if cached:
            logger.debug("Returning cached space news")
            return cached
        
        try:
            feed = feedparser.parse(self.space_news_rss)
            if feed.entries:
                # Get the most recent article (not random for consistency)
                article = feed.entries[0]
                result = {
                    'title': article.get('title', 'Space News'),
                    'summary': article.get('summary', ''),
                    'link': article.get('link', '')
                }
                
                # Cache for shorter time (news changes frequently)
                self._set_cache(cache_key, result)
                logger.info(f"Fetched space news: {result['title'][:50]}...")
                return result
            else:
                logger.warning("No entries found in space news feed")
                return None
                
        except Exception as e:
            logger.error(f"Error fetching space news: {e}")
            return None
    
    def generate_caption(self, content_type: str = 'apod') -> Dict[str, Any]:
        """Generate Instagram caption with hashtags"""
        from config import Config
        
        # Try to get content based on type
        if content_type == 'apod':
            content = self.get_nasa_apod()
            if not content:
                content = self.get_trending_space_news()
                content_type = 'news'
        else:
            content = self.get_trending_space_news()
            if not content:
                content = self.get_nasa_apod()
                content_type = 'apod'
        
        # Fallback content if all sources fail
        if not content:
            logger.warning("All content sources failed, using fallback")
            content = {
                'title': 'Amazing Space Discovery',
                'explanation': 'The universe is full of wonders waiting to be discovered! 🌌✨',
                'date': datetime.now().strftime('%Y-%m-%d')
            }
        
        # Generate caption with proper formatting
        explanation = content.get('explanation', content.get('summary', ''))
        # Clean HTML tags if present
        if '<' in explanation:
            import re
            explanation = re.sub('<[^<]+?>', '', explanation)
        
        # Truncate to fit Instagram limits (2200 chars)
        max_caption_length = 2000  # Leave room for hashtags
        if len(explanation) > max_caption_length:
            explanation = explanation[:max_caption_length].rsplit(' ', 1)[0] + "..."
        
        caption_parts = [
            f"🚀 {content.get('title', 'Space Update')}",
            "",
            explanation,
            "",
            "Follow @ventureuniverse for daily space updates! 🌌✨",
            "",
            " ".join(Config.BASE_HASHTAGS[:10])  # Limit hashtags
        ]
        
        caption = "\n".join(caption_parts)
        
        return {
            'caption': caption,
            'content': content,
            'content_type': content_type
        }
    
    def get_content_for_reel(self) -> Dict[str, Any]:
        """Get content ready for reel generation"""
        # Try APOD first (usually has better images)
        apod = self.get_nasa_apod()
        if apod and apod.get('image_url'):
            return {
                'type': 'apod',
                'title': apod['title'],
                'text': apod['title'],
                'image_url': apod['image_url'],
                'description': apod['explanation'][:150] + "..." if len(apod.get('explanation', '')) > 150 else apod.get('explanation', '')
            }
        
        # Fallback to news
        news = self.get_trending_space_news()
        if news:
            return {
                'type': 'news',
                'title': news['title'],
                'text': news['title'],
                'image_url': None,
                'description': news.get('summary', '')[:150] + "..." if len(news.get('summary', '')) > 150 else news.get('summary', '')
            }
        
        # Ultimate fallback
        logger.warning("Using default fallback content")
        return {
            'type': 'default',
            'title': 'Space Discovery',
            'text': 'Exploring the Universe',
            'image_url': None,
            'description': 'The cosmos awaits!'
        }
    
    def __del__(self):
        """Cleanup session on deletion"""
        if hasattr(self, 'session'):
            self.session.close()
