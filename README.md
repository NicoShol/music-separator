To convert a youtube URL to .wav

```
music_separator/venv/lib/python3.9/site-packages/yt_dlp -x --audio-format wav -o 'input/%(title)s.%(ext)s' $YOUTUBE_URL
```