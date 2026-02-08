# Python Learning Guide - Understanding Your Instagram Automation Project

## 🎓 Welcome to Python!

This guide explains each file in your project as if you're learning Python for the first time. We'll cover:
- What each file does
- Key Python concepts used
- How files work together
- Real-world examples

---\\\

## 📁 File 1: `config.py` - The Settings File

### What It Does:
Think of this as a **settings/configuration file**. It stores all the important settings your program needs, like:
- Instagram username and password
- When to post (9:00 AM)
- Which logo to use
- Hashtags to include

### Key Python Concepts:

#### 1. **Import Statements** (Lines 4-5)
```python
import os
from dotenv import load_dotenv
```
**What this means:**
- `import os` - Brings in Python's built-in "os" module (operating system functions)
- `from dotenv import load_dotenv` - Brings in a function to read `.env` files
- **Think of it like:** Getting tools from a toolbox before you start working

#### 2. **Class Definition** (Line 9)
```python
class Config:
```
**What this means:**
- A **class** is like a blueprint for creating objects
- `Config` is the name of our blueprint
- **Think of it like:** A recipe card - it defines what settings we'll have

#### 3. **Class Variables** (Lines 13-37)
```python
INSTAGRAM_USERNAME = os.getenv('INSTAGRAM_USERNAME', '')
```
**What this means:**
- `INSTAGRAM_USERNAME` - A variable that stores the username
- `os.getenv()` - Gets a value from environment variables (your `.env` file)
- `'INSTAGRAM_USERNAME'` - The name of the setting to look for
- `''` - Default value if not found (empty string)
- **Think of it like:** Reading a setting from a config file, with a backup default

#### 4. **Lists** (Lines 33-37)
```python
BASE_HASHTAGS = [
    '#space', '#astronomy', '#nasa', ...
]
```
**What this means:**
- A **list** is a collection of items in square brackets `[]`
- Each item is separated by commas
- **Think of it like:** A shopping list - multiple items in one place

#### 5. **Class Method** (Lines 39-44)
```python
@classmethod
def validate(cls):
    if not cls.INSTAGRAM_USERNAME or not cls.INSTAGRAM_PASSWORD:
        raise ValueError("Instagram credentials must be set")
    return True
```
**What this means:**
- `@classmethod` - A special decorator (more on this later)
- `def validate(cls)` - A function that belongs to the class
- `if not ...` - Checks if something is missing
- `raise ValueError(...)` - Throws an error if validation fails
- **Think of it like:** A security check - makes sure you have all required settings

### Real-World Analogy:
Imagine `config.py` as a **control panel** in a car:
- It has all the settings (speed, temperature, radio station)
- You can check if everything is set correctly
- Other parts of the car (your program) can read these settings

---

## 📁 File 2: `utils.py` - Helper Functions

### What It Does:
This file contains **reusable helper functions** - small tools that other files can use. Like a Swiss Army knife with multiple tools!

### Key Python Concepts:

#### 1. **Logging Setup** (Lines 12-21)
```python
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('instagram_automation.log'),
        logging.StreamHandler()
    ]
)
```
**What this means:**
- **Logging** = Writing messages about what your program is doing
- `level=logging.INFO` - Only log important messages
- `handlers` - Where to save logs (file + console)
- **Think of it like:** A diary that automatically writes what your program does

#### 2. **Decorators** (Lines 24-47)
```python
def retry(max_attempts: int = 3, delay: float = 1.0, backoff: float = 2.0):
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            # ... retry logic ...
        return wrapper
    return decorator
```
**What this means:**
- A **decorator** is a function that wraps another function
- `@retry` - When you put this above a function, it adds retry logic
- **Think of it like:** A safety net - if something fails, try again automatically

**Example Usage:**
```python
@retry(max_attempts=3)
def download_image():
    # This function will automatically retry 3 times if it fails
    pass
```

#### 3. **Type Hints** (Line 24)
```python
def retry(max_attempts: int = 3, delay: float = 1.0):
```
**What this means:**
- `max_attempts: int` - This parameter must be an integer
- `delay: float = 1.0` - This parameter is a decimal number, default value is 1.0
- **Think of it like:** Labels on boxes - tells you what type of data goes in

