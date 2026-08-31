import os
import json
import re

json_path = r"C:\Users\Kethely\.gemini\antigravity\brain\9dbd3421-ae5c-4f63-9d99-553453c42d0e\scratch\transcript_2026-07-23-23-55-30.json"
out_dir = r"C:\Users\Kethely\.gemini\antigravity\brain\9dbd3421-ae5c-4f63-9d99-553453c42d0e\scratch\minimalist_subs"
os.makedirs(out_dir, exist_ok=True)

with open(json_path, encoding="utf-8") as f:
    data = json.load(f)

segments = data.get("segments", [])

# Let's map target start/end timestamp ranges for each of the 16 videos
cuts = [
    {"num": 1, "name": "video_01", "title": "EU PAGAVA R$ 5 NO CHATGPT", "ss": 462, "t": 48, "card": r"C:\Users\Kethely\.gemini\antigravity\brain\9dbd3421-ae5c-4f63-9d99-553453c42d0e\chatgpt_5reais_minimal_1785067085536.jpg"},
    {"num": 2, "name": "video_02", "title": "72% MAIS BARATO. COMO?", "ss": 753, "t": 45, "card": r"C:\Users\Kethely\.gemini\antigravity\brain\9dbd3421-ae5c-4f63-9d99-553453c42d0e\discount_72_minimal_1785067097059.jpg"},
    {"num": 3, "name": "video_03", "title": "UM EU TESTEI. O OUTRO, NAO.", "ss": 836, "t": 35, "card": None},
    {"num": 4, "name": "video_04", "title": "DE ONDE VEM O PRECO TAO BAIXO?", "ss": 888, "t": 55, "card": r"C:\Users\Kethely\.gemini\antigravity\brain\9dbd3421-ae5c-4f63-9d99-553453c42d0e\cloud_credits_minimal_1785067110367.jpg"},
    {"num": 5, "name": "video_05", "title": "ESSA API E REALMENTE SUA?", "ss": 1001, "t": 50, "card": None},
    {"num": 6, "name": "video_06", "title": "QUANDO O BARATO DEIXA DE COMPENSAR", "ss": 1055, "t": 40, "card": None},
    {"num": 7, "name": "video_07", "title": "VOCE COLOCARIA O CODIGO DA EMPRESA AQUI?", "ss": 1088, "t": 45, "card": None},
    {"num": 8, "name": "video_08", "title": "MEU HOBBY VIROU MEU TRABALHO", "ss": 1417, "t": 50, "card": None},
    {"num": 9, "name": "video_09", "title": "SUA EMPRESA PODE TER ACESSO A ISSO", "ss": 1928, "t": 50, "card": r"C:\Users\Kethely\.gemini\antigravity\brain\9dbd3421-ae5c-4f63-9d99-553453c42d0e\cloud_credits_minimal_1785067110367.jpg"},
    {"num": 10, "name": "video_10", "title": "US$ 5 MIL EM CREDITOS DE IA?", "ss": 2111, "t": 45, "card": r"C:\Users\Kethely\.gemini\antigravity\brain\9dbd3421-ae5c-4f63-9d99-553453c42d0e\cloud_credits_minimal_1785067110367.jpg"},
    {"num": 11, "name": "video_11", "title": "R$ 3 = US$ 100?", "ss": 2290, "t": 55, "card": None},
    {"num": 12, "name": "video_12", "title": "7 MILHOES DE TOKENS POR US$ 2,42?", "ss": 2335, "t": 45, "card": None},
    {"num": 13, "name": "video_13", "title": "O ALMOCO GRATIS VAI ACABAR", "ss": 2950, "t": 42, "card": None},
    {"num": 14, "name": "video_14", "title": "A IA ME ENSINOU A APRENDER", "ss": 3030, "t": 70, "card": None},
    {"num": 15, "name": "video_15", "title": "O QUE PSICOLOGIA TEM A VER COM IA?", "ss": 1896, "t": 45, "card": None},
    {"num": 16, "name": "video_16", "title": "MEU MAIOR ORGULHO AGORA", "ss": 5400, "t": 45, "card": None}
]

def seconds_to_ass_time(sec):
    h = int(sec // 3600)
    m = int((sec % 3600) // 60)
    s = int(sec % 60)
    cs = int(round((sec - int(sec)) * 100))
    if cs >= 100:
        cs = 99
    return f"{h:01d}:{m:02d}:{s:02d}.{cs:02d}"

ass_header = """[Script Info]
Title: Minimalist Subtitles
ScriptType: v4.00+
WrapStyle: 0
ScaledBorderAndShadow: yes
YCbCr Matrix: None
PlayResX: 1080
PlayResY: 1920

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: SubtitleMinimal,Arial,68,&H00FFFFFF,&H0000FFFF,&H00000000,&H80000000,-1,0,0,0,100,100,0,0,1,3,1,2,60,60,320,1
Style: TitleMinimal,Arial,52,&H0000FFFF,&H00FFFFFF,&H00000000,&H90000000,-1,0,0,0,100,100,0,0,1,4,2,8,60,60,1650,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""

for c in cuts:
    cut_start = c["ss"]
    cut_end = c["ss"] + c["t"]
    
    # Filter segments within range
    sub_lines = []
    
    # Add persistent title line at top
    sub_lines.append(f"Dialogue: 0,0:00:00.00,{seconds_to_ass_time(c['t'])},TitleMinimal,,0,0,0,,{c['title']}")
    
    for seg in segments:
        s_start = seg["start"]
        s_end = seg["end"]
        
        if s_end < cut_start or s_start > cut_end:
            continue
        
        # Relativize timestamps
        rel_start = max(0.0, s_start - cut_start)
        rel_end = min(c["t"], s_end - cut_start)
        
        if rel_end - rel_start < 0.2:
            continue
        
        text = seg["text"].strip()
        # Clean text
        text = re.sub(r'[^\w\s\$\%\,\.\!\?\-\:\;\á\é\í\ó\ú\ã\õ\â\ê\ô\ç]', '', text)
        
        if text:
            sub_lines.append(f"Dialogue: 0,{seconds_to_ass_time(rel_start)},{seconds_to_ass_time(rel_end)},SubtitleMinimal,,0,0,0,,{text}")
    
    ass_file = os.path.join(out_dir, f"{c['name']}.ass")
    with open(ass_file, "w", encoding="utf-8") as f:
        f.write(ass_header)
        for line in sub_lines:
            f.write(line + "\n")
    
    print(f"Generated ASS: {ass_file} ({len(sub_lines)} lines)")

print("All ASS subtitle files generated successfully!")
