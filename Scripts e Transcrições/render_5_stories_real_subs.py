"""
Extrai as legendas reais da transcrição do Whisper para cada segmento das 5 histórias narrativas,
gera os arquivos ASS com timing correto relativo ao início de cada clipe concatenado,
e re-renderiza os 5 vídeos.
"""
import re
import os
import subprocess
import shutil
import sys

sys.stdout.reconfigure(encoding='utf-8')

TRANSCRIPT_PATH = r"C:\Users\Kethely\.gemini\antigravity\brain\9dbd3421-ae5c-4f63-9d99-553453c42d0e\scratch\transcricao_completa_2026-07-26-09-28-42.md"
SRC_VIDEO = r"C:\Users\Kethely\Videos\2026-07-26-09-28-42.mp4"
OUT_DIR = r"C:\Users\Kethely\Downloads\cortes_narrativos_5historias"
SUBS_DIR = r"C:\Users\Kethely\.gemini\antigravity\brain\9dbd3421-ae5c-4f63-9d99-553453c42d0e\scratch\minimalist_subs_narrativos"
TEMP_DIR = r"C:\Temp\subs_narrativos"

os.makedirs(OUT_DIR, exist_ok=True)
os.makedirs(SUBS_DIR, exist_ok=True)
os.makedirs(TEMP_DIR, exist_ok=True)

# ─── Parse transcript ───────────────────────────────────────────────────────
def ts_to_sec(ts_str):
    """Converte HH:MM:SS ou MM:SS para segundos float."""
    parts = ts_str.strip().split(":")
    if len(parts) == 3:
        return int(parts[0]) * 3600 + int(parts[1]) * 60 + float(parts[2])
    elif len(parts) == 2:
        return int(parts[0]) * 60 + float(parts[1])
    return float(parts[0])

def parse_transcript(path):
    """Retorna lista de (start_sec, end_sec, text)."""
    entries = []
    pattern = re.compile(r"\*\*\[(\d+:\d+(?::\d+)?)\s*->\s*(\d+:\d+(?::\d+)?)\]\*\*\s*(.*)")
    with open(path, encoding="utf-8") as f:
        for line in f:
            m = pattern.match(line.strip())
            if m:
                s = ts_to_sec(m.group(1))
                e = ts_to_sec(m.group(2))
                txt = m.group(3).strip()
                if txt and txt != "...":
                    entries.append((s, e, txt))
    return entries

print("Lendo transcrição completa...")
transcript = parse_transcript(TRANSCRIPT_PATH)
print(f"  {len(transcript)} segmentos de fala encontrados.")

# ─── Extrai legendas para um conjunto de segmentos ───────────────────────────
def extract_subs_for_segments(segments, transcript):
    """
    Dado segmentos [(ss, t), ...], extrai os entries do transcript que se sobrepõem
    e retorna lista de (start_rel, end_rel, text) com timestamps relativos ao clipe.
    """
    events = []
    clip_offset = 0.0
    for seg in segments:
        seg_start = seg["ss"]
        seg_end = seg["ss"] + seg["t"]
        for (ts, te, txt) in transcript:
            if te <= seg_start or ts >= seg_end:
                continue
            # Clipa dentro do segmento
            rel_s = max(ts, seg_start) - seg_start + clip_offset
            rel_e = min(te, seg_end) - seg_start + clip_offset
            if rel_e > rel_s:
                events.append((rel_s, rel_e, txt))
        clip_offset += seg["t"]
    return events

