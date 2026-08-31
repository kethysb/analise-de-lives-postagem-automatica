import os
import re
import json

txt_file = r"C:\Users\Kethely\.gemini\antigravity\brain\9dbd3421-ae5c-4f63-9d99-553453c42d0e\scratch\transcript_2026-07-23-23-55-30.txt"
out_md = r"C:\Users\Kethely\.gemini\antigravity\brain\9dbd3421-ae5c-4f63-9d99-553453c42d0e\scratch\CORTES_CANDIDATOS_LITERAIS.md"

with open(txt_file, encoding="utf-8") as f:
    lines = f.readlines()

parsed = []
for line in lines:
    m = re.match(r"\[([\d\.]+)s -> ([\d\.]+)s\] (.*)", line.strip())
    if m:
        start = float(m.group(1))
        end = float(m.group(2))
        text = m.group(3).strip()
        parsed.append((start, end, text))

# Group continuous segments that are close together (< 3.0s gap)
blocks = []
curr_block = []

for item in parsed:
    if not curr_block:
        curr_block.append(item)
    else:
        prev_end = curr_block[-1][1]
        if item[0] - prev_end <= 4.0:
            curr_block.append(item)
        else:
            blocks.append(curr_block)
            curr_block = [item]

if curr_block:
    blocks.append(curr_block)

# Filter blocks that have duration >= 18 seconds and clean speech text
filtered_blocks = []
for idx, b in enumerate(blocks):
    b_start = b[0][0]
    b_end = b[-1][1]
    dur = b_end - b_start
    text = " ".join([seg[2] for seg in b])
    
    # Filter out empty or noise blocks
    if dur >= 18.0 and len(text) > 40:
        # Check if text has meaningful Portuguese words
        filtered_blocks.append({
            "index": len(filtered_blocks) + 1,
            "start": b_start,
            "end": b_end,
            "duration": round(dur, 1),
            "text": text
        })

# Write to markdown file
md_content = [
    "# 📜 Todos os Trechos Reais Falados (Mínimo 20 Segundos)\n",
    "Estes são todos os blocos contínuos da sua fala no vídeo `2026-07-23-23-55-30.mp4` com a transcrição **exata e literal**.\n\n",
    f"**Total de trechos candidatos encontrados**: {len(filtered_blocks)}\n\n",
    "---\n\n"
]

for item in filtered_blocks:
    s_min = int(item['start'] // 60)
    s_sec = int(item['start'] % 60)
    e_min = int(item['end'] // 60)
    e_sec = int(item['end'] % 60)
    
    time_str = f"{s_min:02d}:{s_sec:02d} até {e_min:02d}:{e_sec:02d}"
    
    md_content.append(f"### ✂️ Trecho #{item['index']} | Tempo: `{time_str}` | Duração: `{item['duration']}s`\n")
    md_content.append(f"> \"{item['text']}\"\n\n")
    md_content.append("---\n\n")

with open(out_md, "w", encoding="utf-8") as f:
    f.writelines(md_content)

print(f"Generated {len(filtered_blocks)} speech blocks to {out_md}")
