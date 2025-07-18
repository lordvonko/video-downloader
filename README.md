# Video Downloader App

A simple desktop application for downloading videos from various platforms using yt-dlp.
Supports optional cookies for logged-in content.
![Screenshot](assets/screenshot.png)  <!-- Add a screenshot here for visual appeal -->

## Features
- Easy URL input and download button.
- Private without ADS, fuck youtube convert sites.
- Customizable save directory.
- Optional cookies file for sites requiring login (e.g., private TikTok videos).
- Progress updates in the app.

## Prerequisites
- Python 3.8 or higher (download from [python.org](https://www.python.org/)).
- On macOS/Linux: Ensure Tkinter is installed. (macOS: `brew install python-tk@3.13` if using Homebrew; Ubuntu: `sudo apt install python3-tk`).

## Installation
1. Clone the repository:

git clone https://github.com/lordvonko/video-downloader.git
cd video-downloader

2. Create and activate a virtual environment (recommended):
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

3. Install dependencies:
pip install -r requirements.txt


## How to Run
1. Run the app:
python video-downloader.py

2. Enter a video URL (e.g., YouTube or TikTok link).
3. Optionally, select a download folder or cookies file (see below for cookies).
4. Click "Download Video" and monitor progress.

## Using Cookies for Logged-In Content
Some sites (e.g., TikTok) require cookies for private videos. Export cookies from your browser:
- Use extensions like "Get cookies.txt LOCALLY" for Brave.  ##USE BRAVE, privacy is power!!!!
- Save as Netscape format (.txt).
- In the app, toggle "Load Cookies File" and select your file.
- More info: [yt-dlp FAQ](https://github.com/yt-dlp/yt-dlp/wiki/FAQ#how-do-i-pass-cookies-to-yt-dlp).

## Troubleshooting:
- **Tkinter not found**: On macOS, reinstall Python with Tkinter support via Homebrew: `brew install python-tk@3.13`.
- **Download errors**: Ensure yt-dlp is up-to-date (`pip install yt-dlp --upgrade`) and check the URL.
- **Slow downloads**: The app uses concurrent fragments for speed, but network issues may vary.

## Contributing
Feel free to fork and submit pull requests! Issues welcome.

## Se quiserem versao portugues é só me pedir!! AQUI é BRASIL!!
