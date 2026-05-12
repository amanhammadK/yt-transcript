#!/usr/bin/env python3
"""
yt-transcript: Grab any YouTube transcript instantly.
"""

import sys
import argparse
import re
import json
from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled, NoTranscriptFound, VideoIdInvalid

def extract_video_id(url_or_id):
    """Extracts the video ID from a YouTube URL or returns the ID if it matches the format."""
    patterns = [
        r'(?:v=|\/)([0-9A-Za-z_-]{11}).*',
        r'(?:embed\/|v\/|shorts\/|youtu\.be\/)([0-9A-Za-z_-]{11})',
        r'^([0-9A-Za-z_-]{11})$'
    ]
    for pattern in patterns:
        match = re.search(pattern, url_or_id)
        if match:
            return match.group(1)
    return None

def format_timestamp(seconds):
    """Formats seconds into SRT timestamp format (HH:MM:SS,mmm)."""
    milliseconds = int((seconds % 1) * 1000)
    seconds = int(seconds)
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    return f"{hours:02d}:{minutes:02d}:{seconds:02d},{milliseconds:03d}"

def generate_srt(transcript):
    """Generates SRT formatted subtitles from transcript list."""
    srt_output = []
    for i, entry in enumerate(transcript, 1):
        start = entry['start']
        duration = entry['duration']
        end = start + duration
        text = entry['text'].replace('\n', ' ').strip()
        
        srt_output.append(f"{i}")
        srt_output.append(f"{format_timestamp(start)} --> {format_timestamp(end)}")
        srt_output.append(text)
        srt_output.append("")
    return "\n".join(srt_output)

def main():
    parser = argparse.ArgumentParser(description="Grab any YouTube transcript instantly.")
    parser.add_argument("url_or_id", help="YouTube video URL or video ID")
    parser.add_argument("--lang", help="Language code(s), e.g. 'en', 'en-GB'. Default: first available.")
    parser.add_argument("--translate", metavar="LANG", help="Translate transcript to another language (e.g. 'es')")
    parser.add_argument("--output", metavar="FILENAME", help="Save transcript to file instead of printing to stdout")
    parser.add_argument("--format", choices=['plain', 'json', 'srt', 'text'], default='plain', help="Output format (default: plain)")
    parser.add_argument("--list-langs", action="store_true", help="List available transcript languages and exit")

    args = parser.parse_args()

    video_id = extract_video_id(args.url_or_id)
    if not video_id:
        print(f"Error: Invalid YouTube URL or Video ID: {args.url_or_id}", file=sys.stderr)
        sys.exit(1)

    try:
        transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)

        if args.list_langs:
            print(f"Available transcripts for video '{video_id}':")
            for t in transcript_list:
                status = "manual" if not t.is_generated else "auto"
                print(f"- {t.language_code} ({t.language}) [{status}]")
            sys.exit(0)

        # Determine which transcript to fetch
        if args.lang:
            # find_transcript returns a Transcript object
            transcript_obj = transcript_list.find_transcript([args.lang])
        else:
            # Get the first available transcript
            transcript_obj = next(iter(transcript_list))

        # Handle translation if requested
        if args.translate:
            try:
                transcript_data = transcript_obj.translate(args.translate).fetch()
            except Exception as e:
                print(f"Error: Translation to '{args.translate}' failed: {e}", file=sys.stderr)
                sys.exit(1)
        else:
            transcript_data = transcript_obj.fetch()

        # Format the output
        output_content = ""
        if args.format == 'json':
            output_content = json.dumps(transcript_data, indent=2, ensure_ascii=False)
        elif args.format == 'srt':
            output_content = generate_srt(transcript_data)
        elif args.format == 'text':
            output_content = " ".join([entry['text'].replace('\n', ' ') for entry in transcript_data])
        else: # plain
            output_content = "\n".join([entry['text'] for entry in transcript_data])

        # Output handling
        if args.output:
            with open(args.output, 'w', encoding='utf-8') as f:
                f.write(output_content)
            print(f"Saved transcript to {args.output}", file=sys.stderr)
        else:
            print(output_content)

    except VideoIdInvalid:
        print(f"Error: Video ID '{video_id}' is invalid.", file=sys.stderr)
        sys.exit(1)
    except TranscriptsDisabled:
        print(f"Error: Transcripts are disabled for video '{video_id}'.", file=sys.stderr)
        sys.exit(1)
    except NoTranscriptFound:
        print(f"Error: No transcript found for video '{video_id}'.", file=sys.stderr)
        # Suggest listing languages
        print(f"Try running with --list-langs to see available languages.", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"An unexpected error occurred: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
