import os
import subprocess
import sys

sys.stdout.reconfigure(encoding='utf-8')

src_video = r"C:\Users\Kethely\Videos\2026-07-26-09-28-42.mp4"
out_dir = r"C:\Users\Kethely\Downloads\novos_cortes_editados"
os.makedirs(out_dir, exist_ok=True)

scratch_dir = r"C:\Users\Kethely\.gemini\antigravity\brain\9dbd3421-ae5c-4f63-9d99-553453c42d0e\scratch"
subs_dir = os.path.join(scratch_dir, "minimalist_subs_designer")
os.makedirs(subs_dir, exist_ok=True)

frames_dir = os.path.join(scratch_dir, "frames_verification_designer")
os.makedirs(frames_dir, exist_ok=True)

# ASS Subtitles positioned cleanly at bottom (MarginV=180)
ass_header = """[Script Info]
ScriptType: v4.00+
PlayResX: 1080
PlayResY: 1920
ScaledBorderAndShadow: yes

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Default,Arial,60,&H00FFFFFF,&H000000FF,&H00000000,&H80000000,-1,0,0,0,100,100,0,0,1,3,1,2,60,60,180,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""

videos = [
    {
        "num": 1,
        "name": "01_ia_da_dinheiro_mesmo.mp4",
        "sub": "v01.ass",
        "ss": 1002.0,
        "t": 62.0,
        "line1": "IA DÁ DINHEIRO MESMO?",
        "line2": "",
        "zooms": [(4.0, 14.0), (25.0, 45.0)]
    },
    {
        "num": 2,
        "name": "02_quanto_mais_aprendo_ia_menos_dependo.mp4",
        "sub": "v02.ass",
        "ss": 1104.0,
        "t": 34.0,
        "line1": "QUANTO MAIS APRENDO IA,",
        "line2": "MENOS DEPENDO DELA",
        "zooms": [(3.0, 14.0)]
    },
    {
        "num": 3,
        "name": "03_por_que_ia_responde_generico.mp4",
        "sub": "v03.ass",
        "ss": 1290.0,
        "t": 40.0,
        "line1": "POR QUE SUA IA",
        "line2": "RESPONDE GENÉRICO?",
        "zooms": [(8.0, 25.0)]
    },
    {
        "num": 4,
        "name": "04_nao_procure_uma_profissao_chamada_ia.mp4",
        "sub": "v04.ass",
        "ss": 1463.0,
        "t": 50.0,
        "line1": "NÃO PROCURE UMA PROFISSÃO",
        "line2": "CHAMADA 'IA'",
        "zooms": [(15.0, 35.0)]
    },
    {
        "num": 5,
        "name": "05_nota_alta_nao_e_o_mesmo_que_aprender.mp4",
        "sub": "v05.ass",
        "ss": 1620.0,
        "t": 60.0,
        "line1": "NOTA ALTA NÃO É O MESMO",
        "line2": "QUE APRENDER",
        "zooms": [(20.0, 30.0), (52.0, 60.0)]
    },
    {
        "num": 6,
        "name": "06_o_pior_jeito_de_prospectar_empresas.mp4",
        "sub": "v06.ass",
        "ss": 162.0,
        "t": 38.0,
        "line1": "O PIOR JEITO DE PROSPECTAR",
        "line2": "EMPRESAS NOVAS",
        "zooms": [(12.0, 28.0)]
    },
    {
        "num": 7,
        "name": "07_por_que_parei_de_construir_do_zero.mp4",
        "sub": "v07.ass",
        "ss": 1720.0,
        "t": 26.0,
        "line1": "POR QUE PAREI DE CONSTRUIR",
        "line2": "TUDO DO ZERO",
        "zooms": [(10.0, 23.0)]
    },
    {
        "num": 8,
        "name": "08_por_que_computer_use_ainda_erra_tanto.mp4",
        "sub": "v08.ass",
        "ss": 1746.0,
        "t": 65.0,
        "line1": "POR QUE COMPUTER USE",
        "line2": "AINDA ERRA TANTO?",
        "zooms": [(15.0, 30.0), (48.0, 65.0)]
    }
]

import json
json_path = os.path.join(scratch_dir, "transcript_2026-07-26-09-28-42.json")
with open(json_path, 'r', encoding='utf-8') as f:
    transcript_data = json.load(f)
segments = transcript_data.get('segments', [])

def to_ass_time(seconds):
    ms = int((seconds - int(seconds)) * 100)
    m, s = divmod(int(seconds), 60)
    h, m = divmod(m, 60)
    return f"{h:01d}:{m:02d}:{s:02d}.{ms:02d}"

print("Building Subtitles for Designer Layout...")
for v in videos:
    v_ss = v["ss"]
    v_to = v_ss + v["t"]
    out_ass = os.path.join(subs_dir, v["sub"])
    
    event_lines = []
    for seg in segments:
        s_start = seg['start']
        s_end = seg['end']
        text = seg['text'].strip()
        
        if s_end >= v_ss and s_start <= v_to:
            rel_start = max(0.0, s_start - v_ss)
            rel_end = min(v["t"], s_end - v_ss)
            
            if rel_end - rel_start > 0.2 and text:
                words = text.split()
                if len(words) > 6:
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

print("Rendering 8 Videos with Designer Wrapped Titles (No Text Cutoff)...")

for v in videos:
    out_path = os.path.join(out_dir, v["name"])
    ass_path = os.path.join(subs_dir, v["sub"]).replace("\\", "/")
    ass_escaped = ass_path.replace(":", "\\:")
    
    l1 = v["line1"].replace("'", "").replace("\"", "")
    l2 = v["line2"].replace("'", "").replace("\"", "")
    
    print(f"\n[{v['num']}/8] Rendering Designer Video: {v['name']}")
    
    vf_chain = [
        "crop=ih*9/16:ih:(iw-ih*9/16)/2:0",
        "scale=1080:1920"
    ]
    
    if v["zooms"]:
        zoom_exprs = [f"between(t,{zs},{ze})" for zs, ze in v["zooms"]]
        cond_zoom = "+".join(zoom_exprs)
        vf_chain.append(
            f"scale=eval=frame:w='if({cond_zoom}, 1188, 1080)':h='if({cond_zoom}, 2112, 1920)',crop=1080:1920"
        )
    
    # Designer Card Banner (Positioned right below split y=740, Height: 150px)
    # Double-line text formatting so 100% of title fits comfortably on screen
    if l2:
        vf_chain.append("drawbox=x=80:y=730:w=920:h=150:color=black@0.85:t=fill")
        vf_chain.append("drawbox=x=76:y=726:w=928:h=158:color=white@0.3:t=2")
        vf_chain.append(
            f"drawtext=fontfile='C\\:/Windows/Fonts/arialbd.ttf':text='{l1}':fontcolor=white:fontsize=38:x=(w-text_w)/2:y=755"
        )
        vf_chain.append(
            f"drawtext=fontfile='C\\:/Windows/Fonts/arialbd.ttf':text='{l2}':fontcolor=white:fontsize=38:x=(w-text_w)/2:y=810"
        )
    else:
        vf_chain.append("drawbox=x=120:y=740:w=840:h=110:color=black@0.85:t=fill")
        vf_chain.append("drawbox=x=116:y=736:w=848:h=118:color=white@0.3:t=2")
        vf_chain.append(
            f"drawtext=fontfile='C\\:/Windows/Fonts/arialbd.ttf':text='{l1}':fontcolor=white:fontsize=40:x=(w-text_w)/2:y=773"
        )
    
    # ASS Subtitles
    vf_chain.append(f"subtitles='{ass_escaped}'")
    
    vf_str = ",".join(vf_chain)
    
    cmd = [
        "ffmpeg", "-y",
        "-ss", str(v["ss"]),
        "-i", src_video,
        "-t", str(v["t"]),
        "-vf", vf_str,
        "-af", "loudnorm=I=-16:TP=-1.5:LRA=11",
        "-c:v", "libx264", "-preset", "fast", "-crf", "18",
        "-c:a", "aac", "-b:a", "192k",
        out_path
    ]
    
    res = subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    if res.returncode == 0 and os.path.exists(out_path):
        mb = round(os.path.getsize(out_path)/(1024*1024), 2)
        print(f"DESIGNER SUCCESS: {v['name']} ({mb} MB)")
        
        # Extract verification frame at 3 seconds
        frame_jpg = os.path.join(frames_dir, f"v{v['num']:02d}_designer.jpg")
        subprocess.run([
            "ffmpeg", "-y", "-ss", "3", "-i", out_path, "-vframes", "1", frame_jpg
        ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

print("\nALL 8 VIDEOS RENDERED WITH DESIGNER WRAPPED TITLES & NO TEXT CUTOFF!")
