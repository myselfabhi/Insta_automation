"""
Optimized Instagram automation bot for posting reels
"""
import os
import time
import logging
from pathlib import Path
from typing import Optional
from contextlib import contextmanager
from instagrapi import Client
from instagrapi.exceptions import LoginRequired, ChallengeRequired, PleaseWaitFewMinutes
from utils import retry, logger

class InstagramBot:
    """Instagram bot for automated posting with optimized error handling"""
    
    def __init__(self, username: str, password: str, session_file: str = 'instagram_session.json'):
        self.username = username
        self.password = password
        self.session_file = session_file
        self.client = Client()
        self._is_logged_in = False
        
        # Configure client settings for better reliability
        self.client.delay_range = [1, 3]  # Random delay between requests
        
    @contextmanager
    def _ensure_login(self):
        """Context manager to ensure login before operations"""
        if not self._is_logged_in:
            if not self.login():
                raise Exception("Failed to login to Instagram")
        yield
        # Optionally refresh session periodically
    
    @retry(max_attempts=3, delay=2.0)
    def login(self) -> bool:
        """Login to Instagram with session management"""
        try:
            # Try to load existing session
            if os.path.exists(self.session_file):
                try:
                    self.client.load_settings(self.session_file)
                    # Verify session is still valid
                    self.client.account_info()
                    logger.info("Logged in using saved session")
                    self._is_logged_in = True
                    return True
                except Exception as e:
                    logger.warning(f"Session invalid: {e}. Attempting fresh login...")
                    # Remove invalid session file
                    try:
                        os.remove(self.session_file)
                    except:
                        pass
            
            # Fresh login
            logger.info("Logging in to Instagram...")
            self.client.login(self.username, self.password)
            
            # Save session for future use
            self.client.dump_settings(self.session_file)
            logger.info("Login successful!")
            self._is_logged_in = True
            return True
            
        except ChallengeRequired:
            logger.error("Challenge required! Please complete 2FA/challenge manually.")
            logger.error("You may need to log in manually once to complete the challenge.")
            self._is_logged_in = False
            return False
        except LoginRequired:
            logger.error("Login required. Please check your credentials.")
            self._is_logged_in = False
            return False
        except PleaseWaitFewMinutes as e:
            logger.error(f"Rate limited: {e}. Please wait before trying again.")
            self._is_logged_in = False
            return False
        except Exception as e:
            logger.error(f"Login error: {e}")
            self._is_logged_in = False
            return False
    
    @retry(max_attempts=2, delay=5.0)
    def post_reel(self, video_path: str, caption: str) -> Optional[object]:
        """Post a reel to Instagram with retry logic"""
        with self._ensure_login():
            if not os.path.exists(video_path):
                raise FileNotFoundError(f"Video file not found: {video_path}")
            
            # Validate file size
            file_size_mb = os.path.getsize(video_path) / (1024 * 1024)
            if file_size_mb > 100:  # Instagram limit is ~100MB
                raise ValueError(f"Video file too large: {file_size_mb:.2f}MB (max 100MB)")
            
            logger.info(f"Uploading reel: {video_path} ({file_size_mb:.2f}MB)")
            logger.debug(f"Caption preview: {caption[:100]}...")
            
            try:
                # Upload reel
                media = self.client.clip_upload(
                    video_path,
                    caption=caption
                )
                
                logger.info(f"Reel posted successfully! Media ID: {media.id}")
                return media
                
            except PleaseWaitFewMinutes as e:
                logger.error(f"Rate limited: {e}")
                raise
            except Exception as e:
                logger.error(f"Error posting reel: {e}")
                raise
    
    @retry(max_attempts=2, delay=2.0)
    def get_profile_pic(self, save_path: str = 'profile_pic.jpg') -> Optional[str]:
        """Download profile picture with retry logic"""
        with self._ensure_login():
            try:
                user_info = self.client.account_info()
                # account_info returns an Account object with attributes
                profile_pic_url = (
                    getattr(user_info, 'profile_pic_url_hd', None) or 
                    getattr(user_info, 'profile_pic_url', None)
                )
                
                if not profile_pic_url:
                    logger.warning("Could not retrieve profile picture URL")
                    return None
                
                # Download profile picture
                import requests
                response = requests.get(profile_pic_url, timeout=10, stream=True)
                response.raise_for_status()
                
                # Save to file
                save_path_obj = Path(save_path)
                save_path_obj.parent.mkdir(parents=True, exist_ok=True)
                
                with open(save_path, 'wb') as f:
                    for chunk in response.iter_content(chunk_size=8192):
                        f.write(chunk)
                
                logger.info(f"Profile picture saved to {save_path}")
                return save_path
                
            except Exception as e:
                logger.error(f"Error getting profile picture: {e}")
                return None
    
    def is_logged_in(self) -> bool:
        """Check if currently logged in"""
        if not self._is_logged_in:
            return False
        
        try:
            self.client.account_info()
            return True
        except:
            self._is_logged_in = False
            return False
    
    def logout(self):
        """Logout and cleanup"""
        try:
            if self._is_logged_in:
                self.client.logout()
                logger.info("Logged out successfully")
        except:
            pass
        finally:
            self._is_logged_in = False