# ─── ASS Format ──────────────────────────────────────────────────────────────
ASS_HEADER = """\
[Script Info]
ScriptType: v4.00+
PlayResX: 1080
PlayResY: 1920
ScaledBorderAndShadow: yes

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Default,Arial,58,&H00FFFFFF,&H0000FFFF,&H00000000,&H80000000,1,0,0,0,100,100,0,0,1,3,0,2,80,80,360,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""

def fmt_t(sec):
    h = int(sec // 3600)
    m = int((sec % 3600) // 60)
    s = sec % 60
    cs = int((s - int(s)) * 100)
    return f"{h}:{m:02d}:{int(s):02d}.{cs:02d}"

def write_ass(path, events):
    with open(path, "w", encoding="utf-8") as f:
        f.write(ASS_HEADER)
        for (s, e, txt) in events:
            # Limpa o texto para ASS
            clean = txt.replace("{", "").replace("}", "").replace("\n", " ")
            f.write(f"Dialogue: 0,{fmt_t(s)},{fmt_t(e)},Default,,0,0,0,,{clean}\n")
    print(f"  ASS gerado: {os.path.basename(path)} ({len(events)} linhas)")

# ─── Definição das 5 histórias ───────────────────────────────────────────────
stories = [
    {
        "num": 1,
        "name": "historia_01_do_perfume_a_maquina_50k.mp4",
        "sub": "h01.ass",
        "title": "COMECEI COM R$70 E VENDI MAQUINA DE R$50K",
        "segments": [
            {"ss": 3945.0, "t": 61.0},
            {"ss": 4343.0, "t": 23.0},
        ],
        "zooms": [(5.0, 20.0), (45.0, 60.0), (70.0, 80.0)],
        "cards": [
            {"s": 0,  "e": 12, "text": "Eu ganhava R$70/dia vendendo perfume como freelancer"},
            {"s": 25, "e": 50, "text": "Estudei o negocio e montei minha 1a proposta"},
            {"s": 61, "e": 82, "text": "Maquina de R$50 mil vendida com R$100 em ads"},
        ],
    },
    {
        "num": 2,
        "name": "historia_02_ia_estudar_psicologia_para_construir_ia.mp4",
        "sub": "h02.ass",
        "title": "USAVA IA PRA PSICOLOGIA HOJE USO PRA CRIAR IA",
        "segments": [
            {"ss": 1587.0, "t": 45.0},
            {"ss": 5665.0, "t": 25.0},
            {"ss": 6006.0, "t": 20.0},
        ],
        "zooms": [(10.0, 30.0), (50.0, 75.0)],
        "cards": [
            {"s": 0,  "e": 15, "text": "Como usava IA para estudar na faculdade de Psicologia"},
            {"s": 45, "e": 65, "text": "Inversao: Usando Psicologia para desenhar sistemas de IA"},
            {"s": 70, "e": 88, "text": "Mas eu ainda tenho muito a aprender!"},
        ],
    },
    {
        "num": 3,
        "name": "historia_03_clientes_baratos_agencia_automatica.mp4",
        "sub": "h03.ass",
        "title": "CLIENTES BARATOS ME FIZERAM AUTOMATIZAR",
        "segments": [
            {"ss": 2678.0, "t": 45.0},
            {"ss": 2556.0, "t": 35.0},
        ],
        "zooms": [(12.0, 35.0), (50.0, 75.0)],
        "cards": [
            {"s": 0,  "e": 15, "text": "O desgaste de cobrar barato sem escopo definido"},
            {"s": 45, "e": 75, "text": "Solucao: Plataforma que gera 30 dias de conteudo"},
        ],
    },
    {
        "num": 4,
        "name": "historia_04_testei_duas_apis_gratuitas_perdi_tempo.mp4",
        "sub": "h04.ass",
        "title": "TESTEI DUAS APIS GRATUITAS E PERDI TEMPO",
        "segments": [
            {"ss": 4490.0, "t": 45.0},
            {"ss": 6448.0, "t": 40.0},
        ],
        "zooms": [(10.0, 35.0), (50.0, 75.0)],
        "cards": [
            {"s": 0,  "e": 12, "text": "Teste 1: API de vagas que explicou a profissao"},
            {"s": 45, "e": 65, "text": "Teste 2: API financeira so para empresas de bolsa"},
            {"s": 70, "e": 83, "text": "Gratuito nao e barato quando custa horas de teste"},
        ],
    },
    {
        "num": 5,
        "name": "historia_05_minha_plataforma_esta_pronta_o_problema_sou_eu.mp4",
        "sub": "h05.ass",
        "title": "MINHA PLATAFORMA ESTA PRONTA. O PROBLEMA SOU EU.",
        "segments": [
            {"ss": 2614.0, "t": 40.0},
            {"ss": 2766.0, "t": 45.0},
        ],
        "zooms": [(10.0, 35.0), (50.0, 75.0)],
        "cards": [
            {"s": 0,  "e": 15, "text": "A plataforma esta pronta mas ainda nao lancei"},
            {"s": 40, "e": 70, "text": "O perfeccionismo e o maior inimigo do lancamento"},
            {"s": 72, "e": 83, "text": "Primeiro teste com usuarios reais vindo ai!"},
        ],
    },
]

# ─── Render ──────────────────────────────────────────────────────────────────
print("\n" + "=" * 60)
print("GERANDO ASS REAIS E RE-RENDERIZANDO AS 5 HISTÓRIAS")
print("=" * 60)

ok = 0
for v in stories:
    print(f"\n[{v['num']}/5] {v['name']}")

    # 1. Gera ASS com transcrição real
    events = extract_subs_for_segments(v["segments"], transcript)
    ass_path = os.path.join(SUBS_DIR, v["sub"])
    write_ass(ass_path, events)

    temp_sub = os.path.join(TEMP_DIR, f"h{v['num']}.ass")
    shutil.copy2(ass_path, temp_sub)
    sub_param = temp_sub.replace("\\", "/").replace(":", "\\:")

    # 2. Corta e concatena segmentos
    segs = v["segments"]
    if len(segs) == 1:
        base_clip = os.path.join(OUT_DIR, f"_base_h{v['num']}.mp4")
        subprocess.run([
            "ffmpeg", "-y", "-ss", str(segs[0]["ss"]), "-i", SRC_VIDEO,
            "-t", str(segs[0]["t"]),
            "-c:v", "libx264", "-preset", "ultrafast", "-crf", "16",
            "-c:a", "aac", "-b:a", "192k", base_clip
        ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    else:
        tmp_clips = []
        for i, seg in enumerate(segs):
            tmp = os.path.join(OUT_DIR, f"_tmp_h{v['num']}_{i}.mp4")
            tmp_clips.append(tmp)
            subprocess.run([
                "ffmpeg", "-y", "-ss", str(seg["ss"]), "-i", SRC_VIDEO,
                "-t", str(seg["t"]),
                "-c:v", "libx264", "-preset", "ultrafast", "-crf", "16",
                "-c:a", "aac", "-b:a", "192k", tmp
            ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

        concat_list = os.path.join(OUT_DIR, f"_concat_h{v['num']}.txt")
        with open(concat_list, "w", encoding="utf-8") as f:
            for c in tmp_clips:
                f.write(f"file '{c}'\n")

        base_clip = os.path.join(OUT_DIR, f"_base_h{v['num']}.mp4")
        subprocess.run([
            "ffmpeg", "-y", "-f", "concat", "-safe", "0",
            "-i", concat_list, "-c", "copy", base_clip
        ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        for tmp in tmp_clips:
            if os.path.exists(tmp): os.remove(tmp)
        os.remove(concat_list)

    # 3. Filtergraph com legendas reais
    title_text = v["title"].replace("'", "").replace(":", "")
    vf = [
        "crop=ih*9/16:ih:(iw-ih*9/16)/2:0",
        "scale=1080:1920",
    ]

    if v["zooms"]:
        cond = "+".join(f"between(t,{zs},{ze})" for zs, ze in v["zooms"])
        vf.append(f"scale=eval=frame:w='if({cond},1166,1080)':h='if({cond},2073,1920)',crop=1080:1920")

    vf += [
        "drawbox=y=440:h=96:color=black@0.85:t=fill",
        "drawbox=y=438:h=2:color=yellow@0.85:t=fill",
        f"drawtext=fontfile='C\\:/Windows/Fonts/arialbd.ttf':text='{title_text}':fontcolor=white:fontsize=30:x=(w-text_w)/2:y=470",
    ]

    for card in v["cards"]:
        c_txt = card["text"].replace("'", "").replace(":", "")
        cs, ce = card["s"], card["e"]
        vf.append(f"drawbox=y=550:h=76:color=black@0.75:t=fill:enable='between(t,{cs},{ce})'")
        vf.append(f"drawtext=fontfile='C\\:/Windows/Fonts/arial.ttf':text='{c_txt}':fontcolor=yellow:fontsize=25:x=(w-text_w)/2:y=574:enable='between(t,{cs},{ce})'")

    vf.append(f"subtitles='{sub_param}'")

    out_path = os.path.join(OUT_DIR, v["name"])
    res = subprocess.run([
        "ffmpeg", "-y", "-i", base_clip,
        "-vf", ",".join(vf),
        "-af", "loudnorm=I=-16:TP=-1.5:LRA=11",
        "-c:v", "libx264", "-preset", "medium", "-crf", "18",
        "-c:a", "aac", "-b:a", "192k",
        out_path
    ], stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)

    if os.path.exists(base_clip): os.remove(base_clip)

    if os.path.exists(out_path) and os.path.getsize(out_path) > 100_000:
        mb = round(os.path.getsize(out_path) / (1024 * 1024), 2)
        print(f"  SUCCESS: {v['name']} ({mb} MB)")
        ok += 1
    else:
        err = res.stderr.decode(errors="ignore")[-400:] if res.stderr else ""
        print(f"  ERROR: {err}")

print("\n" + "=" * 60)
print(f"CONCLUÍDO: {ok}/5 vídeos re-renderizados com legendas REAIS")
print(f"Pasta: {OUT_DIR}")
print("Nenhum vídeo foi postado.")
print("=" * 60)
