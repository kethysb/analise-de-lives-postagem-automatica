import os
import sys
import subprocess
import json

mkv_path = r"C:\Users\Kethely\Videos\2026-07-23 23-26-35.mkv"
work_dir = r"C:\Users\Kethely\.gemini\antigravity\brain\9dbd3421-ae5c-4f63-9d99-553453c42d0e\scratch"
os.makedirs(work_dir, exist_ok=True)

audio_path = os.path.join(work_dir, "audio_mkv_agency.wav")
output_json = os.path.join(work_dir, "transcript_mkv_agency.json")
output_txt = os.path.join(work_dir, "transcript_mkv_agency.txt")

print(f"1. Extracting audio from MKV {mkv_path}...")
cmd_extract = [
    "ffmpeg", "-y", "-i", mkv_path,
    "-vn", "-acodec", "pcm_s16le", "-ar", "16000", "-ac", "1",
    audio_path
]
subprocess.run(cmd_extract, check=True)
print("Audio extracted successfully!")

print("2. Running Whisper transcription...")
import whisper
model = whisper.load_model("base")
result = model.transcribe(audio_path, verbose=False, language="pt")

print("3. Saving transcription files...")
with open(output_txt, "w", encoding="utf-8") as f:
    for seg in result["segments"]:
        start = seg["start"]
        end = seg["end"]
        text = seg["text"].strip()
        f.write(f"[{start:.2f}s -> {end:.2f}s] {text}\n")

with open(output_json, "w", encoding="utf-8") as f:
    json.dump(result, f, ensure_ascii=False, indent=2)

print(f"Transcription complete! Saved to {output_txt}")
