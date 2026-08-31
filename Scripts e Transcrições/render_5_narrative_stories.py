"""
Renderizador de Elite: 5 Histórias Narrativas Completas da Live de 3 Horas
Junta trechos não-contíguos da live para criar arcos narrativos com retenção máxima.
Salvamento exclusivo em pasta local para revisão (SEM POSTAR).
"""
import os
import subprocess
import shutil
import sys

sys.stdout.reconfigure(encoding='utf-8')

src_video = r"C:\Users\Kethely\Videos\2026-07-26-09-28-42.mp4"
out_dir = r"C:\Users\Kethely\Downloads\cortes_narrativos_5historias"
os.makedirs(out_dir, exist_ok=True)

scratch_dir = r"C:\Users\Kethely\.gemini\antigravity\brain\9dbd3421-ae5c-4f63-9d99-553453c42d0e\scratch"
subs_dir = os.path.join(scratch_dir, "minimalist_subs_narrativos")
temp_subs_dir = r"C:\Temp\subs_narrativos"
os.makedirs(subs_dir, exist_ok=True)
os.makedirs(temp_subs_dir, exist_ok=True)

# Definição das 5 Histórias Narrativas Completas
stories = [
    {
        "num": 1,
        "name": "historia_01_do_perfume_a_maquina_50k.mp4",
        "sub": "h01.ass",
        "title": "COMECEI COM R$70 E VENDI MAQUINA DE R$50K",
        # 1:05:45-1:06:46 (3945s a 4006s = 61s) + 1:12:23-1:12:46 (4343s a 4366s = 23s) = 84s
        "segments": [
            {"ss": 3945.0, "t": 61.0},
            {"ss": 4343.0, "t": 23.0}
        ],
        "total_t": 84.0,
        "zooms": [(5.0, 20.0), (45.0, 60.0), (70.0, 80.0)],
        "cards": [
            {"s": 0, "e": 10, "text": "Eu ganhava R$70/dia vendendo perfume como freelancer"},
            {"s": 25, "e": 45, "text": "Estudei o negocio e montei minha 1 proposta"},
            {"s": 61, "e": 82, "text": "Resultado: Maquina de R$50 mil vendida com R$100 em ads"}
        ],
        "script_events": [
            (0.0, 6.0, "Eu comecei vendendo perfume como freelancer por R$70 por dia."),
            (6.0, 15.0, "Tenho 20 anos e comecei a trabalhar faz aproximadamente um ano."),
            (15.0, 26.0, "Falei com o dono da loja, apresentei uma ideia de projeto..."),
            (26.0, 36.0, "Fui estudar o negocio dele antes de pedir a reuniao."),
            (36.0, 48.0, "Comecei do zero, as pessoas foram confiando no meu trabalho."),
            (48.0, 61.0, "Meu primeiro canal de aquisicao foi CONFIANCA."),
            (61.0, 72.0, "Depois quis testar se vendia para quem nao me conhecia."),
            (72.0, 84.0, "Fiz tráfego para uma maquina de R$50 mil e vendi gastando R$100!")
        ]
    },
    {
        "num": 2,
        "name": "historia_02_ia_estudar_psicologia_para_construir_ia.mp4",
        "sub": "h02.ass",
        "title": "USAVA IA PRA PSICOLOGIA HOJE USO PRA CRIAR IA",
        # 26:27-28:14 (1587s a 1694s = 107s) + 1:34:25-1:35:03 (5665s a 5703s = 38s) + 1:40:06-1:40:32 (6006s a 6032s = 26s) = 171s
        # Vamos enxugar partes redundantes para focar no arco ideal (~90s total)
        "segments": [
            {"ss": 1587.0, "t": 45.0}, # IA no estudo de Psicologia
            {"ss": 5665.0, "t": 25.0}, # Psicologia criando UX de IA
            {"ss": 6006.0, "t": 20.0}  # Conclusão humana
        ],
        "total_t": 90.0,
        "zooms": [(10.0, 30.0), (50.0, 75.0)],
        "cards": [
            {"s": 0, "e": 12, "text": "Como usava IA para estudar na faculdade de Psicologia"},
            {"s": 45, "e": 65, "text": "Inversao: Usando Psicologia para desenhar sistemas de IA"},
            {"s": 70, "e": 88, "text": "Mas eu ainda tenho muito a aprender!"}
        ],
        "script_events": [
            (0.0, 10.0, "Quando comecei a usar IA na faculdade, eu criava perguntas."),
            (10.0, 22.0, "Minhas notas melhoraram, mas percebi que precisava aprofundar."),
            (22.0, 45.0, "Passei a buscar artigos e pensar em aplicacoes reais."),
            (45.0, 58.0, "Hoje aconteceu uma inversao: uso Psicologia para construir IA!"),
            (58.0, 70.0, "No sistema, penso na jornada e cansaco mental do candidato."),
            (70.0, 90.0, "Nunca imaginei trabalhar com tech, mas juntei o que amo!")
        ]
    },
    {
        "num": 3,
        "name": "historia_03_clientes_baratos_agencia_automatica.mp4",
        "sub": "h03.ass",
        "title": "CLIENTES BARATOS ME FIZERAM AUTOMATIZAR",
        # 42:36-43:14 (2556s a 2594s = 38s) + 44:38-45:53 (2678s a 2753s = 75s) = 113s
        "segments": [
            {"ss": 2678.0, "t": 45.0}, # Desgaste com clientes baratos
            {"ss": 2556.0, "t": 35.0}  # Apresentação do produto automático
        ],
        "total_t": 80.0,
        "zooms": [(12.0, 35.0), (50.0, 75.0)],
        "cards": [
            {"s": 0, "e": 15, "text": "O desgaste de cobrar barato sem escopo definido"},
            {"s": 45, "e": 75, "text": "Solucao: Plataforma que gera 30 dias de conteudo sem perder autenticidade"}
        ],
        "script_events": [
            (0.0, 12.0, "Eu comecei prestando servicos, mas tive um desgaste grande."),
            (12.0, 28.0, "Servico barato parecia comprar minha disponibilidade inteira."),
            (28.0, 45.0, "Amo criar projetos, odeio perder autonomia e responder cobranca."),
            (45.0, 62.0, "Por isso decidi construir uma plataforma de automacao!"),
            (62.0, 80.0, "A empresa coloca dados e recebe posts e videos em 24h.")
        ]
    },
    {
        "num": 4,
        "name": "historia_04_testei_duas_apis_gratuitas_perdi_tempo.mp4",
        "sub": "h04.ass",
        "title": "TESTEI DUAS APIS GRATUITAS E PERDI TEMPO",
        # 1:14:50-1:16:10 (4490s a 4570s = 80s) + 1:47:28-1:49:00 (6448s a 6540s = 72s) -> ~85s enxuto
        "segments": [
            {"ss": 4490.0, "t": 45.0}, # API de vagas falhando
            {"ss": 6448.0, "t": 40.0}  # API financeira falhando
        ],
        "total_t": 85.0,
        "zooms": [(10.0, 35.0), (50.0, 75.0)],
        "cards": [
            {"s": 0, "e": 12, "text": "Teste 1: API de vagas que explicou a profissao"},
            {"s": 45, "e": 65, "text": "Teste 2: API financeira que so servia para empresas de bolsa"},
            {"s": 70, "e": 85, "text": "Gratuito nao e barato quando custa horas de teste"}
        ],
        "script_events": [
            (0.0, 12.0, "Separei varias APIs gratuitas para automatizar meus projetos."),
            (12.0, 28.0, "Na primeira, pedi vagas e ela explicou a profissao!"),
            (28.0, 45.0, "Refiz o pedido e vieram resultados fracos. Nota 4/10."),
            (45.0, 65.0, "Depois fui testar uma API financeira para analisar mercado."),
            (65.0, 85.0, "Descobri que so servia para empresas da Bolsa. Perdi horas de teste!")
        ]
    },
    {
        "num": 5,
        "name": "historia_05_minha_plataforma_esta_pronta_o_problema_sou_eu.mp4",
        "sub": "h05.ass",
        "title": "MINHA PLATAFORMA ESTA PRONTA. O PROBLEMA SOU EU.",
        # 43:34-44:20 (2614s a 2660s = 46s) + 46:06-47:00 (2766s a 2820s = 54s) -> 85s
        "segments": [
            {"ss": 2614.0, "t": 40.0}, # Medo de lançar antes de estar perfeito
            {"ss": 2766.0, "t": 45.0}  # Perfeccionismo x Atraso de lançamento
        ],
        "total_t": 85.0,
        "zooms": [(10.0, 35.0), (50.0, 75.0)],
        "cards": [
            {"s": 0, "e": 15, "text": "A plataforma esta pronta, mas ainda nao lancei por medo"},
            {"s": 40, "e": 70, "text": "O perfeccionismo e o maior inimigo do lancamento"},
            {"s": 72, "e": 85, "text": "Primeiro teste com usuarios reais vindo ai!"}
        ],
        "script_events": [
            (0.0, 15.0, "Estou construindo uma plataforma que cria posts e videos."),
            (15.0, 30.0, "Ela esta quase pronta, mas nao divulguei nem vendi ainda."),
            (30.0, 45.0, "Tenho medo de colocar algo no mercado sem ter certeza que e perfeito."),
            (45.0, 65.0, "Eu sei que ja poderia ter lancado uma versao ha tempo."),
            (65.0, 85.0, "O perfeccionismo esta me atrasando. O problema sou eu!")
        ]
    }
]

