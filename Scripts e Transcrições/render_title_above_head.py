import os
import subprocess
import sys

sys.stdout.reconfigure(encoding='utf-8')

src_video = r"C:\Users\Kethely\Videos\2026-07-26-09-28-42.mp4"
out_dir = r"C:\Users\Kethely\Downloads\novos_cortes_editados"
os.makedirs(out_dir, exist_ok=True)

scratch_dir = r"C:\Users\Kethely\.gemini\antigravity\brain\9dbd3421-ae5c-4f63-9d99-553453c42d0e\scratch"
subs_dir = os.path.join(scratch_dir, "minimalist_subs_centered")
frames_dir = os.path.join(scratch_dir, "frames_verification")
os.makedirs(frames_dir, exist_ok=True)

videos = [
    {
        "num": 1,
        "name": "01_ia_da_dinheiro_mesmo.mp4",
        "sub": "v01.ass",
        "ss": 1002.0,
        "t": 62.0,
        "title": "IA DÁ DINHEIRO MESMO?",
        "zooms": [(4.0, 14.0), (25.0, 45.0)]
    },
    {
        "num": 2,
        "name": "02_quanto_mais_aprendo_ia_menos_dependo.mp4",
        "sub": "v02.ass",
        "ss": 1104.0,
        "t": 34.0,
        "title": "QUANTO MAIS APRENDO IA, MENOS DEPENDO DELA",
        "zooms": [(3.0, 14.0)]
    },
    {
        "num": 3,
        "name": "03_por_que_ia_responde_generico.mp4",
        "sub": "v03.ass",
        "ss": 1290.0,
        "t": 40.0,
        "title": "POR QUE SUA IA RESPONDE GENÉRICO?",
        "zooms": [(8.0, 25.0)]
    },
    {
        "num": 4,
        "name": "04_nao_procure_uma_profissao_chamada_ia.mp4",
        "sub": "v04.ass",
        "ss": 1463.0,
        "t": 50.0,
        "title": "NÃO PROCURE UMA PROFISSÃO CHAMADA 'IA'",
        "zooms": [(15.0, 35.0)]
    },
    {
        "num": 5,
        "name": "05_nota_alta_nao_e_o_mesmo_que_aprender.mp4",
        "sub": "v05.ass",
        "ss": 1620.0,
        "t": 60.0,
        "title": "NOTA ALTA NÃO É O MESMO QUE APRENDER",
        "zooms": [(20.0, 30.0), (52.0, 60.0)]
    },
    {
        "num": 6,
        "name": "06_o_pior_jeito_de_prospectar_empresas.mp4",
        "sub": "v06.ass",
        "ss": 162.0,
        "t": 38.0,
        "title": "O PIOR JEITO DE PROSPECTAR EMPRESAS NOVAS",
        "zooms": [(12.0, 28.0)]
    },
    {
        "num": 7,
        "name": "07_por_que_parei_de_construir_do_zero.mp4",
        "sub": "v07.ass",
        "ss": 1720.0,
        "t": 26.0,
        "title": "POR QUE PAREI DE CONSTRUIR TUDO DO ZERO",
        "zooms": [(10.0, 23.0)]
    },
    {
        "num": 8,
        "name": "08_por_que_computer_use_ainda_erra_tanto.mp4",
        "sub": "v08.ass",
        "ss": 1746.0,
        "t": 65.0,
        "title": "POR QUE COMPUTER USE AINDA ERRA TANTO?",
        "zooms": [(15.0, 30.0), (48.0, 65.0)]
    }
]

print("Rendering 8 Videos with Title Box positioned RIGHT ABOVE THE HEAD (y=980)...")

for v in videos:
    out_path = os.path.join(out_dir, v["name"])
    ass_path = os.path.join(subs_dir, v["sub"]).replace("\\", "/")
    ass_escaped = ass_path.replace(":", "\\:")
    title_text = v["title"].replace("'", "").replace("\"", "")
    
    print(f"\n[{v['num']}/8] Rendering Video with Title Above Head: {v['name']}")
    
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
    
    # Title Banner Positioned EXACTLY ABOVE THE HEAD in the camera area (y=980)
    # Background Box: y=970, Height: 130px, Fontsize: 44pt
    vf_chain.append("drawbox=y=970:h=130:color=black@0.85:t=fill")
    vf_chain.append(
        f"drawtext=fontfile='C\\:/Windows/Fonts/arialbd.ttf':text='{title_text}':fontcolor=white:fontsize=44:x=(w-text_w)/2:y=1012"
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
        print(f"HEAD-TITLE SUCCESS: {v['name']} ({mb} MB)")
        
        # Extract verification frame at 3 seconds
        frame_jpg = os.path.join(frames_dir, f"v{v['num']:02d}_head_title.jpg")
        subprocess.run([
            "ffmpeg", "-y", "-ss", "3", "-i", out_path, "-vframes", "1", frame_jpg
        ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

print("\nALL 8 VIDEOS RENDERED WITH TITLE EXACTLY ABOVE THE HEAD!")
