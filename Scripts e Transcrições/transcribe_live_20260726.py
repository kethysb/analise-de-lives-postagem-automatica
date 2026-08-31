import os
import subprocess
import sys
import json

sys.stdout.reconfigure(encoding='utf-8')

video_path = r"C:\Users\Kethely\Videos\2026-07-26-09-28-42.mp4"
scratch_dir = r"C:\Users\Kethely\.gemini\antigravity\brain\9dbd3421-ae5c-4f63-9d99-553453c42d0e\scratch"
audio_path = os.path.join(scratch_dir, "audio_2026-07-26-09-28-42.wav")
json_output_path = os.path.join(scratch_dir, "transcript_2026-07-26-09-28-42.json")
txt_output_path = os.path.join(scratch_dir, "transcript_2026-07-26-09-28-42.txt")
md_output_path = os.path.join(scratch_dir, "transcricao_completa_2026-07-26-09-28-42.md")

print(f"Target Video File: {video_path}")
if not os.path.exists(video_path):
    print(f"ERROR: File not found: {video_path}")
    sys.exit(1)

# Step 1: Extract Audio via FFmpeg if not already extracted
if not os.path.exists(audio_path) or os.path.getsize(audio_path) < 1000:
    print("\n[Step 1/3] Extracting 16kHz mono audio via FFmpeg...")
    cmd_ffmpeg = [
        "ffmpeg", "-y",
        "-i", video_path,
        "-vn",
        "-ac", "1",
        "-ar", "16000",
        "-c:a", "pcm_s16le",
        audio_path
    ]
    res = subprocess.run(cmd_ffmpeg, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)
    if res.returncode != 0:
        print("FFmpeg Error:", res.stderr.decode('utf-8', errors='ignore'))
        sys.exit(1)
    print(f"Audio extracted successfully: {audio_path} ({round(os.path.getsize(audio_path)/(1024*1024), 2)} MB)")
else:
    print(f"\n[Step 1/3] Audio already extracted at: {audio_path}")

# Step 2: Transcribe via Whisper
print("\n[Step 2/3] Loading Whisper model and starting Portuguese transcription...")

import whisper

# Load medium/small model for best accuracy on Portuguese speech
model = whisper.load_model("small")

print("Transcribing 3-hour audio file... (this may take a few minutes)")
result = model.transcribe(audio_path, language="pt", verbose=False)

segments = result.get("segments", [])
full_text = result.get("text", "")

print(f"\nTranscription complete! Generated {len(segments)} segments.")

# Step 3: Save outputs
print("\n[Step 3/3] Saving outputs to JSON, TXT, and Markdown files...")

# Save JSON
with open(json_output_path, "w", encoding="utf-8") as f:
    json.dump(result, f, ensure_ascii=False, indent=2)

# Save TXT
with open(txt_output_path, "w", encoding="utf-8") as f:
    f.write(full_text)

# Save MD with timestamps
def fmt_time(seconds):
    m, s = divmod(int(seconds), 60)
    h, m = divmod(m, 60)
    if h > 0:
        return f"{h:02d}:{m:02d}:{s:02d}"
    return f"{m:02d}:{s:02d}"

md_lines = [
    "# 🎙️ TRANSCRIÇÃO COMPLETA DA LIVE — 2026-07-26 (3 HORAS)",
    "",
    f"* **Arquivo Origem**: `C:\\Users\\Kethely\\Videos\\2026-07-26-09-28-42.mp4`",
    f"* **Total de Segmentos**: {len(segments)}",
    "",
    "---",
    "",
    "## 📄 TRANSCRIÇÃO LITERÁRIA COM TIMESTAMPS",
    ""
]

current_block = []
current_start = 0

for seg in segments:
    start_t = fmt_time(seg['start'])
    end_t = fmt_time(seg['end'])
    text = seg['text'].strip()
    
    md_lines.append(f"**[{start_t} -> {end_t}]** {text}\n")

with open(md_output_path, "w", encoding="utf-8") as f:
    f.write("\n".join(md_lines))

print(f"\nSUCCESS! All transcription files saved:")
print(f" - Markdown: {md_output_path}")
print(f" - JSON: {json_output_path}")
print(f" - TXT: {txt_output_path}")
