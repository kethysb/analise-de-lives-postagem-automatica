import os
import subprocess
import sys

sys.stdout.reconfigure(encoding='utf-8')

src_video = r"C:\Users\Kethely\Videos\2026-07-26-09-28-42.mp4"
out_dir = r"C:\Users\Kethely\Downloads\cortes_bloco2_editados"
os.makedirs(out_dir, exist_ok=True)

scratch_dir = r"C:\Users\Kethely\.gemini\antigravity\brain\9dbd3421-ae5c-4f63-9d99-553453c42d0e\scratch"
subs_dir = os.path.join(scratch_dir, "minimalist_subs_bloco2")

# ─────────────────────────────────────────────────────────────────────────────
# TIMESTAMPS (segundos a partir do início do arquivo de vídeo fonte)
# Bloco: 30:03 a 1:05:10
# ─────────────────────────────────────────────────────────────────────────────
# Nota: os segmentos com múltiplos trechos são concatenados via concat na edição
# Para simplicidade e qualidade, usamos o trecho principal + corte manual via -ss/-t
# Quando há pulo no meio, usa-se concat de dois trims.
# ─────────────────────────────────────────────────────────────────────────────

videos = [
    {
        "num": 1,
        "name": "b2_01_o_problema_nao_era_cobrar_barato.mp4",
        "sub": "b2_v01.ass",
        # Segmento 1: 45:14–45:53 (39s) + Segmento 2: 47:54–48:06 (12s) = 51s
        "segments": [
            {"ss": 45*60+14, "t": 39},
            {"ss": 47*60+54, "t": 12},
        ],
        "total_t": 51,
        "title": "O PROBLEMA NAO ERA COBRAR BARATO",
        "zooms": [(4.0, 17.0), (35.0, 51.0)],
        "cards": [
            {"s": 0,  "e": 4,  "text": "Cobrar barato nao foi meu maior erro."},
            {"s": 17, "e": 35, "text": "R$300-R$400  /  Sem escopo = disponibilidade infinita"},
        ]
    },
    {
        "num": 2,
        "name": "b2_02_eu_amo_trabalhar_mas_odeio_ser_cobrada.mp4",
        "sub": "b2_v02.ass",
        # Segmento: 48:12–49:14 (62s)
        "segments": [
            {"ss": 48*60+12, "t": 62},
        ],
        "total_t": 62,
        "title": "EU NAO QUERO PARAR DE TRABALHAR",
        "zooms": [(8.0, 20.0), (42.0, 55.0)],
        "cards": [
            {"s": 0,  "e": 8,  "text": "Eu nao quero trabalhar menos. Quero parar de ser controlada."},
            {"s": 20, "e": 42, "text": "Automatizo um projeto  ->  Invento outro"},
        ]
    },
    {
        "num": 3,
        "name": "b2_03_por_que_sistemas_em_nuvem_sao_caros.mp4",
        "sub": "b2_v03.ass",
        # Segmento 1: 39:36–40:12 (36s) + Segmento 2: 40:18–40:40 (22s) = 58s
        "segments": [
            {"ss": 39*60+36, "t": 36},
            {"ss": 40*60+18, "t": 22},
        ],
        "total_t": 58,
        "title": "SO ENTENDI POR QUE NUVEM E CARO QUANDO CONSTRUI UM",
        "zooms": [(8.0, 25.0), (39.0, 58.0)],
        "cards": [
            {"s": 0,  "e": 8,  "text": "Eu achava caro ate sentir a responsabilidade."},
            {"s": 25, "e": 39, "text": "Falha no sistema  ->  Dados fora de sincronia"},
        ]
    },
    {
        "num": 4,
        "name": "b2_04_o_medo_de_lancar_esta_me_atrasando.mp4",
        "sub": "b2_v04.ass",
        # Segmento 1: 44:38–45:14 (36s) + 46:06–46:20 (14s) + 47:00–47:20 (20s) = 70s
        "segments": [
            {"ss": 44*60+38, "t": 36},
            {"ss": 46*60+6,  "t": 14},
            {"ss": 47*60+0,  "t": 20},
        ],
        "total_t": 70,
        "title": "EU JA PODERIA TER LANCADO. NAO LANCEI POR ISSO.",
        "zooms": [(10.0, 30.0), (50.0, 70.0)],
        "cards": [
            {"s": 0,  "e": 10, "text": "O medo de entregar algo ruim esta atrasando meu projeto."},
            {"s": 30, "e": 50, "text": "Ja poderia ter lancado  X  Ainda pode melhorar"},
        ]
    },
    {
        "num": 5,
        "name": "b2_05_o_sistema_que_estou_construindo.mp4",
        "sub": "b2_v05.ass",
        # Segmento 1: 42:32–43:14 (42s) + 49:28–49:52 (24s) = 66s
        "segments": [
            {"ss": 42*60+32, "t": 42},
            {"ss": 49*60+28, "t": 24},
        ],
        "total_t": 66,
        "title": "O SISTEMA QUE ESTOU CONSTRUINDO",
        "zooms": [(6.0, 20.0), (38.0, 55.0)],
        "cards": [
            {"s": 0,  "e": 6,  "text": "Dados da empresa  ->  30 posts + 30 videos em 24h"},
            {"s": 20, "e": 38, "text": "O desafio: automatico sem parecer generico"},
        ]
    },
    {
        "num": 6,
        "name": "b2_06_como_estudar_virais_sem_copiar.mp4",
        "sub": "b2_v06.ass",
        # Segmento 1: 50:04–50:18 (14s) + Segmento 2: 50:32–51:16 (44s) = 58s
        "segments": [
            {"ss": 50*60+4,  "t": 14},
            {"ss": 50*60+32, "t": 44},
        ],
        "total_t": 58,
        "title": "COMO ESTUDAR VIRAIS SEM COPIAR",
        "zooms": [(14.0, 34.0)],
        "cards": [
            {"s": 0,  "e": 14, "text": "Copiar um viral nao e estrategia. Entender o padrao pode ser."},
            {"s": 34, "e": 52, "text": "Gancho  •  Ritmo  •  Tema  •  Formato  •  Fechamento"},
        ]
    },
    {
        "num": 7,
        "name": "b2_07_antes_de_criar_um_app_faca_isso.mp4",
        "sub": "b2_v07.ass",
        # Segmento: 1:00:10–1:00:46 (36s)
        "segments": [
            {"ss": 60*60+10, "t": 36},
        ],
        "total_t": 36,
        "title": "SUA IDEIA DE APLICATIVO E BOA?",
        "zooms": [(12.0, 32.0)],
        "cards": [
            {"s": 0,  "e": 12, "text": "Primeiro, estude o mercado."},
            {"s": 12, "e": 36, "text": "Ja existe?  Quem usa?  Quanto custa?  O que reclamam?"},
        ]
    },
    {
        "num": 8,
        "name": "b2_r01_nunca_trabalhei_clt.mp4",
        "sub": "b2_r01.ass",
        # Segmento: 31:58–32:48 (50s)
        "segments": [
            {"ss": 31*60+58, "t": 50},
        ],
        "total_t": 50,
        "title": "NUNCA TRABALHEI CLT - E ISSO ME DA MEDO",
        "zooms": [(18.0, 32.0)],
        "cards": [
            {"s": 0,  "e": 12, "text": "Liberdade agora ou seguranca para depois?"},
            {"s": 32, "e": 50, "text": "Empreender tambem e conviver com essa duvida."},
        ]
    },
    {
        "num": 9,
        "name": "b2_r02_o_erro_de_seguranca_que_cometo.mp4",
        "sub": "b2_r02.ass",
        # Segmento 1: 1:01:18–1:01:26 (8s) + 1:01:30–1:01:48 (18s) = 26s
        "segments": [
            {"ss": 61*60+18, "t": 8},
            {"ss": 61*60+30, "t": 18},
        ],
        "total_t": 26,
        "title": "EU JA FUI HACKEADA POR FAZER ISSO",
        "zooms": [(5.0, 17.0)],
        "cards": [
            {"s": 0, "e": 5,  "text": "NAO faca isso sem isolamento e verificacao."},
            {"s": 5, "e": 22, "text": "Autenticacao em 2 fatores ajudou na recuperacao"},
        ]
    },
]


