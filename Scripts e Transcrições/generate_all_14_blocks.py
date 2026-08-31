import os
import re

txt_src = r"C:\Users\Kethely\.gemini\antigravity\brain\9dbd3421-ae5c-4f63-9d99-553453c42d0e\scratch\transcript_2026-07-23-23-55-30.txt"
md_out = r"C:\Users\Kethely\.gemini\antigravity\brain\9dbd3421-ae5c-4f63-9d99-553453c42d0e\scratch\TODOS_OS_14_BLOCOS_LITERAIS_INTEGRAIS.md"

with open(txt_src, encoding="utf-8") as f:
    lines = f.readlines()

parsed = []
for line in lines:
    m = re.match(r"\[([\d\.]+)s -> ([\d\.]+)s\] (.*)", line.strip())
    if m:
        start = float(m.group(1))
        end = float(m.group(2))
        text = m.group(3).strip()
        parsed.append((start, end, text))

# Group into blocks of continuous speech
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

filtered_blocks = []
for b in blocks:
    b_start = b[0][0]
    b_end = b[-1][1]
    dur = b_end - b_start
    text = " ".join([seg[2] for seg in b])
    if dur >= 18.0 and len(text) > 40:
        filtered_blocks.append({
            "start": b_start,
            "end": b_end,
            "dur": round(dur, 1),
            "text": text
        })

content = [
    "# 📜 Todos os 14 Trechos Literais de Fala Inteiros (Sem Reticências)\n\n"
]

for idx, b in enumerate(filtered_blocks, 1):
    s_min, s_sec = int(b['start'] // 60), int(b['start'] % 60)
    e_min, e_sec = int(b['end'] // 60), int(b['end'] % 60)
    content.append(f"### ✂️ TRECHO #{idx:02d} | Tempo: `{s_min:02d}:{s_sec:02d} até {e_min:02d}:{e_sec:02d}` | Duração: `{b['dur']}s`\n\n")
    content.append(b['text'] + "\n\n")
    content.append("---\n\n")

with open(md_out, "w", encoding="utf-8") as f:
    f.writelines(content)

print(f"Successfully generated {len(filtered_blocks)} complete untruncated blocks into {md_out}")
