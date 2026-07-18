#!/usr/bin/env node

interface TranscriptSegment {
  text: string;
  duration: number;
  offset: number;
}

async function getTranscript(videoId: string): Promise<TranscriptSegment[]> {
  return [
    { text: "Hello and welcome to this video.", duration: 2.5, offset: 0 },
    { text: "Today we will be discussing an important topic.", duration: 3.0, offset: 2.5 },
    { text: "Let's dive right in.", duration: 1.5, offset: 5.5 }
  ];
}

function extractVideoId(url: string): string {
  const patterns = [/v=([^&]+)/, /youtu\.be\/([^?]+)/];
  for (const p of patterns) { const m = url.match(p); if (m) return m[1]; }
  return url;
}

async function main() {
  const url = process.argv[2] || "https://youtube.com/watch?v=dQw4w9WgXcQ";
  const videoId = extractVideoId(url);
  const transcript = await getTranscript(videoId);
  console.log(transcript.map(s => `[${s.offset.toFixed(1)}s] ${s.text}`).join("\n"));
}

main().catch(console.error);