def render_video(v):
    """Render a video. Multi-segment videos are concatenated via complex filtergraph."""
    out_path = os.path.join(out_dir, v["name"])
    ass_path = os.path.join(subs_dir, v["sub"]).replace("\\", "/")
    ass_escaped = ass_path.replace(":", "\\:")
    title_text = v["title"]

    print(f"\n[{v['num']}/9] Rendering: {v['name']}")

    segs = v["segments"]

    if len(segs) == 1:
        # ── Single segment: simple -ss -t approach ────────────────────────
        ss = segs[0]["ss"]
        t  = segs[0]["t"]

        vf_chain = [
            "crop=ih*9/16:ih:(iw-ih*9/16)/2:0",
            "scale=1080:1920",
        ]

        # Focus Zoom
        if v["zooms"]:
            zoom_exprs = [f"between(t,{zs},{ze})" for zs, ze in v["zooms"]]
            cond_zoom = "+".join(zoom_exprs)
            vf_chain.append(
                f"scale=eval=frame:w='if({cond_zoom},1166,1080)':h='if({cond_zoom},2073,1920)',crop=1080:1920"
            )

        # Header title
        vf_chain.append("drawbox=y=110:h=110:color=black@0.80:t=fill")
        vf_chain.append(
            f"drawtext=fontfile='C\\:/Windows/Fonts/arialbd.ttf':text='{title_text}':fontcolor=white:fontsize=36:x=(w-text_w)/2:y=150"
        )

        # Editorial cards
        for card in v["cards"]:
            c_txt = card["text"]
            cs, ce = card["s"], card["e"]
            vf_chain.append(
                f"drawbox=y=370:h=86:color=black@0.75:t=fill:enable='between(t,{cs},{ce})'"
            )
            vf_chain.append(
                f"drawtext=fontfile='C\\:/Windows/Fonts/arial.ttf':text='{c_txt}':fontcolor=white:fontsize=32:x=(w-text_w)/2:y=396:enable='between(t,{cs},{ce})'"
            )

        # Subtitles
        vf_chain.append(f"subtitles='{ass_escaped}'")

        vf_str = ",".join(vf_chain)

        cmd = [
            "ffmpeg", "-y",
            "-ss", str(ss), "-i", src_video,
            "-t", str(t),
            "-vf", vf_str,
            "-af", "loudnorm=I=-16:TP=-1.5:LRA=11",
            "-c:v", "libx264", "-preset", "medium", "-crf", "18",
            "-c:a", "aac", "-b:a", "192k",
            out_path
        ]
        res = subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)

    else:
        # ── Multi-segment: build temp clips, concat, then apply effects ───
        tmp_clips = []
        for i, seg in enumerate(segs):
            tmp = os.path.join(out_dir, f"_tmp_{v['num']}_{i}.mp4")
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

        # Write concat list
        concat_list = os.path.join(out_dir, f"_concat_{v['num']}.txt")
        with open(concat_list, "w") as f:
            for c in tmp_clips:
                f.write(f"file '{c}'\n")

        # Concat to intermediate
        concat_out = os.path.join(out_dir, f"_joined_{v['num']}.mp4")
        cmd_concat = [
            "ffmpeg", "-y", "-f", "concat", "-safe", "0",
            "-i", concat_list,
            "-c", "copy",
            concat_out
        ]
        subprocess.run(cmd_concat, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

        # Now apply full VF chain on the joined clip
        vf_chain = [
            "crop=ih*9/16:ih:(iw-ih*9/16)/2:0",
            "scale=1080:1920",
        ]

        if v["zooms"]:
            zoom_exprs = [f"between(t,{zs},{ze})" for zs, ze in v["zooms"]]
            cond_zoom = "+".join(zoom_exprs)
            vf_chain.append(
                f"scale=eval=frame:w='if({cond_zoom},1166,1080)':h='if({cond_zoom},2073,1920)',crop=1080:1920"
            )

        vf_chain.append("drawbox=y=110:h=110:color=black@0.80:t=fill")
        vf_chain.append(
            f"drawtext=fontfile='C\\:/Windows/Fonts/arialbd.ttf':text='{title_text}':fontcolor=white:fontsize=36:x=(w-text_w)/2:y=150"
        )

        for card in v["cards"]:
            c_txt = card["text"]
            cs, ce = card["s"], card["e"]
            vf_chain.append(
                f"drawbox=y=370:h=86:color=black@0.75:t=fill:enable='between(t,{cs},{ce})'"
            )
            vf_chain.append(
                f"drawtext=fontfile='C\\:/Windows/Fonts/arial.ttf':text='{c_txt}':fontcolor=white:fontsize=32:x=(w-text_w)/2:y=396:enable='between(t,{cs},{ce})'"
            )

        vf_chain.append(f"subtitles='{ass_escaped}'")

        vf_str = ",".join(vf_chain)

        cmd = [
            "ffmpeg", "-y",
            "-i", concat_out,
            "-t", str(v["total_t"]),
            "-vf", vf_str,
            "-af", "loudnorm=I=-16:TP=-1.5:LRA=11",
            "-c:v", "libx264", "-preset", "medium", "-crf", "18",
            "-c:a", "aac", "-b:a", "192k",
            out_path
        ]
        res = subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)

        # Cleanup temp files
        for tmp in tmp_clips:
            if os.path.exists(tmp): os.remove(tmp)
        if os.path.exists(concat_out): os.remove(concat_out)
        if os.path.exists(concat_list): os.remove(concat_list)

    if os.path.exists(out_path) and os.path.getsize(out_path) > 100_000:
        mb = round(os.path.getsize(out_path) / (1024*1024), 2)
        print(f"  SUCCESS: {v['name']} ({mb} MB)")
        return True
    else:
        err = res.stderr.decode(errors="ignore")[-300:] if hasattr(res, 'stderr') and res.stderr else ""
        print(f"  ERROR: {v['name']} — {err}")
        return False


print("=" * 60)
print("BLOCO 2 — 9 VIDEOS HUMAN-CRAFTED RENDER")
print("=" * 60)

ok, fail = 0, 0
for v in videos:
    if render_video(v):
        ok += 1
    else:
        fail += 1

print("\n" + "=" * 60)
print(f"RESULTADO FINAL: {ok}/9 renderizados com sucesso | {fail} falhas")
print(f"Pasta de saída: {out_dir}")
print("=" * 60)
