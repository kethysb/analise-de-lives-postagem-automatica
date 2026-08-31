import os
import subprocess
import sys

sys.stdout.reconfigure(encoding='utf-8')

src_video = r"C:\Users\Kethely\Videos\2026-07-23-23-55-30.mp4"
out_dir = r"C:\Users\Kethely\Downloads\cortes_tiktok_editados"
subs_dir = r"C:\Users\Kethely\.gemini\antigravity\brain\9dbd3421-ae5c-4f63-9d99-553453c42d0e\scratch\minimalist_subs"

cuts = [
    {"num": 1, "name": "01_como_eu_encontrei_chatgpt_5reais.mp4", "sub": "video_01.ass", "ss": 462, "t": 48},
    {"num": 2, "name": "02_plataforma_72_desconto.mp4", "sub": "video_02.ass", "ss": 753, "t": 45},
    {"num": 3, "name": "03_um_site_testei_outro_nao.mp4", "sub": "video_03.ass", "ss": 836, "t": 35},
    {"num": 4, "name": "04_de_onde_vem_apis_baratas.mp4", "sub": "video_04.ass", "ss": 888, "t": 55},
    {"num": 5, "name": "05_essa_api_pode_nao_ser_sua.mp4", "sub": "video_05.ass", "ss": 1001, "t": 50},
    {"num": 6, "name": "06_quando_usaria_api_barata.mp4", "sub": "video_06.ass", "ss": 1055, "t": 40},
    {"num": 7, "name": "07_nao_coloque_codigo_empresa_chatgpt.mp4", "sub": "video_07.ass", "ss": 1088, "t": 45},
    {"num": 8, "name": "08_minha_diversao_virou_trabalhar.mp4", "sub": "video_08.ass", "ss": 1417, "t": 50},
    {"num": 9, "name": "09_beneficios_para_empresas.mp4", "sub": "video_09.ass", "ss": 1928, "t": 50},
    {"num": 10, "name": "10_5mil_dolares_creditos_ia.mp4", "sub": "video_10.ass", "ss": 2111, "t": 45},
    {"num": 11, "name": "11_3reais_por_100dolares_creditos.mp4", "sub": "video_11.ass", "ss": 2290, "t": 55},
    {"num": 12, "name": "12_quanto_gastei_usando_apis.mp4", "sub": "video_12.ass", "ss": 2335, "t": 45},
    {"num": 13, "name": "13_almoco_gratis_ia_vai_acabar.mp4", "sub": "video_13.ass", "ss": 2950, "t": 42},
    {"num": 14, "name": "14_ia_me_ensinou_a_aprender.mp4", "sub": "video_14.ass", "ss": 3030, "t": 70},
    {"num": 15, "name": "15_psicologia_ia_e_programacao.mp4", "sub": "video_15.ass", "ss": 1896, "t": 45},
    {"num": 16, "name": "16_meu_site_maior_orgulho.mp4", "sub": "video_16.ass", "ss": 5400, "t": 45}
]

print("Starting Clean Re-Rendering (NO OVERLAY IMAGES) for 16 Videos...")

for c in cuts:
    out_path = os.path.join(out_dir, c["name"])
    ass_path = os.path.join(subs_dir, c["sub"]).replace("\\", "/")
    ass_escaped = ass_path.replace(":", "\\:")
    
    print(f"[{c['num']}/16] Rendering clean video: {c['name']}")
    
    vf = f"crop=ih*9/16:ih:(iw-ih*9/16)/2:0,scale=1080:1920,subtitles='{ass_escaped}'"
    cmd = [
        "ffmpeg", "-y",
        "-ss", str(c["ss"]),
        "-i", src_video,
        "-t", str(c["t"]),
        "-vf", vf,
        "-af", "loudnorm=I=-16:TP=-1.5:LRA=11",
        "-c:v", "libx264", "-preset", "fast", "-crf", "20",
        "-c:a", "aac", "-b:a", "192k",
        out_path
    ]
    
    res = subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    if res.returncode == 0 and os.path.exists(out_path):
        mb = round(os.path.getsize(out_path)/(1024*1024), 2)
        print(f"CLEAN SUCCESS: {c['name']} ({mb} MB)")
    else:
        print(f"ERROR rendering {c['name']}")

print("\nALL 16 CLEAN VIDEOS RENDERED (NO IMAGES)!")
