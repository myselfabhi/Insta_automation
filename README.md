# 🚀 Instagram Reel Automation for Venture Universe

Automated daily Instagram reel posting tool that creates and posts space and astronomy content with your brand logo.

## ✨ Features

- 🤖 **Automated Daily Posting** - Posts reels automatically at your scheduled time
- 🎨 **Custom Branding** - Uses your Venture Universe logo with cosmic background
- 🌌 **Space Content** - Fetches trending space/astronomy content from NASA APOD and Space.com
- 📝 **Auto-Generated Captions** - Creates engaging captions with relevant hashtags
- 🔄 **Retry Logic** - Automatically retries on failures with exponential backoff
- 💾 **Session Management** - Saves login session to avoid frequent re-authentication
- 📊 **Comprehensive Logging** - Tracks all operations with detailed logs
- 🧹 **Auto Cleanup** - Automatically cleans up temporary files

## 📋 Prerequisites

- Python 3.9 or higher
- Instagram account credentials
- Internet connection
- (Optional) FFmpeg for faster video generation

## 🛠️ Installation

### 1. Clone the Repository

```bash
git clone https://github.com/myselfabhi/Insta_automation.git
cd Insta_automation
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Install FFmpeg (Optional but Recommended)

**macOS:**
```bash
brew install ffmpeg
```

**Linux (Ubuntu/Debian):**
```bash
sudo apt-get install ffmpeg
```

**Windows:**
Download from [ffmpeg.org](https://ffmpeg.org/download.html)

### 4. Configure Environment Variables

Copy the example environment file:
```bash
cp .env.example .env
```

Edit `.env` with your credentials:
```env
# Instagram Credentials
INSTAGRAM_USERNAME=your_instagram_username
INSTAGRAM_PASSWORD=your_instagram_password

# Posting Schedule (24-hour format)
POSTING_TIME=09:00

# Optional: NASA API Key (get free key from https://api.nasa.gov/)
NASA_API_KEY=DEMO_KEY

# Profile Picture Path (will be downloaded if not exists)
PROFILE_PIC_PATH=profile_pic.jpg

# Logo Settings (use Venture Universe logo instead of profile picture)
USE_LOGO=true
LOGO_PATH=assets/vu.png
```

## 🚀 Quick Start

### Test Post (Post Immediately)

Test the automation with a single post:

```bash
python3 test_post.py
```

This will:
1. Log in to Instagram
2. Fetch space content
3. Generate a reel with your logo
4. Post it to your account

### Run Daily Scheduler

Start the automated daily posting:

```bash
python3 scheduler.py
```

The scheduler will:
- Post a reel every day at the time specified in `.env` (default: 9:00 AM)
- Run continuously until stopped (Ctrl+C)
- Log all activities to `instagram_automation.log`

## 📁 Project Structure

```
Insta_automation/
├── config.py              # Configuration management
├── content_generator.py   # Fetches space/astronomy content
├── instagram_bot.py       # Instagram automation and posting
├── reel_generator.py      # Creates video reels
├── scheduler.py           # Daily scheduling and orchestration
├── utils.py               # Utility functions (retry, logging, cleanup)
├── test_post.py           # Test script for immediate posting
├── requirements.txt       # Python dependencies
├── .env                   # Your credentials (not in git)
├── .env.example           # Example configuration
├── assets/
│   └── vu.png            # Your Venture Universe logo
└── output/                # Generated reels (auto-created)
```

## 🎯 How It Works

### 1. Content Discovery
- Fetches NASA's Astronomy Picture of the Day (APOD)
- Gets trending space news from Space.com RSS feeds
- Caches content to avoid redundant API calls

### 2. Reel Generation
- Extracts cosmic background from your logo
- Combines logo, content image, and text
- Creates Instagram-optimized video (1080x1920, 30fps)
- Generates engaging captions with hashtags

### 3. Automated Posting
- Logs into Instagram (saves session for future use)
- Uploads the generated reel
- Posts with auto-generated caption
- Handles errors with automatic retries

## ⚙️ Configuration Options

### Posting Schedule

Set your posting time in `.env`:
```env
POSTING_TIME=09:00  # 24-hour format (HH:MM)
```

### Logo vs Profile Picture

Use your logo (recommended):
```env
USE_LOGO=true
LOGO_PATH=assets/vu.png
```

Or use profile picture:
```env
USE_LOGO=false
PROFILE_PIC_PATH=profile_pic.jpg
```

### Reel Settings

Edit `config.py` to customize:
- `REEL_DURATION` - Video duration in seconds (default: 15)
- `REEL_FPS` - Frame rate (default: 30)
- `BASE_HASHTAGS` - Default hashtags to include

## 📊 Logging

All activities are logged to:
- **Console** - Real-time output
- **File** - `instagram_automation.log` (detailed logs)

Log levels:
- `INFO` - Normal operations
- `WARNING` - Non-critical issues
- `ERROR` - Errors that need attention

## 🔧 Troubleshooting

### Login Issues

**Problem:** "Challenge required" or "Login required"
- **Solution:** Complete 2FA/challenge manually once
- The session will be saved for future use

**Problem:** "Rate limited"
- **Solution:** Wait a few minutes before trying again
- Instagram may temporarily restrict automated access

### Video Generation Issues

**Problem:** "ffmpeg not found"
- **Solution:** Install FFmpeg (see Installation section)
- The system will fall back to MoviePy if FFmpeg isn't available

**Problem:** Video file too large
- **Solution:** Instagram limit is ~100MB
- The system automatically validates file size before uploading

### Content Fetching Issues

**Problem:** No content fetched
- **Solution:** Check internet connection
- Verify NASA API key is valid (or use DEMO_KEY)
- Check `instagram_automation.log` for detailed errors

## 🛡️ Important Notes

### ⚠️ Instagram Automation Warning

- Instagram's Terms of Service discourage automation
- Use at your own risk - accounts may be flagged or banned
- Consider using Instagram's official API for business accounts
- Start with low frequency posting to avoid detection
- Use 2FA carefully (may require additional setup)

### Best Practices

1. **Start Slow** - Post once a day initially
2. **Monitor Activity** - Check logs regularly
3. **Keep Credentials Safe** - Never commit `.env` file
4. **Test First** - Use `test_post.py` before scheduling
5. **Backup Session** - Keep `instagram_session.json` safe

## 📚 Learning Resources

- **Python Learning Guide** - See `PYTHON_LEARNING_GUIDE.md` for detailed explanations of each file
- **Code Comments** - All files are well-commented for learning

## 🤝 Contributing

Contributions are welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## 📝 License

This project is for personal/educational use. Please respect Instagram's Terms of Service.

## 🆘 Support

For issues or questions:
1. Check the troubleshooting section
2. Review `instagram_automation.log` for errors
3. Open an issue on GitHub

## 🎉 Credits

- **NASA APOD API** - For daily astronomy pictures
- **Space.com** - For trending space news
- **instagrapi** - Instagram automation library
- **MoviePy** - Video generation
- **Pillow** - Image processing

---

**Made with ❤️ for Venture Universe**

*Automating space content, one reel at a time! 🚀✨*
