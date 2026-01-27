"""
Optimized scheduler for daily Instagram reel posting
"""
import schedule
import time
import os
import sys
from datetime import datetime
from pathlib import Path
from typing import Optional
from config import Config
from instagram_bot import InstagramBot
from content_generator import ContentGenerator
from reel_generator import ReelGenerator
from utils import logger, ensure_directory, validate_video_file

class ReelScheduler:
    """Scheduler for automated reel posting"""
    
    def __init__(self):
        self.bot: Optional[InstagramBot] = None
        self.content_gen: Optional[ContentGenerator] = None
        self.reel_gen: Optional[ReelGenerator] = None
        self.profile_pic_path = Path(Config.PROFILE_PIC_PATH)
        
    def _initialize_components(self):
        """Initialize all components"""
        try:
            # Validate config
            Config.validate()
            
            # Initialize bot
            self.bot = InstagramBot(Config.INSTAGRAM_USERNAME, Config.INSTAGRAM_PASSWORD)
            
            # Initialize content generator
            self.content_gen = ContentGenerator(Config.NASA_API_KEY)
            
            # Ensure profile picture exists
            self._ensure_profile_picture()
            
            # Initialize reel generator (use logo if configured)
            self.reel_gen = ReelGenerator(
                str(self.profile_pic_path), 
                output_dir='output',
                use_logo=Config.USE_LOGO,
                logo_path=Config.LOGO_PATH if Config.USE_LOGO else None
            )
            
            logger.info("All components initialized successfully")
            return True
            
        except Exception as e:
            logger.error(f"Failed to initialize components: {e}")
            return False
    
    def _ensure_profile_picture(self):
        """Ensure profile picture or logo exists"""
        # If using logo, check if logo exists
        if Config.USE_LOGO:
            logo_path = Path(Config.LOGO_PATH)
            if not logo_path.exists():
                logger.warning(f"Logo not found at {Config.LOGO_PATH}. Please ensure logo file exists.")
            return
        
        # Otherwise, ensure profile picture exists
        if not self.profile_pic_path.exists():
            logger.info("Profile picture not found. Downloading from Instagram...")
            
            if not self.bot.login():
                raise Exception("Failed to login to download profile picture")
            
            downloaded = self.bot.get_profile_pic(str(self.profile_pic_path))
            if not downloaded:
                logger.warning("Could not get profile picture. Creating placeholder...")
                from PIL import Image
                placeholder = Image.new('RGB', (400, 400), color='#1a1a2e')
                self.profile_pic_path.parent.mkdir(parents=True, exist_ok=True)
                placeholder.save(self.profile_pic_path)
                placeholder.close()
    
    def post_daily_reel(self):
        """Main function to post daily reel with comprehensive error handling"""
        start_time = datetime.now()
        logger.info(f"{'='*60}")
        logger.info(f"Starting daily reel posting at {start_time}")
        logger.info(f"{'='*60}")
        
        try:
            # Initialize if not already done
            if not all([self.bot, self.content_gen, self.reel_gen]):
                if not self._initialize_components():
                    logger.error("Failed to initialize components")
                    return False
            
            # Ensure we're logged in
            if not self.bot.is_logged_in():
                logger.info("Not logged in, attempting login...")
                if not self.bot.login():
                    logger.error("Failed to login. Please check credentials and try again.")
                    return False
            
            # Generate content
            logger.info("Generating content...")
            content_data = self.content_gen.get_content_for_reel()
            logger.info(f"Content generated: {content_data.get('title', 'Unknown')}")
            
            # Generate caption
            caption_data = self.content_gen.generate_caption()
            caption = caption_data['caption']
            
            # Generate reel
            logger.info("Creating reel...")
            reel_path = self.reel_gen.generate_reel(
                content_data, 
                duration=Config.REEL_DURATION
            )
            
            # Validate video file
            if not validate_video_file(reel_path):
                raise Exception(f"Invalid video file: {reel_path}")
            
            # Post reel
            logger.info("Posting reel to Instagram...")
            media = self.bot.post_reel(reel_path, caption)
            
            if media:
                elapsed = (datetime.now() - start_time).total_seconds()
                logger.info(f"✅ Daily reel posted successfully!")
                logger.info(f"   Media ID: {media.id}")
                logger.info(f"   Reel saved at: {reel_path}")
                logger.info(f"   Time taken: {elapsed:.2f} seconds")
                return True
            else:
                logger.error("Failed to post reel (no media returned)")
                return False
            
        except KeyboardInterrupt:
            logger.warning("Posting interrupted by user")
            raise
        except Exception as e:
            elapsed = (datetime.now() - start_time).total_seconds()
            logger.error(f"❌ Error posting daily reel after {elapsed:.2f}s: {e}")
            logger.exception("Full error traceback:")
            return False
    
    def run_scheduler(self):
        """Run the scheduler loop"""
        logger.info("="*60)
        logger.info("Instagram Reel Automation Scheduler")
        logger.info(f"Posting time: {Config.POSTING_TIME}")
        logger.info("Press Ctrl+C to stop")
        logger.info("="*60)
        
        # Initialize components
        if not self._initialize_components():
            logger.error("Failed to initialize. Exiting.")
            sys.exit(1)
        
        # Schedule daily posting
        schedule.every().day.at(Config.POSTING_TIME).do(self.post_daily_reel)
        
        # Keep running
        try:
            while True:
                schedule.run_pending()
                time.sleep(60)  # Check every minute
        except KeyboardInterrupt:
            logger.info("\n\nScheduler stopped by user")
            if self.bot:
                self.bot.logout()
            if self.reel_gen:
                self.reel_gen.cleanup()

def main():
    """Main entry point"""
    scheduler = ReelScheduler()
    scheduler.run_scheduler()

if __name__ == '__main__':
    main()
