import os
import subprocess
import sys

sys.stdout.reconfigure(encoding='utf-8')

src_video = r"C:\Users\Kethely\Videos\2026-07-26-09-28-42.mp4"
out_dir = r"C:\Users\Kethely\Downloads\novos_cortes_editados"
os.makedirs(out_dir, exist_ok=True)

scratch_dir = r"C:\Users\Kethely\.gemini\antigravity\brain\9dbd3421-ae5c-4f63-9d99-553453c42d0e\scratch"
subs_dir = os.path.join(scratch_dir, "minimalist_subs_centered")
os.makedirs(subs_dir, exist_ok=True)

frames_dir = os.path.join(scratch_dir, "frames_verification")
os.makedirs(frames_dir, exist_ok=True)

# Generate centered ASS subtitles with larger font size (68pt) and balanced margins
ass_header = """[Script Info]
ScriptType: v4.00+
PlayResX: 1080
PlayResY: 1920
ScaledBorderAndShadow: yes

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Default,Arial,68,&H00FFFFFF,&H000000FF,&H00000000,&H80000000,-1,0,0,0,100,100,0,0,1,3,1,2,60,60,420,1

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
        "title": "IA DÁ DINHEIRO MESMO?",
        "zooms": [(4.0, 14.0), (25.0, 45.0)],
        "cards": [
            {"s": 0, "e": 4, "text": "💬 'Dá para ganhar bem com esse conhecimento?'"},
            {"s": 14, "e": 25, "text": "⚡ 2 DIAS  ➞  10 MINUTOS"}
        ]
    },
    {
        "num": 2,
        "name": "02_quanto_mais_aprendo_ia_menos_dependo.mp4",
        "sub": "v02.ass",
        "ss": 1104.0,
        "t": 34.0,
        "title": "QUANTO MAIS APRENDO IA, MENOS DEPENDO DELA",
        "zooms": [(3.0, 14.0)],
        "cards": [
            {"s": 3, "e": 14, "text": "📌 O almoço grátis não vai ser para sempre"},
            {"s": 14, "e": 28, "text": "💡 IA para construir  •  Automação para manter"}
        ]
    },
    {
        "num": 3,
        "name": "03_por_que_ia_responde_generico.mp4",
        "sub": "v03.ass",
        "ss": 1290.0,
        "t": 40.0,
        "title": "POR QUE SUA IA RESPONDE GENÉRICO?",
        "zooms": [(8.0, 25.0)],
        "cards": [
            {"s": 0, "e": 5, "text": "❌ Prompt vago = Resposta genérica"},
            {"s": 8, "e": 25, "text": "🎯 Objetivo  •  Contexto  •  Limites"}
        ]
    },
    {
        "num": 4,
        "name": "04_nao_procure_uma_profissao_chamada_ia.mp4",
        "sub": "v04.ass",
        "ss": 1463.0,
        "t": 50.0,
        "title": "NÃO PROCURE UMA PROFISSÃO CHAMADA 'IA'",
        "zooms": [(15.0, 35.0)],
        "cards": [
            {"s": 3, "e": 15, "text": "💻 Programação  •  📊 Dados  •  🚀 Marketing"},
            {"s": 35, "e": 50, "text": "💡 IA + Área Real = Habilidade Única"}
        ]
    },
    {
        "num": 5,
        "name": "05_nota_alta_nao_e_o_mesmo_que_aprender.mp4",
        "sub": "v05.ass",
        "ss": 1620.0,
        "t": 60.0,
        "title": "NOTA ALTA NÃO É O MESMO QUE APRENDER",
        "zooms": [(20.0, 30.0), (52.0, 60.0)],
        "cards": [
            {"s": 0, "e": 8, "text": "📊 Exercícios inteligentes com IA"},
            {"s": 20, "e": 30, "text": "🚨 NOTA  ≠  COMPREENSÃO REAL"}
        ]
    },
    {
        "num": 6,
        "name": "06_o_pior_jeito_de_prospectar_empresas.mp4",
        "sub": "v06.ass",
        "ss": 162.0,
        "t": 38.0,
        "title": "O PIOR JEITO DE PROSPECTAR EMPRESAS NOVAS",
        "zooms": [(12.0, 28.0)],
        "cards": [
            {"s": 3, "e": 12, "text": "🏢 Empresa Nova ➞ Possível Cliente"},
            {"s": 12, "e": 28, "text": "📩 Prospecção sem contexto vira spam"}
        ]
    },
    {
        "num": 7,
        "name": "07_por_que_parei_de_construir_do_zero.mp4",
        "sub": "v07.ass",
        "ss": 1720.0,
        "t": 26.0,
        "title": "POR QUE PAREI DE CONSTRUIR TUDO DO ZERO",
        "zooms": [(10.0, 23.0)],
        "cards": [
            {"s": 10, "e": 23, "text": "🛠️ Agent Zero: Base aberta e personalizável"}
        ]
    },
    {
        "num": 8,
        "name": "08_por_que_computer_use_ainda_erra_tanto.mp4",
        "sub": "v08.ass",
        "ss": 1746.0,
        "t": 65.0,
        "title": "POR QUE COMPUTER USE AINDA ERRA TANTO?",
        "zooms": [(15.0, 30.0), (48.0, 65.0)],
        "cards": [
            {"s": 15, "e": 30, "text": "⚠️ Cliques em coordenadas são frágeis"},
            {"s": 48, "e": 65, "text": "⚡ Menos cliques visuais  •  Mais comandos estruturados"}
        ]
    }
]

# Generate large centered ASS subtitles
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

print("Building Large & Centered ASS Subtitles...")
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
                if len(words) > 5:
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

print("Rendering 8 Videos with Large & Centered Typography...")

for v in videos:
    out_path = os.path.join(out_dir, v["name"])
    ass_path = os.path.join(subs_dir, v["sub"]).replace("\\", "/")
    ass_escaped = ass_path.replace(":", "\\:")
    title_text = v["title"].replace("'", "").replace("\"", "")
    
    print(f"\n[{v['num']}/8] Rendering Large & Centered Video: {v['name']}")
    
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
    
    # Larger, Centered Title Banner (Height: 140px, Fontsize: 46pt)
    vf_chain.append("drawbox=y=130:h=140:color=black@0.85:t=fill")
    vf_chain.append(
        f"drawtext=fontfile='C\\:/Windows/Fonts/arialbd.ttf':text='{title_text}':fontcolor=white:fontsize=46:x=(w-text_w)/2:y=175"
    )
    
    # Larger, Centered Card Overlays (Height: 100px, Fontsize: 40pt)
    for card in v["cards"]:
        c_txt = card["text"].replace("'", "").replace("\"", "")
        cs = card["s"]
        ce = card["e"]
        vf_chain.append(
            f"drawbox=y=380:h=100:color=black@0.80:t=fill:enable='between(t,{cs},{ce})'"
        )
        vf_chain.append(
            f"drawtext=fontfile='C\\:/Windows/Fonts/arial.ttf':text='{c_txt}':fontcolor=white:fontsize=40:x=(w-text_w)/2:y=410:enable='between(t,{cs},{ce})'"
        )
    
    # Large Subtitles
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
        print(f"LARGE & CENTERED SUCCESS: {v['name']} ({mb} MB)")
        
        # Extract verification frame at 5 seconds
        frame_jpg = os.path.join(frames_dir, f"v{v['num']:02d}_frame.jpg")
        subprocess.run([
            "ffmpeg", "-y", "-ss", "5", "-i", out_path, "-vframes", "1", frame_jpg
        ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        print(f"Extracted verification frame: {frame_jpg}")

print("\nALL 8 VIDEOS RENDERED WITH LARGE & CENTERED TYPOGRAPHY + FRAMES EXTRACTED!")