#### 4. **Path Objects** (Line 53)
```python
dir_path = Path(directory)
```
**What this means:**
- `Path` - A modern way to work with file paths
- Works on Windows, Mac, and Linux
- **Think of it like:** A GPS for files - handles different operating systems

#### 5. **List Comprehension & Sorting** (Line 57)
```python
files = sorted(dir_path.glob(pattern), key=lambda p: p.stat().st_mtime, reverse=True)
```
**What this means:**
- `glob(pattern)` - Finds files matching a pattern (like `*.jpg`)
- `sorted()` - Sorts the files
- `key=lambda p: p.stat().st_mtime` - Sort by modification time
- `reverse=True` - Newest files first
- **Think of it like:** Organizing photos by date, newest first

### Real-World Analogy:
`utils.py` is like a **toolbox**:
- Each function is a different tool
- Other files can "borrow" these tools
- Makes code reusable and organized

---

## 📁 File 3: `content_generator.py` - Getting Space Content

### What It Does:
This file **fetches space/astronomy content** from the internet (NASA, space news) to use in your reels.

### Key Python Concepts:

#### 1. **Class Initialization** (Lines 15-26)
```python
def __init__(self, nasa_api_key: str = 'DEMO_KEY', cache_ttl: int = 3600):
    self.nasa_api_key = nasa_api_key
    self.nasa_apod_url = 'https://api.nasa.gov/planetary/apod'
    self._cache: Dict[str, tuple] = {}
```
**What this means:**
- `__init__` - Special method that runs when you create an object
- `self` - Refers to the object itself
- `self.nasa_api_key` - Stores data in the object
- **Think of it like:** Setting up a new phone - you configure it when you first get it

#### 2. **HTTP Requests** (Lines 54-59)
```python
response = self.session.get(
    self.nasa_apod_url, 
    params=params, 
    timeout=10
)
```
**What this means:**
- `session.get()` - Makes an HTTP GET request (like visiting a website)
- `params` - Additional parameters to send
- `timeout=10` - Wait max 10 seconds for response
- **Think of it like:** Asking a website for information and waiting for the answer

#### 3. **JSON Parsing** (Line 61)
```python
data = response.json()
```
**What this means:**
- `json()` - Converts JSON (JavaScript Object Notation) to Python dictionary
- JSON is a common data format for APIs
- **Think of it like:** Translating a foreign language into something Python understands

#### 4. **Dictionaries** (Lines 63-68)
```python
result = {
    'title': data.get('title', 'Space Discovery'),
    'explanation': data.get('explanation', ''),
    'image_url': data.get('url', ''),
}
```
**What this means:**
- A **dictionary** stores key-value pairs in curly braces `{}`
- `'title': value` - Key is 'title', value is stored data
- `data.get('title', 'Space Discovery')` - Get 'title', or use default if missing
- **Think of it like:** A phone book - look up a name (key) to get a number (value)

#### 5. **Caching** (Lines 28-40)
```python
def _get_cached(self, key: str) -> Optional[Any]:
    if key in self._cache:
        value, timestamp = self._cache[key]
        if datetime.now() - timestamp < timedelta(seconds=self.cache_ttl):
            return value
```
**What this means:**
- **Caching** = Storing data temporarily to avoid re-fetching
- Checks if data exists and is still fresh
- **Think of it like:** Remembering a phone number instead of looking it up every time

#### 6. **Error Handling** (Lines 75-80)
```python
except requests.exceptions.RequestException as e:
    logger.error(f"Error fetching NASA APOD: {e}")
    return None
```
**What this means:**
- `try/except` - Tries to do something, catches errors if they happen
- `as e` - Stores the error message in variable `e`
- `return None` - Returns nothing if error occurs
- **Think of it like:** Having a backup plan if something goes wrong

#### 7. **String Formatting** (Line 45)
```python
cache_key = f"nasa_apod_{datetime.now().strftime('%Y-%m-%d')}"
```
**What this means:**
- `f"..."` - f-string, allows inserting variables into strings
- `datetime.now()` - Gets current date/time
- `strftime('%Y-%m-%d')` - Formats date as "2026-01-27"
- **Think of it like:** Filling in blanks in a form letter

