import os
import re

txt_src = r"C:\Users\Kethely\.gemini\antigravity\brain\9dbd3421-ae5c-4f63-9d99-553453c42d0e\scratch\transcript_2026-07-23-23-55-30.txt"
md_out = r"C:\Users\Kethely\.gemini\antigravity\brain\9dbd3421-ae5c-4f63-9d99-553453c42d0e\scratch\TRANSCRIÇÃO_INTEGRA_SEM_RETICENCIAS.md"

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

def get_block_text(start_sec, end_sec):
    return " ".join([p[2] for p in parsed if start_sec <= p[0] <= end_sec])

content = [
    "# 📜 Transcrição 100% Íntegra Sem Nenhuma Reticência (...) ou Corte\n\n",
    "## 📌 BLOCO 1: Transição de Psicologia para IA, Aprendizado Autônomo e Mudança de Vida (Tempo: 50:00 até 65:00)\n\n",
    get_block_text(3000, 3900),
    "\n\n---\n\n",
    "## 📌 BLOCO 2: Como Funcionam os Vouchers/Créditos de IA para Startups, Segurança de Dados e Preços (Tempo: 11:40 até 30:00)\n\n",
    get_block_text(700, 1800),
    "\n\n---\n\n",
    "## 📌 BLOCO 3: Criando Ferramentas de Análise do TikTok, Uso do Gemini e Comunidade (Tempo: 66:40 até 80:00)\n\n",
    get_block_text(4000, 4800),
    "\n\n---\n\n"
]

with open(md_out, "w", encoding="utf-8") as f:
    f.writelines(content)

print("File written successfully!")
