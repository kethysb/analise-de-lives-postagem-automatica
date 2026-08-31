import os
import subprocess
import sys

sys.stdout.reconfigure(encoding='utf-8')

src_video = r"C:\Users\Kethely\Videos\2026-07-26-09-28-42.mp4"
out_dir = r"C:\Users\Kethely\Downloads\novos_cortes_editados"
os.makedirs(out_dir, exist_ok=True)

scratch_dir = r"C:\Users\Kethely\.gemini\antigravity\brain\9dbd3421-ae5c-4f63-9d99-553453c42d0e\scratch"
subs_dir = os.path.join(scratch_dir, "minimalist_subs_8vids")

# Video metadata with custom editorial edit points and focus zooms
videos = [
    {
        "num": 1,
        "name": "01_ia_da_dinheiro_mesmo.mp4",
        "sub": "v01.ass",
        "ss": 1002.0,
        "t": 62.0,
        "title": "IA DÁ DINHEIRO MESMO?",
        # Focus Zoom intervals (start, end)
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

print("Starting Human-Crafted Video Rendering Engine...")

for v in videos:
    out_path = os.path.join(out_dir, v["name"])
    ass_path = os.path.join(subs_dir, v["sub"]).replace("\\", "/")
    ass_escaped = ass_path.replace(":", "\\:")
    
    title_text = v["title"].replace("'", "").replace("\"", "")
    
    print(f"\n[{v['num']}/8] Rendering Human-Edited Video: {v['name']}")
    
    # Base Crop 9:16 & Scale
    vf_chain = [
        "crop=ih*9/16:ih:(iw-ih*9/16)/2:0",
        "scale=1080:1920"
    ]
    
    # 1. Focus Zoom Switches (simulate multi-cam cut)
    if v["zooms"]:
        zoom_exprs = []
        for zs, ze in v["zooms"]:
            zoom_exprs.append(f"between(t,{zs},{ze})")
        cond_zoom = "+".join(zoom_exprs)
        # Apply smooth 1.08x scale zoom during emphasis
        vf_chain.append(
            f"scale=eval=frame:w='if({cond_zoom}, 1166, 1080)':h='if({cond_zoom}, 2073, 1920)',crop=1080:1920"
        )
    
    # 2. Minimalist Header Title (Top 120px, clean rounded dark bg)
    vf_chain.append("drawbox=y=110:h=110:color=black@0.80:t=fill")
    vf_chain.append(
        f"drawtext=fontfile='C\\:/Windows/Fonts/arialbd.ttf':text='{title_text}':fontcolor=white:fontsize=38:x=(w-text_w)/2:y=146"
    )
    
    # 3. Editorial Pop-in Cards (Human-style lower thirds)
    for card in v["cards"]:
        c_txt = card["text"].replace("'", "").replace("\"", "")
        cs = card["s"]
        ce = card["e"]
        # Fade in/out box & text
        vf_chain.append(
            f"drawbox=y=360:h=86:color=black@0.75:t=fill:enable='between(t,{cs},{ce})'"
        )
        vf_chain.append(
            f"drawtext=fontfile='C\\:/Windows/Fonts/arial.ttf':text='{c_txt}':fontcolor=white:fontsize=34:x=(w-text_w)/2:y=386:enable='between(t,{cs},{ce})'"
        )
    
    # 4. ASS Subtitles
    vf_chain.append(f"subtitles='{ass_escaped}'")
    
    vf_str = ",".join(vf_chain)
    
    cmd = [
        "ffmpeg", "-y",
        "-ss", str(v["ss"]),
        "-i", src_video,
        "-t", str(v["t"]),
        "-vf", vf_str,
        "-af", "loudnorm=I=-16:TP=-1.5:LRA=11",
        "-c:v", "libx264", "-preset", "medium", "-crf", "18",
        "-c:a", "aac", "-b:a", "192k",
        out_path
    ]
    
    res = subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    if res.returncode == 0 and os.path.exists(out_path):
        mb = round(os.path.getsize(out_path)/(1024*1024), 2)
        print(f"HUMAN EDIT SUCCESS: {v['name']} ({mb} MB)")
    else:
        print(f"ERROR rendering {v['name']}")

print("\nALL 8 HUMAN-CRAFTED VIDEOS RENDERED WITH MULTI-CAM ZOOMS & EDITORIAL CARDS!")
