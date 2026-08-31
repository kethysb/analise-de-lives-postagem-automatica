import os
import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

scratch_dir = r"C:\Users\Kethely\.gemini\antigravity\brain\9dbd3421-ae5c-4f63-9d99-553453c42d0e\scratch"
subs_dir = os.path.join(scratch_dir, "minimalist_subs_8vids")
os.makedirs(subs_dir, exist_ok=True)

json_path = os.path.join(scratch_dir, "transcript_2026-07-26-09-28-42.json")

with open(json_path, 'r', encoding='utf-8') as f:
    data = json.load(f)

segments = data.get('segments', [])

videos_def = [
    {"num": 1, "filename": "v01.ass", "ss": 1002.0, "to": 1064.0},
    {"num": 2, "filename": "v02.ass", "ss": 1104.0, "to": 1138.0},
    {"num": 3, "filename": "v03.ass", "ss": 1290.0, "to": 1330.0},
    {"num": 4, "filename": "v04.ass", "ss": 1463.0, "to": 1513.0},
    {"num": 5, "filename": "v05.ass", "ss": 1620.0, "to": 1680.0},
    {"num": 6, "filename": "v06.ass", "ss": 162.0, "to": 200.0},
    {"num": 7, "filename": "v07.ass", "ss": 1720.0, "to": 1746.0},
    {"num": 8, "filename": "v08.ass", "ss": 1746.0, "to": 1811.0}
]

ass_header = """[Script Info]
ScriptType: v4.00+
PlayResX: 1080
PlayResY: 1920
ScaledBorderAndShadow: yes

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Default,Arial,54,&H00FFFFFF,&H000000FF,&H00000000,&H80000000,-1,0,0,0,100,100,0,0,1,3,0,2,80,80,320,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""

def to_ass_time(seconds):
    ms = int((seconds - int(seconds)) * 100)
    m, s = divmod(int(seconds), 60)
    h, m = divmod(m, 60)
    return f"{h:01d}:{m:02d}:{s:02d}.{ms:02d}"

for v in videos_def:
    v_ss = v["ss"]
    v_to = v["to"]
    out_ass = os.path.join(subs_dir, v["filename"])
    
    event_lines = []
    for seg in segments:
        s_start = seg['start']
        s_end = seg['end']
        text = seg['text'].strip()
        
        if s_end >= v_ss and s_start <= v_to:
            rel_start = max(0.0, s_start - v_ss)
            rel_end = min(v_to - v_ss, s_end - v_ss)
            
            if rel_end - rel_start > 0.2 and text:
                # Wrap text to max 2 lines
                words = text.split()
                if len(words) > 7:
                    mid = len(words) // 2
                    line1 = " ".join(words[:mid])
                    line2 = " ".join(words[mid:])
                    wrapped_text = f"{line1}\\N{line2}"
                else:
                    wrapped_text = text
                
                t_start = to_ass_time(rel_start)
                t_end = to_ass_time(rel_end)
                event_lines.append(f"Dialogue: 0,{t_start},{t_end},Default,,0,0,0,,{wrapped_text}")
    
    with open(out_ass, "w", encoding="utf-8") as f:
        f.write(ass_header + "\n".join(event_lines) + "\n")
    
    print(f"Generated subtitle {v['filename']} with {len(event_lines)} lines.")

print("All 8 ASS subtitle files generated successfully!")
