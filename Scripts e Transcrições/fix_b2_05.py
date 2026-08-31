"""
Fix b2_05: re-renderiza o video com segmentos concatenados.
O erro anterior era que o caminho do ASS com C\:/ interferia no output path.
Solução: copiar o ASS para C:\Temp\ e usar caminho curto.
"""
import os
import subprocess
import shutil
import sys

sys.stdout.reconfigure(encoding='utf-8')

SRC      = r"C:\Users\Kethely\Videos\2026-07-26-09-28-42.mp4"
OUT_DIR  = r"C:\Users\Kethely\Downloads\cortes_bloco2_editados"
SUBS_SRC = r"C:\Users\Kethely\.gemini\antigravity\brain\9dbd3421-ae5c-4f63-9d99-553453c42d0e\scratch\minimalist_subs_bloco2\b2_v05.ass"

# Copia ASS para um path curto e sem caracteres especiais
ASS_TEMP = r"C:\Temp\b2_v05.ass"
os.makedirs(r"C:\Temp", exist_ok=True)
shutil.copy2(SUBS_SRC, ASS_TEMP)

# Segmentos: 42:32–43:14 (42s) + 49:28–49:52 (24s)
SEGMENTS = [
    {"ss": 42*60+32, "t": 42},
    {"ss": 49*60+28, "t": 24},
]
TOTAL_T  = 66
OUT_PATH = os.path.join(OUT_DIR, "b2_05_o_sistema_que_estou_construindo.mp4")

# ASS path: no Windows ffmpeg precisa de C\\:/...
ass_for_ffmpeg = ASS_TEMP.replace("\\", "/").replace(":", "\\:")
print(f"ASS path para ffmpeg: {ass_for_ffmpeg}")

# ── Etapa 1: Cortar segmentos em clips temporários ──────────────────────────
tmp_clips = []
for i, seg in enumerate(SEGMENTS):
    tmp = os.path.join(OUT_DIR, f"_tmp_b205_{i}.mp4")
    tmp_clips.append(tmp)
    cmd = [
        "ffmpeg", "-y",
        "-ss", str(seg["ss"]),
        "-i", SRC,
        "-t", str(seg["t"]),
        "-c:v", "libx264", "-preset", "ultrafast", "-crf", "16",
        "-c:a", "aac", "-b:a", "192k",
        tmp
    ]
    print(f"  Cortando segmento {i+1}...")
    r = subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)
    if r.returncode != 0:
        print(f"  ERRO no segmento {i+1}: {r.stderr.decode(errors='ignore')[-200:]}")
        sys.exit(1)

# ── Etapa 2: Escrever lista de concat ──────────────────────────────────────
concat_list = os.path.join(OUT_DIR, "_concat_b205.txt")
with open(concat_list, "w") as f:
    for c in tmp_clips:
        f.write(f"file '{c}'\n")

# ── Etapa 3: Concatenar em clip intermediário ───────────────────────────────
joined = os.path.join(OUT_DIR, "_joined_b205.mp4")
cmd_concat = [
    "ffmpeg", "-y", "-f", "concat", "-safe", "0",
    "-i", concat_list,
    "-c", "copy",
    joined
]
print("  Concatenando segmentos...")
r = subprocess.run(cmd_concat, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)
if r.returncode != 0:
    print(f"  ERRO na concatenação: {r.stderr.decode(errors='ignore')[-300:]}")
    sys.exit(1)

# ── Etapa 4: Aplicar filtros visuais + legendas ─────────────────────────────
title_text = "O SISTEMA QUE ESTOU CONSTRUINDO"

# Escapar texto do título
title_safe = title_text.replace("'", "\\'").replace(":", "\\:")

vf_parts = [
    "crop=ih*9/16:ih:(iw-ih*9/16)/2:0",
    "scale=1080:1920",
    # Focus zoom: 6–20s e 38–55s
    "scale=eval=frame:w='if(between(t,6,20)+between(t,38,55),1166,1080)':h='if(between(t,6,20)+between(t,38,55),2073,1920)',crop=1080:1920",
    # Título
    "drawbox=y=110:h=110:color=black@0.80:t=fill",
    f"drawtext=fontfile='C\\:/Windows/Fonts/arialbd.ttf':text='{title_safe}':fontcolor=white:fontsize=36:x=(w-text_w)/2:y=150",
    # Card 1: 0–6s
    "drawbox=y=370:h=86:color=black@0.75:t=fill:enable='between(t,0,6)'",
    "drawtext=fontfile='C\\:/Windows/Fonts/arial.ttf':text='Dados da empresa -> 30 posts + 30 videos em 24h':fontcolor=white:fontsize=30:x=(w-text_w)/2:y=396:enable='between(t,0,6)'",
    # Card 2: 20–38s
    "drawbox=y=370:h=86:color=black@0.75:t=fill:enable='between(t,20,38)'",
    "drawtext=fontfile='C\\:/Windows/Fonts/arial.ttf':text='O desafio: automatico sem parecer generico':fontcolor=white:fontsize=30:x=(w-text_w)/2:y=396:enable='between(t,20,38)'",
    # Legendas
    f"subtitles='{ass_for_ffmpeg}'",
]

vf_str = ",".join(vf_parts)

cmd_final = [
    "ffmpeg", "-y",
    "-i", joined,
    "-t", str(TOTAL_T),
    "-vf", vf_str,
    "-af", "loudnorm=I=-16:TP=-1.5:LRA=11",
    "-c:v", "libx264", "-preset", "medium", "-crf", "18",
    "-c:a", "aac", "-b:a", "192k",
    OUT_PATH
]

print(f"  Renderizando com filtros: {OUT_PATH}")
r = subprocess.run(cmd_final, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)
if r.returncode != 0:
    print(f"  ERRO FINAL: {r.stderr.decode(errors='ignore')[-500:]}")
else:
    mb = round(os.path.getsize(OUT_PATH) / (1024*1024), 2) if os.path.exists(OUT_PATH) else 0
    print(f"  SUCCESS: b2_05_o_sistema_que_estou_construindo.mp4 ({mb} MB)")

# Limpeza
for tmp in tmp_clips:
    if os.path.exists(tmp): os.remove(tmp)
if os.path.exists(joined):   os.remove(joined)
if os.path.exists(concat_list): os.remove(concat_list)

print("\nConcluído!")
