import os
import sys
import json
import subprocess

video_src = r"C:\Users\Kethely\Videos\2026-07-23-23-55-30.mp4"
transcript_json = r"C:\Users\Kethely\.gemini\antigravity\brain\9dbd3421-ae5c-4f63-9d99-553453c42d0e\scratch\transcript_2026-07-23-23-55-30.json"
out_dir = r"C:\Users\Kethely\Downloads"
scratch_dir = r"C:\Users\Kethely\.gemini\antigravity\brain\9dbd3421-ae5c-4f63-9d99-553453c42d0e\scratch"

with open(transcript_json, encoding="utf-8") as f:
    data = json.load(f)

segments = data.get("segments", [])

cuts_def = [
    {
        "id": "corte_01_chatgpt_5reais_gringo",
        "title": "Como paguei R$ 5,00 no ChatGPT Pro em site gringo",
        "start": 280.0,
        "end": 340.0
    },
    {
        "id": "corte_02_banimento_contas_chatgpt",
        "title": "Por que o ChatGPT esta banindo contas pelo mundo",
        "start": 340.0,
        "end": 435.0
    },
    {
        "id": "corte_03_plataforma_apis_baratas",
        "title": "Descobri a plataforma mais barata de APIs de IA",
        "start": 460.0,
        "end": 550.0
    },
    {
        "id": "corte_04_72porcento_desconto_gemini_gpt4",
        "title": "72% de Desconto Oficial em APIs do Gemini e GPT-4",
        "start": 700.0,
        "end": 790.0
    },
    {
        "id": "corte_05_psicologia_para_programacao_ia",
        "title": "Abandonei a Psicologia para viver de IA e Programacao",
        "start": 3075.0,
        "end": 3180.0
    }
]

def seconds_to_ass_time(s):
    h = int(s // 3600)
    m = int((s % 3600) // 60)
    sec = int(s % 60)
    cs = int(round((s - int(s)) * 100))
    if cs >= 100:
        cs = 99
    return f"{h}:{m:02d}:{sec:02d}.{cs:02d}"

ass_header = """[Script Info]
Title: Wendell Preset Captions
ScriptType: v4.00+
WrapStyle: 0
ScaledBorderAndShadow: yes
YCbCr Matrix: None

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Default,Arial,18,&H00FFFFFF,&H0000FFFF,&H00000000,&H80000000,-1,0,0,0,100,100,0,0,1,3,2,2,10,10,120,1
Style: Highlight,Arial,20,&H0000FFFF,&H0000FFFF,&H00000000,&H80000000,-1,0,0,0,100,100,0,0,1,4,3,2,10,10,120,1
Style: TitleHeader,Arial,22,&H0000E6FF,&H0000E6FF,&H00000000,&H90000000,-1,0,0,0,100,100,0,0,1,3,3,8,10,10,40,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""

for cut in cuts_def:
    cut_id = cut["id"]
    cut_title = cut["title"]
    start_sec = cut["start"]
    end_sec = cut["end"]
    duration = end_sec - start_sec

    print(f"=== Rendering {cut_id} ({duration}s) ===")
    
    # 1. Filter matching whisper segments
    cut_segments = [s for s in segments if s["start"] >= start_sec - 1.0 and s["end"] <= end_sec + 1.0]
    
    # 2. Build ASS file
    ass_path = os.path.join(scratch_dir, f"{cut_id}.ass")
    with open(ass_path, "w", encoding="utf-8") as f_ass:
        f_ass.write(ass_header)
        
        # Add Title Header at top of screen throughout video
        t_start_ass = seconds_to_ass_time(0.0)
        t_end_ass = seconds_to_ass_time(duration)
        f_ass.write(f"Dialogue: 0,{t_start_ass},{t_end_ass},TitleHeader,,0,0,0,,{{\\b1\\c&H0000FFFF&}}{cut_title.upper()}{{\\b0}}\n")
        
        for seg in cut_segments:
            seg_rel_start = max(0.0, seg["start"] - start_sec)
            seg_rel_end = min(duration, seg["end"] - start_sec)
            if seg_rel_end <= seg_rel_start:
                continue
            
            s_str = seconds_to_ass_time(seg_rel_start)
            e_str = seconds_to_ass_time(seg_rel_end)
            text = seg["text"].strip()
            if text:
                f_ass.write(f"Dialogue: 0,{s_str},{e_str},Default,,0,0,0,,{text}\n")
    
    # 3. FFmpeg crop to vertical 9:16 + burn ASS subtitles + loudnorm audio
    out_mp4 = os.path.join(out_dir, f"{cut_id}.mp4")
    ass_escaped = ass_path.replace("\\", "/").replace(":", "\\:")
    
    # Crop filter: crop 1080:1920:in_w/2-540:0 for 9:16 vertical crop
    vf_chain = f"crop=ih*9/16:ih:(iw-ih*9/16)/2:0,scale=1080:1920,subtitles='{ass_escaped}'"
    
    cmd_ffmpeg = [
        "ffmpeg", "-y",
        "-ss", str(start_sec),
        "-i", video_src,
        "-t", str(duration),
        "-vf", vf_chain,
        "-af", "loudnorm=I=-16:TP=-1.5:LRA=11",
        "-c:v", "libx264", "-preset", "fast", "-crf", "22",
        "-c:a", "aac", "-b:a", "192k",
        out_mp4
    ]
    
    try:
        subprocess.run(cmd_ffmpeg, check=True)
        print(f"SUCCESS: Created {out_mp4}")
    except Exception as e:
        print(f"ERROR rendering {cut_id}: {e}")

print("All cuts rendered successfully!")
