# Instagram Reel Automation for Venture Universe

Optimized automated daily Instagram reel posting tool that posts trending space and astronomy content.

## Features

- 🤖 Automated daily reel posting with retry logic
- 🚀 Trending space/astronomy content discovery with caching
- 🎨 Automatic reel generation with profile picture
- 📝 Caption and hashtag generation
- ⏰ Scheduled daily posting (configurable time)
- 🔄 Automatic retry on failures with exponential backoff
- 💾 Session management and caching for efficiency
- 📊 Comprehensive logging for monitoring
- 🧹 Automatic cleanup of temporary files
- ⚡ Optimized video generation (ffmpeg preferred, moviepy fallback)

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Create a `.env` file with your Instagram credentials:
```
INSTAGRAM_USERNAME=your_username
INSTAGRAM_PASSWORD=your_password
POSTING_TIME=09:00  # Time to post daily (24-hour format)
```

3. Run the scheduler:
```bash
python scheduler.py
```

## Important Notes

⚠️ **Instagram Automation Warning**: 
- Instagram's Terms of Service discourage automation
- Use at your own risk - accounts may be flagged or banned
- Consider using Instagram's official API for business accounts
- Start with low frequency posting to avoid detection
- Use 2FA carefully (may require additional setup)

## Project Structure

- `instagram_bot.py` - Instagram automation with retry logic and session management
- `content_generator.py` - Content discovery with caching and connection pooling
- `reel_generator.py` - Optimized reel creation with memory management
- `scheduler.py` - Scheduler with comprehensive error handling
- `utils.py` - Utility functions (retry decorator, cleanup, logging)
- `config.py` - Configuration management
- `.env` - Environment variables (credentials)
- `instagram_automation.log` - Application logs

## How It Works

1. **Content Discovery**: Fetches trending space/astronomy news from NASA API and RSS feeds with intelligent caching
2. **Reel Generation**: Creates optimized video reels combining your profile picture with content
3. **Caption Generation**: Generates engaging captions with relevant hashtags (HTML cleaned, length optimized)
4. **Automated Posting**: Posts to Instagram at scheduled time with automatic retry on failures

## Optimizations

- **Caching**: Content is cached to avoid redundant API calls
- **Connection Pooling**: HTTP sessions are reused for better performance
- **Memory Management**: Images are properly closed after use
- **Retry Logic**: Automatic retries with exponential backoff for network operations
- **Video Generation**: Prefers ffmpeg (faster) with moviepy fallback
- **Cleanup**: Automatic cleanup of temporary files
- **Logging**: Comprehensive logging to file and console
- **Error Recovery**: Graceful error handling with detailed logging
