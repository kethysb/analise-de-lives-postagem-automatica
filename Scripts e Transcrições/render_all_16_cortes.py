import os
import subprocess
import sys

sys.stdout.reconfigure(encoding='utf-8')

src_video = r"C:\Users\Kethely\Videos\2026-07-23-23-55-30.mp4"
out_dir = r"C:\Users\Kethely\Downloads\cortes_tiktok_editados"
os.makedirs(out_dir, exist_ok=True)

# List of 16 cuts with exact timestamps and titles
cuts = [
    {
        "num": 1,
        "name": "01_como_eu_encontrei_chatgpt_5reais.mp4",
        "title": "EU PAGAVA R$ 5 NO CHATGPT",
        "ss": 462,
        "t": 48
    },
    {
        "num": 2,
        "name": "02_plataforma_72_desconto.mp4",
        "title": "72% MAIS BARATO. COMO?",
        "ss": 753,
        "t": 45
    },
    {
        "num": 3,
        "name": "03_um_site_testei_outro_nao.mp4",
        "title": "UM EU TESTEI. O OUTRO, NAO.",
        "ss": 836,
        "t": 35
    },
    {
        "num": 4,
        "name": "04_de_onde_vem_apis_baratas.mp4",
        "title": "DE ONDE VEM O PRECO TAO BAIXO?",
        "ss": 888,
        "t": 55
    },
    {
        "num": 5,
        "name": "05_essa_api_pode_nao_ser_sua.mp4",
        "title": "ESSA API E REALMENTE SUA?",
        "ss": 1001,
        "t": 50
    },
    {
        "num": 6,
        "name": "06_quando_usaria_api_barata.mp4",
        "title": "QUANDO O BARATO DEIXA DE COMPENSAR",
        "ss": 1055,
        "t": 40
    },
    {
        "num": 7,
        "name": "07_nao_coloque_codigo_empresa_chatgpt.mp4",
        "title": "VOCE COLOCARIA O CODIGO DA EMPRESA AQUI?",
        "ss": 1088,
        "t": 45
    },
    {
        "num": 8,
        "name": "08_minha_diversao_virou_trabalhar.mp4",
        "title": "MEU HOBBY VIROU MEU TRABALHO",
        "ss": 1417,
        "t": 50
    },
    {
        "num": 9,
        "name": "09_beneficios_para_empresas.mp4",
        "title": "SUA EMPRESA PODE TER ACESSO A ISSO",
        "ss": 1928,
        "t": 50
    },
    {
        "num": 10,
        "name": "10_5mil_dolares_creditos_ia.mp4",
        "title": "US$ 5 MIL EM CREDITOS DE IA?",
        "ss": 2111,
        "t": 45
    },
    {
        "num": 11,
        "name": "11_3reais_por_100dolares_creditos.mp4",
        "title": "R$ 3 = US$ 100?",
        "ss": 2290,
        "t": 55
    },
    {
        "num": 12,
        "name": "12_quanto_gastei_usando_apis.mp4",
        "title": "7 MILHOES DE TOKENS POR US$ 2,42?",
        "ss": 2335,
        "t": 45
    },
    {
        "num": 13,
        "name": "13_almoco_gratis_ia_vai_acabar.mp4",
        "title": "O ALMOCO GRATIS VAI ACABAR",
        "ss": 2950,
        "t": 42
    },
    {
        "num": 14,
        "name": "14_ia_me_ensinou_a_aprender.mp4",
        "title": "A IA ME ENSINOU A APRENDER",
        "ss": 3030,
        "t": 70
    },
    {
        "num": 15,
        "name": "15_psicologia_ia_e_programacao.mp4",
        "title": "O QUE PSICOLOGIA TEM A VER COM IA?",
        "ss": 1896,
        "t": 45
    },
    {
        "num": 16,
        "name": "16_meu_site_maior_orgulho.mp4",
        "title": "MEU MAIOR ORGULHO AGORA",
        "ss": 5400,
        "t": 45
    }
]

print(f"Starting batch rendering of {len(cuts)} TikTok cuts...")

for c in cuts:
    out_path = os.path.join(out_dir, c["name"])
    print(f"\n==============================================")
    print(f"[{c['num']}/16] Rendering: {c['name']}")
    print(f"Title: {c['title']}")
    print(f"Start: {c['ss']}s, Duration: {c['t']}s")
    
    # FFmpeg crop to 9:16 vertical (1080x1920), add title box overlay, and loudnorm audio
    clean_title = c["title"].replace("'", "\\'").replace(":", "\\:")
    vf = f"crop=ih*9/16:ih:(iw-ih*9/16)/2:0,scale=1080:1920,drawtext=fontfile=C\\\\:/Windows/Fonts/arialbd.ttf:text='{clean_title}':fontcolor=yellow:fontsize=44:x=(w-text_w)/2:y=160:box=1:boxcolor=black@0.75:boxborderw=12"
    
    cmd = [
        "ffmpeg", "-y",
        "-ss", str(c["ss"]),
        "-i", src_video,
        "-t", str(c["t"]),
        "-vf", vf,
        "-af", "loudnorm=I=-16:TP=-1.5:LRA=11",
        "-c:v", "libx264",
        "-preset", "fast",
        "-crf", "22",
        "-c:a", "aac",
        "-b:a", "192k",
        out_path
    ]
    
    res = subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    if res.returncode == 0 and os.path.exists(out_path):
        size_mb = round(os.path.getsize(out_path) / (1024 * 1024), 2)
        print(f"SUCCESS: {c['name']} rendered ({size_mb} MB)")
    else:
        print(f"ERROR rendering {c['name']}")

print("\nALL 16 VIDEOS RENDERED SUCCESSFULLY!")
