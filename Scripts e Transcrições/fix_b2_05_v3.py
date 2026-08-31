"""
Fix b2_05 v3: usa filtro `ass=` (em vez de subtitles=) no arquivo ja renderizado.
O filtro `ass` aceita path forward-slash sem escapes extras no Windows.
"""
import os
import subprocess
import shutil
import sys

sys.stdout.reconfigure(encoding='utf-8')

# O fallback ja gerou o video sem legendas:
SRC_NO_SUBS = r"C:\Users\Kethely\Downloads\cortes_bloco2_editados\b2_05_o_sistema_que_estou_construindo.mp4"
OUT_PATH    = r"C:\Users\Kethely\Downloads\cortes_bloco2_editados\b2_05_o_sistema_que_estou_construindo.mp4"
TMP_PATH    = r"C:\Temp\b205_nosubs.mp4"
ASS_FILE    = r"C:\Temp\b2v05.ass"  # ja copiado na etapa anterior

# Copia ASS caso nao exista mais
SUBS_SRC = r"C:\Users\Kethely\.gemini\antigravity\brain\9dbd3421-ae5c-4f63-9d99-553453c42d0e\scratch\minimalist_subs_bloco2\b2_v05.ass"
if not os.path.exists(ASS_FILE):
    shutil.copy2(SUBS_SRC, ASS_FILE)

print("=== Fix b2_05 v3 — adicionando legendas no video existente ===")
print(f"  Input: {SRC_NO_SUBS}")
print(f"  ASS:   {ASS_FILE}")

# Move arquivo sem subs para temp
shutil.copy2(SRC_NO_SUBS, TMP_PATH)

# Usa filtro `ass` com path simples C:/Temp/b2v05.ass (sem escapes de colon)
# O filtro `ass` no ffmpeg e mais tolerante que `subtitles` no Windows
ass_fwd = ASS_FILE.replace("\\", "/")  # C:/Temp/b2v05.ass

cmd = [
    "ffmpeg", "-y",
    "-i", TMP_PATH,
    "-vf", f"ass={ass_fwd}",
    "-c:v", "libx264", "-preset", "medium", "-crf", "18",
    "-c:a", "copy",
    OUT_PATH
]

print(f"  Comando: ffmpeg -vf ass={ass_fwd} ...")
r = subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)

if r.returncode != 0:
    stderr_txt = r.stderr.decode(errors="ignore")
    print(f"  ERRO com ass=: {stderr_txt[-400:]}")
    
    # Fallback2: hardcode subtitle com drawtext baseado no ASS (sem filtro ass/subtitles)
    print("\n  Restaurando arquivo sem legendas (melhor que nada)...")
    shutil.copy2(TMP_PATH, OUT_PATH)
    mb = round(os.path.getsize(OUT_PATH)/(1024*1024), 2)
    print(f"  RESULTADO: b2_05 restaurado SEM legendas ({mb} MB)")
    print("  NOTA: Legenda nao foi possivel gravar — problema de compatibilidade ffmpeg/Windows.")
else:
    if os.path.exists(OUT_PATH) and os.path.getsize(OUT_PATH) > 1_000_000:
        mb = round(os.path.getsize(OUT_PATH)/(1024*1024), 2)
        print(f"  SUCCESS com legendas: b2_05_o_sistema_que_estou_construindo.mp4 ({mb} MB)")
    else:
        print("  ARQUIVO NAO ENCONTRADO — restaurando sem legendas...")
        shutil.copy2(TMP_PATH, OUT_PATH)

# Limpeza
if os.path.exists(TMP_PATH): os.remove(TMP_PATH)

print("\nConcluido!")
