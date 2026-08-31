"""
Fix b2_05 v2: usa subprocess com shell=True e powershell para evitar
problemas de escape de aspas simples no vf_str do ffmpeg.
Estratégia: gera um script .bat temporário com o comando ffmpeg completo.
"""
import os
import subprocess
import shutil
import sys

sys.stdout.reconfigure(encoding='utf-8')

SRC      = r"C:\Users\Kethely\Videos\2026-07-26-09-28-42.mp4"
OUT_DIR  = r"C:\Users\Kethely\Downloads\cortes_bloco2_editados"
SUBS_SRC = r"C:\Users\Kethely\.gemini\antigravity\brain\9dbd3421-ae5c-4f63-9d99-553453c42d0e\scratch\minimalist_subs_bloco2\b2_v05.ass"
ASS_TEMP = r"C:\Temp\b2v05.ass"
os.makedirs(r"C:\Temp", exist_ok=True)
shutil.copy2(SUBS_SRC, ASS_TEMP)

SEGMENTS = [
    {"ss": 42*60+32, "t": 42},
    {"ss": 49*60+28, "t": 24},
]
TOTAL_T  = 66
OUT_PATH = os.path.join(OUT_DIR, "b2_05_o_sistema_que_estou_construindo.mp4")

print("=== Fix b2_05 v2 ===")

# ── Etapa 1: Segmentos ──────────────────────────────────────────────────────
tmp_clips = []
for i, seg in enumerate(SEGMENTS):
    tmp = os.path.join(OUT_DIR, f"_tmp_b205v2_{i}.mp4")
    tmp_clips.append(tmp)
    cmd = ["ffmpeg", "-y", "-ss", str(seg["ss"]), "-i", SRC,
           "-t", str(seg["t"]),
           "-c:v", "libx264", "-preset", "ultrafast", "-crf", "16",
           "-c:a", "aac", "-b:a", "192k", tmp]
    print(f"  Cortando segmento {i+1}: {seg['ss']}s + {seg['t']}s...")
    r = subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)
    if r.returncode != 0:
        print(f"ERRO seg {i+1}: {r.stderr.decode(errors='ignore')[-200:]}")
        sys.exit(1)

# ── Etapa 2: Concat ─────────────────────────────────────────────────────────
concat_list = os.path.join(OUT_DIR, "_concat_b205v2.txt")
with open(concat_list, "w", encoding="utf-8") as f:
    for c in tmp_clips:
        f.write(f"file '{c}'\n")

joined = os.path.join(OUT_DIR, "_joined_b205v2.mp4")
cmd_concat = ["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", concat_list, "-c", "copy", joined]
print("  Concatenando...")
r = subprocess.run(cmd_concat, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)
if r.returncode != 0:
    print(f"ERRO concat: {r.stderr.decode(errors='ignore')[-300:]}")
    sys.exit(1)

# ── Etapa 3: Render final SEM subtitles no vf_str, depois mux ───────────────
# Estratégia alternativa: renderiza video limpo e depois faz mux das legendas 
# usando um segundo passo com subtitles filter em arquivo separado para evitar
# conflito de escape de aspas simples nos enable='' 
# 
# Usamos arquivo de filtros ffmpeg (filtergraph file) para evitar o problema

# Cria arquivo de filtro temporário
filter_file = r"C:\Temp\b205_vf.txt"
ass_path_fwd = ASS_TEMP.replace("\\", "/")  # sem escapes adicionais

# No arquivo de filtro, as aspas simples dentro de enable não conflitam
filter_content = f"""crop=ih*9/16:ih:(iw-ih*9/16)/2:0,
scale=1080:1920,
scale=eval=frame:w=if(between(t\\,6\\,20)+between(t\\,38\\,55)\\,1166\\,1080):h=if(between(t\\,6\\,20)+between(t\\,38\\,55)\\,2073\\,1920),
crop=1080:1920,
drawbox=y=110:h=110:color=black@0.80:t=fill,
drawtext=fontfile=C\\\\:/Windows/Fonts/arialbd.ttf:text=O SISTEMA QUE ESTOU CONSTRUINDO:fontcolor=white:fontsize=36:x=(w-text_w)/2:y=150,
drawbox=y=370:h=86:color=black@0.75:t=fill:enable=between(t\\,0\\,6),
drawtext=fontfile=C\\\\:/Windows/Fonts/arial.ttf:text=Dados da empresa -> 30 posts + 30 videos em 24h:fontcolor=white:fontsize=28:x=(w-text_w)/2:y=396:enable=between(t\\,0\\,6),
drawbox=y=370:h=86:color=black@0.75:t=fill:enable=between(t\\,20\\,38),
drawtext=fontfile=C\\\\:/Windows/Fonts/arial.ttf:text=O desafio\\: automatico sem parecer generico:fontcolor=white:fontsize=28:x=(w-text_w)/2:y=396:enable=between(t\\,20\\,38),
subtitles={ass_path_fwd}"""

with open(filter_file, "w", encoding="utf-8") as f:
    f.write(filter_content)

print(f"  Filter file: {filter_file}")
print(f"  Output: {OUT_PATH}")

cmd_final = [
    "ffmpeg", "-y",
    "-i", joined,
    "-t", str(TOTAL_T),
    "-filter_complex_script", filter_file,
    "-af", "loudnorm=I=-16:TP=-1.5:LRA=11",
    "-c:v", "libx264", "-preset", "medium", "-crf", "18",
    "-c:a", "aac", "-b:a", "192k",
    OUT_PATH
]

print("  Renderizando com filter_complex_script...")
r = subprocess.run(cmd_final, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)
if r.returncode != 0:
    stderr_txt = r.stderr.decode(errors='ignore')
    print(f"  ERRO: {stderr_txt[-600:]}")
    
    # Fallback: render sem subtitles
    print("\n  Tentando fallback SEM subtitles...")
    vf_simple = (
        "crop=ih*9/16:ih:(iw-ih*9/16)/2:0,"
        "scale=1080:1920,"
        "drawbox=y=110:h=110:color=black@0.80:t=fill"
    )
    cmd_fallback = [
        "ffmpeg", "-y",
        "-i", joined,
        "-t", str(TOTAL_T),
        "-vf", vf_simple,
        "-af", "loudnorm=I=-16:TP=-1.5:LRA=11",
        "-c:v", "libx264", "-preset", "medium", "-crf", "18",
        "-c:a", "aac", "-b:a", "192k",
        OUT_PATH
    ]
    r2 = subprocess.run(cmd_fallback, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)
    if r2.returncode == 0 and os.path.exists(OUT_PATH):
        mb = round(os.path.getsize(OUT_PATH)/(1024*1024), 2)
        print(f"  FALLBACK OK (sem legendas): {mb} MB")
    else:
        print(f"  FALLBACK ERRO: {r2.stderr.decode(errors='ignore')[-300:]}")
else:
    if os.path.exists(OUT_PATH):
        mb = round(os.path.getsize(OUT_PATH)/(1024*1024), 2)
        print(f"  SUCCESS: b2_05_o_sistema_que_estou_construindo.mp4 ({mb} MB)")
    else:
        print("  ARQUIVO NÃO ENCONTRADO APÓS RENDER")

# Limpeza
for tmp in tmp_clips:
    if os.path.exists(tmp): os.remove(tmp)
for f in [joined, concat_list, filter_file]:
    if os.path.exists(f): os.remove(f)

print("\nConcluído!")
