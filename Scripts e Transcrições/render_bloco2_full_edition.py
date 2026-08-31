"""
Renderizador Bloco 2 - Edição Avançada Human-Crafted com Legendas Kinetic ASS
- Aplica legendas ASS com destaque em tempo real palavra por palavra
- Aplica enquadramento multi-câmera (Focus Zoom 100% -> 108%)
- Título posicionado na base do enquadramento superior da câmera (y=450)
- Trata caminho de legendas para compatibilidade total ffmpeg Windows
"""
import os
import subprocess
import shutil
import sys

sys.stdout.reconfigure(encoding='utf-8')

src_video = r"C:\Users\Kethely\Videos\2026-07-26-09-28-42.mp4"
out_dir = r"C:\Users\Kethely\Downloads\cortes_bloco2_editados"
os.makedirs(out_dir, exist_ok=True)

scratch_dir = r"C:\Users\Kethely\.gemini\antigravity\brain\9dbd3421-ae5c-4f63-9d99-553453c42d0e\scratch"
subs_dir = os.path.join(scratch_dir, "minimalist_subs_bloco2")
temp_subs_dir = r"C:\Temp\subs_b2"
os.makedirs(temp_subs_dir, exist_ok=True)

videos = [
    {
        "num": 1,
        "name": "b2_01_o_problema_nao_era_cobrar_barato.mp4",
        "sub": "b2_v01.ass",
        "segments": [{"ss": 1002.0, "t": 62.0}],
        "total_t": 62.0,
        "title": "O PROBLEMA NÂO ERA COBRAR BARATO",
        "zooms": [(4.0, 14.0), (25.0, 45.0)],
        "cards": [
            {"s": 0, "e": 4, "text": "Dá para ganhar bem com esse conhecimento?"},
            {"s": 14, "e": 25, "text": "2 DIAS  ->  10 MINUTOS"}
        ]
    },
    {
        "num": 2,
        "name": "b2_02_eu_amo_trabalhar_mas_odeio_ser_cobrada.mp4",
        "sub": "b2_v02.ass",
        "segments": [{"ss": 1104.0, "t": 34.0}],
        "total_t": 34.0,
        "title": "EU AMO TRABALHAR, MAS ODEIO SER COBRADA",
        "zooms": [(3.0, 14.0)],
        "cards": [
            {"s": 3, "e": 14, "text": "O almoço grátis não vai ser para sempre"},
            {"s": 14, "e": 28, "text": "IA para construir | Automação para manter"}
        ]
    },
    {
        "num": 3,
        "name": "b2_03_por_que_sistemas_em_nuvem_sao_caros.mp4",
        "sub": "b2_v03.ass",
        "segments": [{"ss": 1290.0, "t": 40.0}],
        "total_t": 40.0,
        "title": "POR QUE SISTEMAS EM NUVEM SÃO CAROS?",
        "zooms": [(8.0, 25.0)],
        "cards": [
            {"s": 0, "e": 8, "text": "A diferença entre um app simples e um sistema real"},
            {"s": 25, "e": 38, "text": "Infraestrutura -> Segurança -> Disponibilidade"}
        ]
    },
    {
        "num": 4,
        "name": "b2_04_o_medo_de_lancar_esta_me_atrasando.mp4",
        "sub": "b2_v04.ass",
        "segments": [{"ss": 1410.0, "t": 70.0}],
        "total_t": 70.0,
        "title": "EU JÁ PODERIA TER LANÇADO. NÃO LANÇEI POR ISSO.",
        "zooms": [(10.0, 30.0), (50.0, 70.0)],
        "cards": [
            {"s": 0, "e": 10, "text": "O medo de entregar algo ruim está atrasando meu projeto."},
            {"s": 30, "e": 50, "text": "Já poderia ter lançado  VS  Ainda pode melhorar"}
        ]
    },
    {
        "num": 5,
        "name": "b2_05_o_sistema_que_estou_construindo.mp4",
        "sub": "b2_v05.ass",
        "segments": [
            {"ss": 42*60+32, "t": 42},
            {"ss": 49*60+28, "t": 24},
        ],
        "total_t": 66,
        "title": "O SISTEMA QUE ESTOU CONSTRUINDO",
        "zooms": [(6.0, 20.0), (38.0, 55.0)],
        "cards": [
            {"s": 0, "e": 6, "text": "Dados da empresa -> 30 posts + 30 vídeos em 24h"},
            {"s": 20, "e": 38, "text": "O desafio: automático sem parecer genérico"}
        ]
    },
    {
        "num": 6,
        "name": "b2_06_como_estudar_virais_sem_copiar.mp4",
        "sub": "b2_v06.ass",
        "segments": [
            {"ss": 50*60+4, "t": 14},
            {"ss": 50*60+32, "t": 44},
        ],
        "total_t": 58,
        "title": "COMO ESTUDAR VIRAIS SEM COPIAR",
        "zooms": [(14.0, 34.0)],
        "cards": [
            {"s": 0, "e": 14, "text": "Copiar um viral não é estratégia. Entender o padrão é."},
            {"s": 34, "e": 52, "text": "Gancho • Ritmo • Tema • Formato • Fechamento"}
        ]
    },
    {
        "num": 7,
        "name": "b2_07_antes_de_criar_um_app_faca_isso.mp4",
        "sub": "b2_v07.ass",
        "segments": [{"ss": 60*60+10, "t": 36}],
        "total_t": 36,
        "title": "ANTES DE CRIAR UM APP, FAÇA ISSO",
        "zooms": [(8.0, 22.0)],
        "cards": [
            {"s": 0, "e": 8, "text": "Criar o app é a parte fácil. A parte difícil é essa."},
            {"s": 22, "e": 34, "text": "Valide a dor antes de escrever a primeira linha de código"}
        ]
    },
    {
        "num": 8,
        "name": "b2_r01_nunca_trabalhei_clt.mp4",
        "sub": "b2_r01.ass",
        "segments": [
            {"ss": 1*60*60 + 1*60 + 2, "t": 10},
            {"ss": 1*60*60 + 1*60 + 16, "t": 38},
        ],
        "total_t": 48,
        "title": "NUNCA TRABALHEI CLT. ISSO FOI BOM OU RUIM?",
        "zooms": [(10.0, 30.0)],
        "cards": [
            {"s": 0, "e": 10, "text": "Minha trajetória foi direto para o digital e projetos próprios."},
            {"s": 32, "e": 48, "text": "Empreender também é conviver com essa dúvida."}
        ]
    },
    {
        "num": 9,
        "name": "b2_r02_o_erro_de_seguranca_que_cometo.mp4",
        "sub": "b2_r02.ass",
        "segments": [
            {"ss": 61*60+18, "t": 8},
            {"ss": 61*60+30, "t": 18},
        ],
        "total_t": 26,
        "title": "EU JÁ FUI HACKEADA POR FAZER ISSO",
        "zooms": [(5.0, 17.0)],
        "cards": [
            {"s": 0, "e": 5, "text": "NÃO faça isso sem isolamento e verificação."},
            {"s": 5, "e": 22, "text": "Autenticação em 2 fatores ajudou na recuperação"}
        ]
    }
]

