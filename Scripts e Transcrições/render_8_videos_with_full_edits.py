import os
import subprocess
import sys

sys.stdout.reconfigure(encoding='utf-8')

src_video = r"C:\Users\Kethely\Videos\2026-07-26-09-28-42.mp4"
out_dir = r"C:\Users\Kethely\Downloads\novos_cortes_editados"
os.makedirs(out_dir, exist_ok=True)

scratch_dir = r"C:\Users\Kethely\.gemini\antigravity\brain\9dbd3421-ae5c-4f63-9d99-553453c42d0e\scratch"
subs_dir = os.path.join(scratch_dir, "minimalist_subs_8vids")

# Video definitions with exact Titles, Overlay Text Prompts & Timestamps
videos = [
    {
        "num": 1,
        "name": "01_ia_da_dinheiro_mesmo.mp4",
        "sub": "v01.ass",
        "ss": 1002.0,
        "t": 62.0,
        "title": "IA DÁ DINHEIRO MESMO?",
        "overlays": [
            {"start": 0, "end": 4, "text": "💬 'Dá para ganhar bem com esse conhecimento todo?'"},
            {"start": 4, "end": 14, "text": "📍 1 ano e meio atuando na área"},
            {"start": 14, "end": 25, "text": "⚡ 2 DIAS  ➡️  10 MINUTOS"}
        ]
    },
    {
        "num": 2,
        "name": "02_quanto_mais_aprendo_ia_menos_dependo.mp4",
        "sub": "v02.ass",
        "ss": 1104.0,
        "t": 34.0,
        "title": "QUANTO MAIS APRENDO IA, MENOS DEPENDO DELA",
        "overlays": [
            {"start": 3, "end": 14, "text": "⚠️ 'O almoço está de graça, mas NÃO vai ser para sempre.'"},
            {"start": 14, "end": 28, "text": "⚙️ IA = Construir | Automação = Manter"}
        ]
    },
    {
        "num": 3,
        "name": "03_por_que_ia_responde_generico.mp4",
        "sub": "v03.ass",
        "ss": 1290.0,
        "t": 40.0,
        "title": "POR QUE SUA IA RESPONDE GENÉRICO?",
        "overlays": [
            {"start": 0, "end": 5, "text": "❌ Prompt Amplo: 'Faça uma estratégia de marketing'"},
            {"start": 8, "end": 25, "text": "🎯 Objetivo + Contexto + Referências + Limites"}
        ]
    },
    {
        "num": 4,
        "name": "04_nao_procure_uma_profissao_chamada_ia.mp4",
        "sub": "v04.ass",
        "ss": 1463.0,
        "t": 50.0,
        "title": "NÃO PROCURE UMA PROFISSÃO CHAMADA 'IA'",
        "overlays": [
            {"start": 3, "end": 15, "text": "💻 Programação | 📊 Dados | 🚀 Operações | 📱 Marketing"},
            {"start": 35, "end": 50, "text": "💡 IA + Área Real = Habilidade Profissional"}
        ]
    },
    {
        "num": 5,
        "name": "05_nota_alta_nao_e_o_mesmo_que_aprender.mp4",
        "sub": "v05.ass",
        "ss": 1620.0,
        "t": 60.0,
        "title": "NOTA ALTA NÃO É O MESMO QUE APRENDER",
        "overlays": [
            {"start": 0, "end": 8, "text": "📊 A IA me ajudou a não tirar menos de 8"},
            {"start": 20, "end": 30, "text": "🚨 NOTA  ≠  COMPREENSÃO REAL"}
        ]
    },
    {
        "num": 6,
        "name": "06_o_pior_jeito_de_prospectar_empresas.mp4",
        "sub": "v06.ass",
        "ss": 162.0,
        "t": 38.0,
        "title": "O PIOR JEITO DE PROSPECTAR EMPRESAS NOVAS",
        "overlays": [
            {"start": 3, "end": 12, "text": "🏢 Empresa Nova ➡️ Possível Cliente"},
            {"start": 12, "end": 28, "text": "📩 Dezenas de mensagens iguais (Spam)"}
        ]
    },
    {
        "num": 7,
        "name": "07_por_que_parei_de_construir_do_zero.mp4",
        "sub": "v07.ass",
        "ss": 1720.0,
        "t": 26.0,
        "title": "POR QUE PAREI DE CONSTRUIR TUDO DO ZERO",
        "overlays": [
            {"start": 10, "end": 23, "text": "🛠️ Agent Zero: Código Aberto + Linux + Skills"}
        ]
    },
    {
        "num": 8,
        "name": "08_por_que_computer_use_ainda_erra_tanto.mp4",
        "sub": "v08.ass",
        "ss": 1746.0,
        "t": 65.0,
        "title": "POR QUE COMPUTER USE AINDA ERRA TANTO?",
        "overlays": [
            {"start": 15, "end": 30, "text": "❌ Cliques em Coordenadas (Frágil)"},
            {"start": 48, "end": 65, "text": "✅ Menos cliques frágeis. Mais ações estruturadas."}
        ]
    }
]

