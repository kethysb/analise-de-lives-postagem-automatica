import os
import subprocess
import sys

sys.stdout.reconfigure(encoding='utf-8')

src_video = r"C:\Users\Kethely\Videos\2026-07-26-09-28-42.mp4"
scratch_dir = r"C:\Users\Kethely\.gemini\antigravity\brain\9dbd3421-ae5c-4f63-9d99-553453c42d0e\scratch"
framing_dir = os.path.join(scratch_dir, "framing_analysis")
os.makedirs(framing_dir, exist_ok=True)

# Sample times (in seconds) across the 8 videos
sample_times = [
    {"v": "V1", "t": 1010}, # 16:50
    {"v": "V2", "t": 1115}, # 18:35
    {"v": "V3", "t": 1300}, # 21:40
    {"v": "V4", "t": 1475}, # 24:35
    {"v": "V5", "t": 1635}, # 27:15
    {"v": "V6", "t": 175},  # 02:55
    {"v": "V7", "t": 1730}, # 28:50
    {"v": "V8", "t": 1760}  # 29:20
]

print("Extracting test frames for framing analysis...")

for item in sample_times:
    v_name = item["v"]
    t_sec = item["t"]
    
    # 1. Full raw frame
    raw_jpg = os.path.join(framing_dir, f"{v_name}_raw.jpg")
    subprocess.run(["ffmpeg", "-y", "-ss", str(t_sec), "-i", src_video, "-vframes", "1", raw_jpg], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    
    # 2. Vertical 9:16 crop from top (y=0)
    crop_top = os.path.join(framing_dir, f"{v_name}_crop_top.jpg")
    vf_top = "crop=ih*9/16:ih:(iw-ih*9/16)/2:0,scale=1080:1920"
    subprocess.run(["ffmpeg", "-y", "-ss", str(t_sec), "-i", src_video, "-vf", vf_top, "-vframes", "1", crop_top], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    
    # 3. Vertical 9:16 crop from bottom (y=ih-ih)
    print(f"Extracted frames for {v_name} at t={t_sec}s")

print(f"Framing analysis complete! Frames saved to: {framing_dir}")
