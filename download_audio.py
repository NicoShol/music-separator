
import sys
import yt_dlp
from pathlib import Path

# Check for required URL argument
if len(sys.argv) < 2:
    print("Usage: python download_audio.py <youtube_url> [browser]")
    print("Example: python download_audio.py \"URL\" chrome")
    sys.exit(1)

# The YouTube URL is the first argument
video_urls = [sys.argv[1]]
WD = Path(__file__).parent.resolve()
# Set the base options for the download
ydl_opts = {
    'outtmpl': f'{WD}/input/%(title)s.%(ext)s',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'wav',
    }],
}

print(f"Downloading audio from: {video_urls[0]}")

# Create a YoutubeDL object with the options and download the videos
with yt_dlp.YoutubeDL(ydl_opts) as ydl:
    try:
        ydl.download(video_urls)
        print("Download finished successfully.")
    except Exception as e:
        print(f"An error occurred during download: {e}")