def render_video(v):
    out_path = os.path.join(out_dir, v["name"])
    print(f"\n[{v['num']}/9] Renderizando com Edição Completa + Legendas Kinéticas: {v['name']}")
    
    # Prepara cópia limpa do arquivo ASS em pasta sem espaços/caracteres complexos
    orig_sub = os.path.join(subs_dir, v["sub"])
    temp_sub = os.path.join(temp_subs_dir, f"sub_{v['num']}.ass")
    shutil.copy2(orig_sub, temp_sub)
    
    # Path de legenda formatado para ffmpeg windows
    sub_param = temp_sub.replace("\\", "/").replace(":", "\\:")
    
    segs = v["segments"]
    
    # Prepara vídeo cortado/concatenado base
    if len(segs) == 1:
        base_clip = os.path.join(out_dir, f"_base_{v['num']}.mp4")
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
        
        concat_list = os.path.join(out_dir, f"_concat_{v['num']}.txt")
        with open(concat_list, "w", encoding="utf-8") as f:
            for c in tmp_clips:
                f.write(f"file '{c}'\n")
        
        base_clip = os.path.join(out_dir, f"_base_{v['num']}.mp4")
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

    # Construção do Filtergraph Completo
    title_text = v["title"].replace("'", "").replace(":", "")
    
    vf_parts = [
        "crop=ih*9/16:ih:(iw-ih*9/16)/2:0",
        "scale=1080:1920",
    ]
    
    # Focus Zoom Multi-Camera (Cortes em 108% escala)
    if v["zooms"]:
        zoom_exprs = [f"between(t,{zs},{ze})" for zs, ze in v["zooms"]]
        cond_zoom = "+".join(zoom_exprs)
        vf_parts.append(
            f"scale=eval=frame:w='if({cond_zoom},1166,1080)':h='if({cond_zoom},2073,1920)',crop=1080:1920"
        )
    
    # CARD DE TÍTULO MODERNO (Posição y=450)
    vf_parts.append("drawbox=y=440:h=96:color=black@0.85:t=fill")
    vf_parts.append("drawbox=y=438:h=2:color=yellow@0.85:t=fill")
    vf_parts.append(
        f"drawtext=fontfile='C\\:/Windows/Fonts/arialbd.ttf':text='{title_text}':fontcolor=white:fontsize=34:x=(w-text_w)/2:y=470"
    )
    
    # CARDS DE CONTEXTO POP-IN (Posição y=550)
    for card in v["cards"]:
        c_txt = card["text"].replace("'", "").replace(":", "")
        cs, ce = card["s"], card["e"]
        vf_parts.append(
            f"drawbox=y=550:h=76:color=black@0.75:t=fill:enable='between(t,{cs},{ce})'"
        )
        vf_parts.append(
            f"drawtext=fontfile='C\\:/Windows/Fonts/arial.ttf':text='{c_txt}':fontcolor=yellow:fontsize=28:x=(w-text_w)/2:y=574:enable='between(t,{cs},{ce})'"
        )
        
    # LEGENDAS ASS KINÉTICAS PALAVRA POR PALAVRA
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
        return True
    else:
        err = res.stderr.decode(errors="ignore")[-300:] if hasattr(res, 'stderr') and res.stderr else ""
        print(f"  ERROR: {v['name']} — {err}")
        return False

print("=" * 60)
print("RE-RENDERIZANDO BLOCO 2 — EDIÇÃO COMPLETA HUMAN-CRAFTED COM LEGENDAS ASS")
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