### Real-World Analogy:
`content_generator.py` is like a **news reporter**:
- Goes out to get information (from NASA, space news)
- Remembers recent stories (caching)
- Has backup sources if one fails
- Formats the information nicely

---

## 📁 File 4: `instagram_bot.py` - Instagram Automation

### What It Does:
This file handles **logging into Instagram and posting reels**. It's like a robot that controls Instagram for you.

### Key Python Concepts:

#### 1. **Context Manager** (Lines 27-34)
```python
@contextmanager
def _ensure_login(self):
    if not self._is_logged_in:
        if not self.login():
            raise Exception("Failed to login")
    yield
```
**What this means:**
- `@contextmanager` - Makes a function work with `with` statement
- `yield` - Pauses here, does the work, then continues
- **Think of it like:** Automatic door opener - opens when you enter, closes when you leave

**Usage:**
```python
with bot._ensure_login():
    # Automatically logs in if needed
    bot.post_reel(...)
```

#### 2. **Exception Handling** (Lines 67-83)
```python
except ChallengeRequired:
    logger.error("Challenge required! Please complete 2FA/challenge manually.")
    return False
except LoginRequired:
    logger.error("Login required. Check your credentials.")
    return False
```
**What this means:**
- Different `except` blocks catch different types of errors
- `ChallengeRequired` - Instagram wants 2FA verification
- `LoginRequired` - Login failed
- **Think of it like:** Different error messages for different problems

#### 3. **File Operations** (Lines 142-144)
```python
with open(save_path, 'wb') as f:
    for chunk in response.iter_content(chunk_size=8192):
        f.write(chunk)
```
**What this means:**
- `'wb'` - Write in binary mode (for images/videos)
- `with open()` - Automatically closes file when done
- `iter_content()` - Downloads in chunks (saves memory)
- **Think of it like:** Saving a large file piece by piece instead of all at once

#### 4. **Attribute Access** (Lines 124-126)
```python
profile_pic_url = (
    getattr(user_info, 'profile_pic_url_hd', None) or 
    getattr(user_info, 'profile_pic_url', None)
)
```
**What this means:**
- `getattr()` - Safely gets an attribute, returns default if missing
- Tries HD version first, then regular version
- **Think of it like:** Checking if someone has a phone number, trying mobile first, then home

### Real-World Analogy:
`instagram_bot.py` is like a **personal assistant**:
- Logs into Instagram for you
- Posts content automatically
- Handles errors gracefully
- Saves your session so you don't need to login every time

---

## 📁 File 5: `reel_generator.py` - Creating Videos

### What It Does:
This file **creates the actual video reel** - combines images, text, and your logo into a video file.

### Key Python Concepts:

#### 1. **Image Processing** (Lines 140-145)
```python
logo = Image.open(logo_path)
logo = logo.convert('RGB')
background = logo.resize((self.REEL_WIDTH, self.REEL_HEIGHT), Image.Resampling.LANCZOS)
```
**What this means:**
- `Image.open()` - Opens an image file
- `convert('RGB')` - Converts to RGB color mode
- `resize()` - Changes image size
- `LANCZOS` - High-quality resampling algorithm
- **Think of it like:** Editing a photo - opening, adjusting, resizing

#### 2. **Drawing on Images** (Lines 169, 242-249)
```python
draw = ImageDraw.Draw(frame)
draw.text((text_x, text_y + i * 50), line, fill='white', font=self._fonts['medium'])
```
**What this means:**
- `ImageDraw.Draw()` - Creates a drawing object
- `draw.text()` - Draws text on the image
- `(x, y)` - Position coordinates
- `fill='white'` - Text color
- **Think of it like:** Writing text on a picture

#### 3. **Image Masking** (Lines 100-105)
```python
mask = Image.new('L', (size, size), 0)
draw_mask = ImageDraw.Draw(mask)
draw_mask.ellipse((0, 0, size, size), fill=255)
```
**What this means:**
- Creates a **mask** - determines which parts of image are visible
- `'L'` - Grayscale mode
- `ellipse()` - Draws a circle
- Used to make circular profile pictures
- **Think of it like:** A stencil - only shows parts you want visible