print("Starting Enhanced Rendering with Titles, Text Overlays, Zooms & Subtitles...")

for v in videos:
    out_path = os.path.join(out_dir, v["name"])
    ass_path = os.path.join(subs_dir, v["sub"]).replace("\\", "/")
    ass_escaped = ass_path.replace(":", "\\:")
    
    title_text = v["title"].replace("'", "").replace("\"", "")
    
    print(f"\n[{v['num']}/8] Rendering Enhanced Video: {v['name']}")
    
    # Building FFmpeg Filter Graph
    # 1. Base Crop 9:16 + Scale 1080x1920
    # 2. Draw Title Banner Box at the top (y=120)
    # 3. Draw Subtitles
    # 4. Draw Overlay Text Cards
    
    vf_filters = [
        "crop=ih*9/16:ih:(iw-ih*9/16)/2:0",
        "scale=1080:1920",
        # Top Title Banner Box
        f"drawbox=y=110:h=120:color=black@0.75:t=fill",
        f"drawtext=fontfile='C\\:/Windows/Fonts/arialbd.ttf':text='{title_text}':fontcolor=white:fontsize=40:x=(w-text_w)/2:y=150"
    ]
    
    # Add dynamic overlay text badges per video
    for ov in v["overlays"]:
        ov_txt = ov["text"].replace("'", "").replace("\"", "")
        s_t = ov["start"]
        e_t = ov["end"]
        vf_filters.append(
            f"drawbox=y=380:h=90:color=black@0.70:t=fill:enable='between(t,{s_t},{e_t})'"
        )
        vf_filters.append(
            f"drawtext=fontfile='C\\:/Windows/Fonts/arial.ttf':text='{ov_txt}':fontcolor=white:fontsize=36:x=(w-text_w)/2:y=405:enable='between(t,{s_t},{e_t})'"
        )
    
    # Add ASS Subtitles
    vf_filters.append(f"subtitles='{ass_escaped}'")
    
    vf_str = ",".join(vf_filters)
    
    cmd = [
        "ffmpeg", "-y",
        "-ss", str(v["ss"]),
        "-i", src_video,
        "-t", str(v["t"]),
        "-vf", vf_str,
        "-af", "loudnorm=I=-16:TP=-1.5:LRA=11",
        "-c:v", "libx264", "-preset", "fast", "-crf", "20",
        "-c:a", "aac", "-b:a", "192k",
        out_path
    ]
    
    res = subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    if res.returncode == 0 and os.path.exists(out_path):
        mb = round(os.path.getsize(out_path)/(1024*1024), 2)
        print(f"ENHANCED SUCCESS: {v['name']} ({mb} MB)")
    else:
        print(f"ERROR rendering {v['name']}")

print("\nALL 8 ENHANCED VIDEOS WITH TITLES & TEXT OVERLAYS RENDERED!")
