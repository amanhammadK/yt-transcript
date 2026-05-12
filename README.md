# yt-transcript

Grab any YouTube transcript instantly. No ads, no copy-pasting from the web.

![Python Version](https://img.shields.io/badge/python-3.7+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![PyPI](https://img.shields.io/badge/pypi-v0.1.0-orange.svg)

![demo](demo.gif)

## Installation

1. Install the required library:
   ```bash
   pip install youtube-transcript-api
   ```
2. Download `yt_transcript.py` and make it executable, or copy it to your PATH.
   ```bash
   chmod +x yt_transcript.py
   ```

## Quick Usage

- **Get plain text transcript:**
  ```bash
  yt-transcript https://www.youtube.com/watch?v=dQw4w9WgXcQ
  ```

- **Save as SRT subtitles in a specific language:**
  ```bash
  yt-transcript dQw4w9WgXcQ --lang en --format srt --output transcript.srt
  ```

- **List all available transcript languages:**
  ```bash
  yt-transcript https://youtu.be/dQw4w9WgXcQ --list-langs
  ```

- **Translate a transcript to Spanish:**
  ```bash
  yt-transcript VIDEO_ID --translate es
  ```

## Why?

Because every other online transcript tool is bloated with ads, sign-ups, and slow load times. This is one command, zero bullshit.

## Requirements

- Python 3.7+
- `youtube-transcript-api` library

## License

MIT
