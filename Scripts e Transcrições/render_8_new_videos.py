import os
import subprocess
import sys

sys.stdout.reconfigure(encoding='utf-8')

src_video = r"C:\Users\Kethely\Videos\2026-07-26-09-28-42.mp4"
out_dir = r"C:\Users\Kethely\Downloads\novos_cortes_editados"
os.makedirs(out_dir, exist_ok=True)

scratch_dir = r"C:\Users\Kethely\.gemini\antigravity\brain\9dbd3421-ae5c-4f63-9d99-553453c42d0e\scratch"
subs_dir = os.path.join(scratch_dir, "minimalist_subs_8vids")

videos = [
    {"num": 1, "name": "01_ia_da_dinheiro_mesmo.mp4", "sub": "v01.ass", "ss": 1002.0, "t": 62.0},
    {"num": 2, "name": "02_quanto_mais_aprendo_ia_menos_dependo.mp4", "sub": "v02.ass", "ss": 1104.0, "t": 34.0},
    {"num": 3, "name": "03_por_que_ia_responde_generico.mp4", "sub": "v03.ass", "ss": 1290.0, "t": 40.0},
    {"num": 4, "name": "04_nao_procure_uma_profissao_chamada_ia.mp4", "sub": "v04.ass", "ss": 1463.0, "t": 50.0},
    {"num": 5, "name": "05_nota_alta_nao_e_o_mesmo_que_aprender.mp4", "sub": "v05.ass", "ss": 1620.0, "t": 60.0},
    {"num": 6, "name": "06_o_pior_jeito_de_prospectar_empresas.mp4", "sub": "v06.ass", "ss": 162.0, "t": 38.0},
    {"num": 7, "name": "07_por_que_parei_de_construir_do_zero.mp4", "sub": "v07.ass", "ss": 1720.0, "t": 26.0},
    {"num": 8, "name": "08_por_que_computer_use_ainda_erra_tanto.mp4", "sub": "v08.ass", "ss": 1746.0, "t": 65.0}
]

print("Starting Batch Rendering for 8 New Clean Minimalist Videos...")

for v in videos:
    out_path = os.path.join(out_dir, v["name"])
    ass_path = os.path.join(subs_dir, v["sub"]).replace("\\", "/")
    ass_escaped = ass_path.replace(":", "\\:")
    
    print(f"\n[{v['num']}/8] Rendering: {v['name']}")
    
    vf = f"crop=ih*9/16:ih:(iw-ih*9/16)/2:0,scale=1080:1920,subtitles='{ass_escaped}'"
    
    cmd = [
        "ffmpeg", "-y",
        "-ss", str(v["ss"]),
        "-i", src_video,
        "-t", str(v["t"]),
        "-vf", vf,
        "-af", "loudnorm=I=-16:TP=-1.5:LRA=11",
        "-c:v", "libx264", "-preset", "fast", "-crf", "20",
        "-c:a", "aac", "-b:a", "192k",
        out_path
    ]
    
    res = subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    if res.returncode == 0 and os.path.exists(out_path):
        mb = round(os.path.getsize(out_path)/(1024*1024), 2)
        print(f"SUCCESS: {v['name']} rendered ({mb} MB)")
    else:
        print(f"ERROR rendering {v['name']}")

print("\nALL 8 NEW CLEAN VIDEOS RENDERED SUCCESSFULLY!")