#### 4. **Subprocess** (Lines 278-295)
```python
cmd = ['ffmpeg', '-y', '-loop', '1', '-i', frame_path, ...]
result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
```
**What this means:**
- `subprocess.run()` - Runs external programs (like ffmpeg)
- `cmd` - List of command arguments
- `capture_output=True` - Captures the output
- **Think of it like:** Running a command in terminal from Python

#### 5. **Path Operations** (Line 315)
```python
content_image_path = self.output_dir / 'content_image.jpg'
```
**What this means:**
- `/` operator joins paths (works on all operating systems)
- `self.output_dir` is a Path object
- **Think of it like:** Building a file path automatically

#### 6. **Method Chaining** (Line 229)
```python
content_img.thumbnail((max_size, max_size), Image.Resampling.LANCZOS)
```
**What this means:**
- `thumbnail()` - Resizes image maintaining aspect ratio
- Modifies the image in place
- **Think of it like:** Resizing a photo to fit a frame

### Real-World Analogy:
`reel_generator.py` is like a **video editor**:
- Combines images and text
- Creates the final video
- Handles different formats
- Optimizes file size

---

## 📁 File 6: `scheduler.py` - The Main Controller

### What It Does:
This is the **main controller** - it coordinates all other files to post reels automatically every day.

### Key Python Concepts:

#### 1. **Class Attributes** (Lines 20-24)
```python
def __init__(self):
    self.bot: Optional[InstagramBot] = None
    self.content_gen: Optional[ContentGenerator] = None
    self.reel_gen: Optional[ReelGenerator] = None
```
**What this means:**
- `Optional[...]` - Can be the type OR None
- `None` - Represents "nothing" or "not set yet"
- **Think of it like:** Empty slots that will be filled later

#### 2. **All Function** (Line 90)
```python
if not all([self.bot, self.content_gen, self.reel_gen]):
```
**What this means:**
- `all()` - Returns True if ALL items are truthy
- Checks if all components are initialized
- **Think of it like:** Checking if all ingredients are ready before cooking

#### 3. **Schedule Library** (Line 160)
```python
schedule.every().day.at(Config.POSTING_TIME).do(self.post_daily_reel)
```
**What this means:**
- `schedule` - External library for scheduling tasks
- `.every().day.at('09:00')` - Every day at 9 AM
- `.do(function)` - What function to run
- **Think of it like:** Setting an alarm clock

#### 4. **Infinite Loop** (Lines 164-166)
```python
while True:
    schedule.run_pending()
    time.sleep(60)
```
**What this means:**
- `while True:` - Loop forever
- `schedule.run_pending()` - Check if any scheduled tasks are due
- `time.sleep(60)` - Wait 60 seconds before checking again
- **Think of it like:** A security guard checking every minute

#### 5. **String Multiplication** (Line 84)
```python
logger.info(f"{'='*60}")
```
**What this means:**
- `'='*60` - Repeats '=' 60 times
- Creates a visual separator line
- **Think of it like:** Drawing a line with dashes

#### 6. **F-Strings with Calculations** (Line 127)
```python
elapsed = (datetime.now() - start_time).total_seconds()
logger.info(f"Time taken: {elapsed:.2f} seconds")
```
**What this means:**
- `datetime.now() - start_time` - Calculates time difference
- `.total_seconds()` - Converts to seconds
- `{elapsed:.2f}` - Formats to 2 decimal places
- **Think of it like:** Measuring how long something took

### Real-World Analogy:
`scheduler.py` is like a **conductor**:
- Coordinates all the musicians (other files)
- Keeps everything in sync
- Runs on schedule
- Handles errors gracefully

---

## 📁 File 7: `test_post.py` - Testing Script

### What It Does:
A simple script to **test posting a reel immediately** without waiting for the scheduler.

### Key Python Concepts:

