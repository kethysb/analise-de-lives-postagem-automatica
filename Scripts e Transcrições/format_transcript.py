import os
import json
import re

txt_src = r"C:\Users\Kethely\.gemini\antigravity\brain\9dbd3421-ae5c-4f63-9d99-553453c42d0e\scratch\transcript_2026-07-23-23-55-30.txt"
md_out = r"C:\Users\Kethely\.gemini\antigravity\brain\9dbd3421-ae5c-4f63-9d99-553453c42d0e\scratch\transcricao_completa_2026-07-23-23-55-30.md"

with open(txt_src, encoding="utf-8") as f:
    lines = f.readlines()

output_lines = [
    "# 📜 Transcrição Completa e Literal: Video `2026-07-23-23-55-30.mp4`\n",
    "**Duração total**: 1h 33m 43s\n",
    "---\n\n"
]

current_block = []
block_start = 0

for line in lines:
    m = re.match(r"\[([\d\.]+)s -> ([\d\.]+)s\] (.*)", line.strip())
    if m:
        s = float(m.group(1))
        e = float(m.group(2))
        t = m.group(3).strip()
        
        # Format time as MM:SS
        m_s = int(s // 60)
        sec_s = int(s % 60)
        time_tag = f"{m_s:02d}:{sec_s:02d}"
        
        output_lines.append(f"`[{time_tag}]` {t}\n")

with open(md_out, "w", encoding="utf-8") as f:
    f.writelines(output_lines)

print(f"Full markdown transcript written to {md_out}")
