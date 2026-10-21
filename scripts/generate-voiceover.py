import os
import sys
import json
import asyncio
import subprocess
import edge_tts
import edge_tts.constants
import edge_tts.communicate

# Fix Microsoft Edge TTS 403 on cloud runners & local machines
_NEW_WSS = (
    "wss://api.msedgeservices.com/tts/cognitiveservices/websocket/v1"
    f"?Ocp-Apim-Subscription-Key={edge_tts.constants.TRUSTED_CLIENT_TOKEN}"
)
edge_tts.constants.WSS_URL = _NEW_WSS
edge_tts.communicate.WSS_URL = _NEW_WSS

DEFAULT_VOICE = "id-ID-GadisNeural"
DEFAULT_RATE = "-3%"  # Soothing, warm bedtime cadence (~115-120 WPM)

async def synthesize_with_timestamps(text, voice, output_audio_path, rate=DEFAULT_RATE):
    communicate = edge_tts.Communicate(text, voice, rate=rate)
    sentence_boundaries = []
    
    with open(output_audio_path, "wb") as audio_file:
        async for message in communicate.stream():
            if message["type"] == "audio":
                audio_file.write(message["data"])
            elif message["type"] == "SentenceBoundary":
                # offset and duration are in 100-nanosecond ticks
                start_sec = message["offset"] / 10_000_000.0
                dur_sec = message["duration"] / 10_000_000.0
                sentence_boundaries.append({
                    "start": round(start_sec, 3),
                    "end": round(start_sec + dur_sec, 3),
                    "duration": round(dur_sec, 3),
                    "text": message["text"].strip()
                })
    return sentence_boundaries

def split_sentence_into_chunks(sentence_entry, max_words=4):
    text = sentence_entry["text"]
    start = sentence_entry["start"]
    end = sentence_entry["end"]
    total_dur = end - start
    
    words = text.split()
    if not words:
        return []
    
    if len(words) <= max_words:
        return [{
            "start": round(start, 3),
            "end": round(end, 3),
            "text": text
        }]
    
    chunks = []
    current_chunk = []
    for w in words:
        current_chunk.append(w)
        if len(current_chunk) >= max_words:
            chunks.append(" ".join(current_chunk))
            current_chunk = []
    if current_chunk:
        chunks.append(" ".join(current_chunk))
        
    total_chars = sum(len(c) for c in chunks)
    res = []
    cur_time = start
    for c in chunks:
        ratio = len(c) / total_chars if total_chars > 0 else 1.0 / len(chunks)
        c_dur = total_dur * ratio
        res.append({
            "start": round(cur_time, 3),
            "end": round(cur_time + c_dur, 3),
            "text": c
        })
        cur_time += c_dur
        
    return res

def get_audio_duration_ffprobe(file_path):
    try:
        cmd = [
            "ffprobe", "-v", "error", "-show_entries",
            "format=duration", "-of", "default=noprint_wrappers=1:nokey=1", file_path
        ]
        res = subprocess.run(cmd, capture_output=True, text=True, check=True)
        return float(res.stdout.strip())
    except Exception as e:
        print(f"Warning: ffprobe failed ({e}), using fallback estimate")
        return None

def main():
    packet_path = sys.argv[1] if len(sys.argv) > 1 else "curriculum/content_packet_day_001.json"
    output_audio = sys.argv[2] if len(sys.argv) > 2 else "public/voiceover_day_001.mp3"
    meta_output = sys.argv[3] if len(sys.argv) > 3 else "public/audio_meta.json"

    os.makedirs(os.path.dirname(os.path.abspath(output_audio)), exist_ok=True)
    os.makedirs(os.path.dirname(os.path.abspath(meta_output)), exist_ok=True)

    if not os.path.exists(packet_path):
        print(f"Error: Packet not found at {packet_path}")
        sys.exit(1)

    with open(packet_path, "r", encoding="utf-8") as f:
        pkt = json.load(f)

    script_text = (
        pkt.get("verbatim_script_master", {}).get("full_spoken_text_id")
        or pkt.get("script_text")
    )
    if not script_text:
        print("Error: No spoken script found in packet")
        sys.exit(1)

    voice = DEFAULT_VOICE
    print(f"[DITA-04 TTS] Synthesizing bedtime voiceover with {voice} ({len(script_text.split())} words)...")
    
    boundaries = asyncio.run(synthesize_with_timestamps(script_text, voice, output_audio, rate=DEFAULT_RATE))
    
    ff_dur = get_audio_duration_ffprobe(output_audio)
    if ff_dur is None:
        ff_dur = boundaries[-1]["end"] if boundaries else 55.0
        
    fps = 24
    duration_frames = int(round(ff_dur * fps))

    # Generate kinetic subtitle chunks (3-4 words per popup)
    timed_subtitles = []
    for sb in boundaries:
        timed_subtitles.extend(split_sentence_into_chunks(sb, max_words=4))

    meta = {
        "channel_id": "DITA-04",
        "channel_name": pkt.get("metadata", {}).get("channel_name", "Dita Dongeng & Fabel"),
        "channel_handle": pkt.get("metadata", {}).get("handle", "@ditafable"),
        "audio_path": output_audio,
        "voice": voice,
        "rate": DEFAULT_RATE,
        "total_words": len(script_text.split()),
        "duration_seconds": round(ff_dur, 2),
        "duration_frames": duration_frames,
        "fps": fps,
        "sentences": boundaries,
        "timed_subtitles": timed_subtitles
    }

    with open(meta_output, "w", encoding="utf-8") as f:
        json.dump(meta, f, indent=2, ensure_ascii=False)

    print(f"[DITA-04 TTS] Audio successfully created -> {output_audio}")
    print(f"[DITA-04 TTS] Duration: {ff_dur:.2f}s ({duration_frames} frames @ {fps}fps)")
    print(f"[DITA-04 TTS] Subtitle chunks: {len(timed_subtitles)} chunks saved to {meta_output}")

if __name__ == "__main__":
    main()
