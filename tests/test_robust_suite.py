import sys
import os
import importlib
import types
from unittest.mock import MagicMock, patch
import pytest

# Insert root path in sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Pre-mock youtube_transcript_api and standard dependencies with valid Exception subclasses
class MockException(Exception):
    pass

mock_yt_api = types.ModuleType('youtube_transcript_api')
mock_yt_api.YouTubeTranscriptApi = MagicMock()
mock_yt_api.TranscriptsDisabled = MockException
mock_yt_api.NoTranscriptFound = MockException
mock_yt_api.VideoIdInvalid = MockException

sys.modules['youtube_transcript_api'] = mock_yt_api

def safe_import(module_name):
    try:
        return importlib.import_module(module_name)
    except ImportError as e:
        missing = e.name
        if not missing:
            parts = str(e).split("'")
            if len(parts) > 1:
                missing = parts[1]
        sys.modules[missing] = MagicMock()
        return importlib.import_module(module_name)

yt_transcript = safe_import('yt_transcript')

def test_module_loaded():
    assert yt_transcript is not None

def test_extract_video_id():
    assert yt_transcript.extract_video_id("https://www.youtube.com/watch?v=dQw4w9WgXcQ") == "dQw4w9WgXcQ"
    assert yt_transcript.extract_video_id("dQw4w9WgXcQ") == "dQw4w9WgXcQ"
    assert yt_transcript.extract_video_id("invalid_url_without_id") is None

def test_format_timestamp():
    assert yt_transcript.format_timestamp(0) == "00:00:00,000"
    assert yt_transcript.format_timestamp(3661.123) == "01:01:01,123"

def test_generate_srt():
    transcript = [{"start": 1.0, "duration": 2.0, "text": "Hello World"}]
    srt = yt_transcript.generate_srt(transcript)
    assert "1" in srt
    assert "00:00:01,000 --> 00:00:03,000" in srt
    assert "Hello World" in srt

def test_main_success(capsys, monkeypatch):
    mock_transcript_obj = MagicMock()
    mock_transcript_obj.fetch.return_value = [{"start": 0.0, "duration": 1.0, "text": "Hello"}]
    mock_yt_api.YouTubeTranscriptApi.list_transcripts.return_value = [mock_transcript_obj]
    
    monkeypatch.setattr(sys, "argv", ["yt_transcript.py", "dQw4w9WgXcQ", "--format", "plain"])
    yt_transcript.main()
        
    captured = capsys.readouterr()
    assert "Hello" in captured.out
