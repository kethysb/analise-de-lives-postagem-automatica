import subprocess, os

src = r"C:\Users\Kethely\Videos\2026-07-26-09-28-42.mp4"
out_dir = r"C:\Users\Kethely\Downloads\cortes_narrativos_5historias"
out = os.path.join(out_dir, "RAW_historia_01_do_perfume_a_maquina_50k.mp4")

tmp1 = os.path.join(out_dir, "_raw_tmp1.mp4")
tmp2 = os.path.join(out_dir, "_raw_tmp2.mp4")
concat_txt = os.path.join(out_dir, "_raw_concat.txt")

# Seg 1: 1:05:45 -> 1:06:46 (3945s, 61s)
subprocess.run(["ffmpeg", "-y", "-ss", "3945", "-i", src, "-t", "61", "-c", "copy", tmp1],
               stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

# Seg 2: 1:12:23 -> 1:12:46 (4343s, 23s)
subprocess.run(["ffmpeg", "-y", "-ss", "4343", "-i", src, "-t", "23", "-c", "copy", tmp2],
               stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

with open(concat_txt, "w") as f:
    f.write(f"file '{tmp1}'\nfile '{tmp2}'\n")

subprocess.run(["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", concat_txt, "-c", "copy", out],
               stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

for fp in [tmp1, tmp2, concat_txt]:
    if os.path.exists(fp): os.remove(fp)

mb = round(os.path.getsize(out) / (1024*1024), 2) if os.path.exists(out) else 0
print(f"RAW pronto: {out} ({mb} MB)")
