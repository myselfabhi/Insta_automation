"""
Utility functions for Instagram automation
"""
import logging
import os
import functools
import time
from typing import Optional, Callable, Any
from pathlib import Path

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('instagram_automation.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)


def retry(max_attempts: int = 3, delay: float = 1.0, backoff: float = 2.0):
    """Retry decorator with exponential backoff"""
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            attempt = 0
            current_delay = delay
            
            while attempt < max_attempts:
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    attempt += 1
                    if attempt >= max_attempts:
                        logger.error(f"{func.__name__} failed after {max_attempts} attempts: {e}")
                        raise
                    
                    logger.warning(f"{func.__name__} failed (attempt {attempt}/{max_attempts}): {e}. Retrying in {current_delay}s...")
                    time.sleep(current_delay)
                    current_delay *= backoff
            
            return None
        return wrapper
    return decorator


def cleanup_temp_files(directory: str, pattern: str = "*", keep_recent: int = 5):
    """Clean up temporary files, keeping only the most recent ones"""
    try:
        dir_path = Path(directory)
        if not dir_path.exists():
            return
        
        files = sorted(dir_path.glob(pattern), key=lambda p: p.stat().st_mtime, reverse=True)
        
        # Keep the most recent files
        for file in files[keep_recent:]:
            try:
                file.unlink()
                logger.debug(f"Cleaned up old file: {file}")
            except Exception as e:
                logger.warning(f"Failed to delete {file}: {e}")
    except Exception as e:
        logger.warning(f"Error during cleanup: {e}")


def ensure_directory(path: str) -> Path:
    """Ensure directory exists, create if it doesn't"""
    dir_path = Path(path)
    dir_path.mkdir(parents=True, exist_ok=True)
    return dir_path


def get_file_size_mb(file_path: str) -> float:
    """Get file size in MB"""
    try:
        size_bytes = os.path.getsize(file_path)
        return size_bytes / (1024 * 1024)
    except Exception:
        return 0.0


def validate_video_file(file_path: str, min_size_mb: float = 0.1) -> bool:
    """Validate video file exists and meets minimum size requirement"""
    if not os.path.exists(file_path):
        return False
    
    size_mb = get_file_size_mb(file_path)
    if size_mb < min_size_mb:
        logger.warning(f"Video file too small: {size_mb:.2f}MB (minimum: {min_size_mb}MB)")
        return False
    
    return True
