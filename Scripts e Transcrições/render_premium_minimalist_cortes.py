import os
import subprocess
import sys

sys.stdout.reconfigure(encoding='utf-8')

src_video = r"C:\Users\Kethely\Videos\2026-07-23-23-55-30.mp4"
out_dir = r"C:\Users\Kethely\Downloads\cortes_tiktok_editados"
subs_dir = r"C:\Users\Kethely\.gemini\antigravity\brain\9dbd3421-ae5c-4f63-9d99-553453c42d0e\scratch\minimalist_subs"

cuts = [
    {"num": 1, "name": "01_como_eu_encontrei_chatgpt_5reais.mp4", "sub": "video_01.ass", "ss": 462, "t": 48, "card": r"C:\Users\Kethely\.gemini\antigravity\brain\9dbd3421-ae5c-4f63-9d99-553453c42d0e\chatgpt_5reais_minimal_1785067085536.jpg"},
    {"num": 2, "name": "02_plataforma_72_desconto.mp4", "sub": "video_02.ass", "ss": 753, "t": 45, "card": r"C:\Users\Kethely\.gemini\antigravity\brain\9dbd3421-ae5c-4f63-9d99-553453c42d0e\discount_72_minimal_1785067097059.jpg"},
    {"num": 3, "name": "03_um_site_testei_outro_nao.mp4", "sub": "video_03.ass", "ss": 836, "t": 35, "card": None},
    {"num": 4, "name": "04_de_onde_vem_apis_baratas.mp4", "sub": "video_04.ass", "ss": 888, "t": 55, "card": r"C:\Users\Kethely\.gemini\antigravity\brain\9dbd3421-ae5c-4f63-9d99-553453c42d0e\cloud_credits_minimal_1785067110367.jpg"},
    {"num": 5, "name": "05_essa_api_pode_nao_ser_sua.mp4", "sub": "video_05.ass", "ss": 1001, "t": 50, "card": None},
    {"num": 6, "name": "06_quando_usaria_api_barata.mp4", "sub": "video_06.ass", "ss": 1055, "t": 40, "card": None},
    {"num": 7, "name": "07_nao_coloque_codigo_empresa_chatgpt.mp4", "sub": "video_07.ass", "ss": 1088, "t": 45, "card": None},
    {"num": 8, "name": "08_minha_diversao_virou_trabalhar.mp4", "sub": "video_08.ass", "ss": 1417, "t": 50, "card": None},
    {"num": 9, "name": "09_beneficios_para_empresas.mp4", "sub": "video_09.ass", "ss": 1928, "t": 50, "card": r"C:\Users\Kethely\.gemini\antigravity\brain\9dbd3421-ae5c-4f63-9d99-553453c42d0e\cloud_credits_minimal_1785067110367.jpg"},
    {"num": 10, "name": "10_5mil_dolares_creditos_ia.mp4", "sub": "video_10.ass", "ss": 2111, "t": 45, "card": r"C:\Users\Kethely\.gemini\antigravity\brain\9dbd3421-ae5c-4f63-9d99-553453c42d0e\cloud_credits_minimal_1785067110367.jpg"},
    {"num": 11, "name": "11_3reais_por_100dolares_creditos.mp4", "sub": "video_11.ass", "ss": 2290, "t": 55, "card": None},
    {"num": 12, "name": "12_quanto_gastei_usando_apis.mp4", "sub": "video_12.ass", "ss": 2335, "t": 45, "card": None},
    {"num": 13, "name": "13_almoco_gratis_ia_vai_acabar.mp4", "sub": "video_13.ass", "ss": 2950, "t": 42, "card": None},
    {"num": 14, "name": "14_ia_me_ensinou_a_aprender.mp4", "sub": "video_14.ass", "ss": 3030, "t": 70, "card": None},
    {"num": 15, "name": "15_psicologia_ia_e_programacao.mp4", "sub": "video_15.ass", "ss": 1896, "t": 45, "card": None},
    {"num": 16, "name": "16_meu_site_maior_orgulho.mp4", "sub": "video_16.ass", "ss": 5400, "t": 45, "card": None}
]

print("Starting Premium Minimalist Batch Rendering for 16 Videos...")

for c in cuts:
    out_path = os.path.join(out_dir, c["name"])
    ass_path = os.path.join(subs_dir, c["sub"]).replace("\\", "/")
    
    print(f"\n==============================================")
    print(f"[{c['num']}/16] Rendering: {c['name']}")
    
    # Escape ASS path for FFmpeg subtitles filter
    ass_escaped = ass_path.replace(":", "\\:")
    
    if c["card"] and os.path.exists(c["card"]):
        card_path = c["card"].replace("\\", "/")
        # Overlay minimalist card overlay at 8s to 13s
        vf = f"[0:v]crop=ih*9/16:ih:(iw-ih*9/16)/2:0,scale=1080:1920[vbase]; [1:v]scale=720:720[card]; [vbase][card]overlay=x=180:y=600:enable='between(t,8,13)'[vover]; [vover]subtitles='{ass_escaped}'[outv]"
        cmd = [
            "ffmpeg", "-y",
            "-ss", str(c["ss"]),
            "-i", src_video,
            "-loop", "1", "-i", card_path,
            "-t", str(c["t"]),
            "-filter_complex", vf,
            "-map", "[outv]",
            "-map", "0:a",
            "-af", "loudnorm=I=-16:TP=-1.5:LRA=11",
            "-c:v", "libx264", "-preset", "fast", "-crf", "20",
            "-c:a", "aac", "-b:a", "192k",
            out_path
        ]
    else:
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
        print(f"SUCCESS: {c['name']} rendered ({mb} MB)")
    else:
        print(f"ERROR rendering {c['name']}")

print("\nALL 16 PREMIUM MINIMALIST VIDEOS RENDERED!")