# Cabeçalho ASS Kinético elegante
ASS_HEADER = """[Script Info]
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

def format_time(seconds):
    h = int(seconds // 3600)
    m = int((seconds % 3600) // 60)
    s = seconds % 60
    cs = int((s - int(s)) * 100)
    return f"{h}:{m:02d}:{int(s):02d}.{cs:02d}"

print("=" * 60)
print("GERANDO LEGENDAS ASS E RENDERIZANDO AS 5 HISTÓRIAS NARRATIVAS")
print("=" * 60)

for v in stories:
    # 1. Gerar arquivo ASS
    ass_path = os.path.join(subs_dir, v["sub"])
    with open(ass_path, "w", encoding="utf-8") as f:
        f.write(ASS_HEADER)
        for start, end, text in v["script_events"]:
            f.write(f"Dialogue: 0,{format_time(start)},{format_time(end)},Default,,0,0,0,,{text}\n")
    
    # 2. Copia ASS para Temp
    temp_sub = os.path.join(temp_subs_dir, f"sub_h_{v['num']}.ass")
    shutil.copy2(ass_path, temp_sub)
    sub_param = temp_sub.replace("\\", "/").replace(":", "\\:")
    
    # 3. Recortar e Concatenar segmentos da história
    out_path = os.path.join(out_dir, v["name"])
    print(f"\n[{v['num']}/5] Renderizando História Narrativa: {v['name']}")
    
    segs = v["segments"]
    if len(segs) == 1:
        base_clip = os.path.join(out_dir, f"_base_h_{v['num']}.mp4")
        cmd_trim = [
            "ffmpeg", "-y",
            "-ss", str(segs[0]["ss"]), "-i", src_video,
            "-t", str(segs[0]["t"]),
            "-c:v", "libx264", "-preset", "ultrafast", "-crf", "16",
            "-c:a", "aac", "-b:a", "192k",
            base_clip
        ]
        subprocess.run(cmd_trim, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    else:
        tmp_clips = []
        for i, seg in enumerate(segs):
            tmp = os.path.join(out_dir, f"_tmp_h_{v['num']}_{i}.mp4")
            tmp_clips.append(tmp)
            cmd_trim = [
                "ffmpeg", "-y",
                "-ss", str(seg["ss"]), "-i", src_video,
                "-t", str(seg["t"]),
                "-c:v", "libx264", "-preset", "ultrafast", "-crf", "16",
                "-c:a", "aac", "-b:a", "192k",
                tmp
            ]
            subprocess.run(cmd_trim, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        
        concat_list = os.path.join(out_dir, f"_concat_h_{v['num']}.txt")
        with open(concat_list, "w", encoding="utf-8") as f:
            for c in tmp_clips:
                f.write(f"file '{c}'\n")
        
        base_clip = os.path.join(out_dir, f"_base_h_{v['num']}.mp4")
        cmd_concat = [
            "ffmpeg", "-y", "-f", "concat", "-safe", "0",
            "-i", concat_list,
            "-c", "copy",
            base_clip
        ]
        subprocess.run(cmd_concat, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        for tmp in tmp_clips:
            if os.path.exists(tmp): os.remove(tmp)
        if os.path.exists(concat_list): os.remove(concat_list)

    # 4. Filtergraph
    title_text = v["title"].replace("'", "").replace(":", "")
    vf_parts = [
        "crop=ih*9/16:ih:(iw-ih*9/16)/2:0",
        "scale=1080:1920",
    ]
    
    if v["zooms"]:
        zoom_exprs = [f"between(t,{zs},{ze})" for zs, ze in v["zooms"]]
        cond_zoom = "+".join(zoom_exprs)
        vf_parts.append(
            f"scale=eval=frame:w='if({cond_zoom},1166,1080)':h='if({cond_zoom},2073,1920)',crop=1080:1920"
        )
    
    # CARD DE TÍTULO NA ALTURA DA CÂMERA (y=440)
    vf_parts.append("drawbox=y=440:h=96:color=black@0.85:t=fill")
    vf_parts.append("drawbox=y=438:h=2:color=yellow@0.85:t=fill")
    vf_parts.append(
        f"drawtext=fontfile='C\\:/Windows/Fonts/arialbd.ttf':text='{title_text}':fontcolor=white:fontsize=32:x=(w-text_w)/2:y=470"
    )
    
    # POP-INS EDITORIAIS
    for card in v["cards"]:
        c_txt = card["text"].replace("'", "").replace(":", "")
        cs, ce = card["s"], card["e"]
        vf_parts.append(
            f"drawbox=y=550:h=76:color=black@0.75:t=fill:enable='between(t,{cs},{ce})'"
        )
        vf_parts.append(
            f"drawtext=fontfile='C\\:/Windows/Fonts/arial.ttf':text='{c_txt}':fontcolor=yellow:fontsize=26:x=(w-text_w)/2:y=574:enable='between(t,{cs},{ce})'"
        )
        
    vf_parts.append(f"subtitles='{sub_param}'")
    vf_str = ",".join(vf_parts)
    
    cmd_render = [
        "ffmpeg", "-y",
        "-i", base_clip,
        "-vf", vf_str,
        "-af", "loudnorm=I=-16:TP=-1.5:LRA=11",
        "-c:v", "libx264", "-preset", "medium", "-crf", "18",
        "-c:a", "aac", "-b:a", "192k",
        out_path
    ]
    
    res = subprocess.run(cmd_render, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)
    if os.path.exists(base_clip): os.remove(base_clip)
    
    if os.path.exists(out_path) and os.path.getsize(out_path) > 100_000:
        mb = round(os.path.getsize(out_path) / (1024*1024), 2)
        print(f"  SUCCESS: {v['name']} ({mb} MB)")
    else:
        err = res.stderr.decode(errors="ignore")[-300:] if hasattr(res, 'stderr') and res.stderr else ""
        print(f"  ERROR: {v['name']} — {err}")

print("\n" + "=" * 60)
print(f"CONCLUÍDO! As 5 histórias foram geradas na pasta: {out_dir}")
print("Nenhum vídeo foi agendado ou postado.")
print("=" * 60)