#### 1. **Main Function Pattern** (Lines 8-20)
```python
def main():
    """Run a test post"""
    logger.info("Running test post...")
    scheduler = ReelScheduler()
    success = scheduler.post_daily_reel()
    
    if success:
        logger.info("Test post completed successfully!")
        sys.exit(0)
    else:
        logger.error("Test post failed!")
        sys.exit(1)
```
**What this means:**
- `def main()` - Defines the main function
- `sys.exit(0)` - Exit with success code (0 = success)
- `sys.exit(1)` - Exit with error code (1 = failure)
- **Think of it like:** A test run - try it once to see if it works

#### 2. **If Name Main Pattern** (Lines 22-23)
```python
if __name__ == '__main__':
    main()
```
**What this means:**
- `__name__` - Special variable that's `'__main__'` when script is run directly
- Only runs `main()` if script is executed directly (not imported)
- **Think of it like:** "Only do this if someone runs this file directly"

### Real-World Analogy:
`test_post.py` is like a **practice run**:
- Tests everything before the real thing
- Quick way to verify everything works
- Doesn't wait for schedule

---

## 🔗 How Files Work Together

### The Flow:

```
1. scheduler.py (Main Controller)
   ↓
2. config.py (Reads settings)
   ↓
3. content_generator.py (Gets space content)
   ↓
4. reel_generator.py (Creates video)
   ↓
5. instagram_bot.py (Posts to Instagram)
   ↓
6. utils.py (Helper functions used throughout)
```

### Example: Posting a Reel

1. **scheduler.py** starts: "Time to post!"
2. **config.py** provides: Username, password, settings
3. **content_generator.py** fetches: NASA picture of the day
4. **reel_generator.py** creates: Video with logo and text
5. **instagram_bot.py** posts: Uploads to Instagram
6. **utils.py** helps: Logging, retries, file operations

---

## 🎯 Key Python Concepts Summary

### 1. **Variables**
```python
username = "venture_universe"  # Stores a string
count = 5  # Stores a number
is_logged_in = True  # Stores a boolean (True/False)
```

### 2. **Lists**
```python
hashtags = ['#space', '#nasa', '#astronomy']
```

### 3. **Dictionaries**
```python
person = {
    'name': 'John',
    'age': 30,
    'city': 'New York'
}
```

### 4. **Functions**
```python
def greet(name):
    return f"Hello, {name}!"
```

### 5. **Classes**
```python
class Dog:
    def __init__(self, name):
        self.name = name
    
    def bark(self):
        return f"{self.name} says woof!"
```

### 6. **Error Handling**
```python
try:
    # Try to do something
    result = 10 / 0
except ZeroDivisionError:
    # Handle the error
    print("Can't divide by zero!")
```

### 7. **Loops**
```python
for i in range(5):
    print(i)  # Prints 0, 1, 2, 3, 4

while condition:
    # Do something
    pass
```

### 8. **Conditionals**
```python
if age >= 18:
    print("Adult")
elif age >= 13:
    print("Teenager")
else:
    print("Child")
```

---

## 🚀 Next Steps for Learning

1. **Practice Reading Code**
   - Read each file slowly
   - Look up concepts you don't understand
   - Try modifying small parts

2. **Experiment**
   - Change values in `config.py`
   - Add print statements to see what happens
   - Break things and fix them!

3. **Build Small Projects**
   - Start with simple scripts
   - Gradually add complexity
   - Use this project as reference

4. **Learn Python Basics**
   - Variables, lists, dictionaries
   - Functions and classes
   - Error handling
   - File operations

---

## 💡 Tips for Beginners

1. **Don't Panic!**
   - Code looks scary at first
   - Break it into small pieces
   - Understand one concept at a time

2. **Use Print Statements**
   ```python
   print(f"Value of x is: {x}")
   ```

3. **Read Error Messages**
   - They tell you what's wrong
   - Google the error message
   - Learn from mistakes

4. **Comment Your Code**
   ```python
   # This calculates the total
   total = price * quantity
   ```

5. **Practice Regularly**
   - Code a little every day
   - Build small projects
   - Don't give up!

---

**You've got this! Keep learning and coding! 🚀🐍**
