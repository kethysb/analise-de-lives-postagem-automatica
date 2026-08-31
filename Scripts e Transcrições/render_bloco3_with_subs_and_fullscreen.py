"""
Re-renderizador de Elite do Bloco 3:
1. Aplica Legendas ASS Kinéticas palavra por palavra centralizadas em TODOS os 7 vídeos.
2. Trata o vídeo do Bug do TikTok (b3_r01) com enquadramento total da tela (Full Screen Zoom),
   eliminando barras pretas e destacando a mensagem de erro do TikTok com efeito visual.
"""
import os
import subprocess
import shutil
import sys

sys.stdout.reconfigure(encoding='utf-8')

src_video = r"C:\Users\Kethely\Videos\2026-07-26-09-28-42.mp4"
out_dir = r"C:\Users\Kethely\Downloads\cortes_bloco3_editados"
os.makedirs(out_dir, exist_ok=True)

scratch_dir = r"C:\Users\Kethely\.gemini\antigravity\brain\9dbd3421-ae5c-4f63-9d99-553453c42d0e\scratch"
subs_dir = os.path.join(scratch_dir, "minimalist_subs_bloco3")
temp_subs_dir = r"C:\Temp\subs_b3"
os.makedirs(temp_subs_dir, exist_ok=True)

videos_b3 = [
    {
        "num": 1,
        "name": "b3_01_primeiros_clientes_do_zero.mp4",
        "sub": "b3_v01.ass",
        "title": "COMO CONSEGUI MEUS PRIMEIROS CLIENTES",
        "segments": [{"ss": 3945.0, "t": 61.0}],
        "total_t": 61.0,
        "zooms": [(5.0, 20.0), (35.0, 50.0)],
        "cards": [
            {"s": 0, "e": 8, "text": "Eu comecei vendendo perfume e ganhando R$70/dia"},
            {"s": 20, "e": 38, "text": "Estudei o negocio e montei a proposta"},
            {"s": 45, "e": 58, "text": "Meu 1 canal de aquisicao foi CONFIANCA"}
        ],
        "full_screen": False
    },
    {
        "num": 2,
        "name": "b3_02_vendi_maquina_50mil_com_100reais.mp4",
        "sub": "b3_v02.ass",
        "title": "MEU PRIMEIRO TESTE DE TRAFEGO PAGO",
        "segments": [
            {"ss": 3996.0, "t": 10.0},
            {"ss": 4343.0, "t": 23.0}
        ],
        "total_t": 33.0,
        "zooms": [(10.0, 25.0)],
        "cards": [
            {"s": 0, "e": 10, "text": "Da indicacao para o trafego pago"},
            {"s": 10, "e": 30, "text": "Produto: R$30k-R$50k | Anuncios: ~R$100"}
        ],
        "full_screen": False
    },
    {
        "num": 3,
        "name": "b3_03_fluxo_de_trabalho_comeca_por_audio.mp4",
        "sub": "b3_v03.ass",
        "title": "MEU FLUXO DE TRABALHO COMECA POR AUDIO",
        "segments": [
            {"ss": 4329.0, "t": 10.0},
            {"ss": 4396.0, "t": 33.0}
        ],
        "total_t": 43.0,
        "zooms": [(8.0, 25.0)],
        "cards": [
            {"s": 0, "e": 10, "text": "Parei de esperar chegar ao PC para anotar ideias"},
            {"s": 15, "e": 35, "text": "Audio -> Transcricao -> Execucao"}
        ],
        "full_screen": False
    },
    {
        "num": 4,
        "name": "b3_04_testei_api_vagas_ao_vivo.mp4",
        "sub": "b3_v04.ass",
        "title": "TESTEI UMA API DE VAGAS: NOTA 4/10",
        "segments": [{"ss": 4490.0, "t": 80.0}],
        "total_t": 80.0,
        "zooms": [(12.0, 35.0), (55.0, 75.0)],
        "cards": [
            {"s": 0, "e": 12, "text": "Pedi vagas e ela explicou a profissao"},
            {"s": 35, "e": 60, "text": "Resultados mal formatados na 2 tentativa"},
            {"s": 65, "e": 78, "text": "Nota Geral: 4/10 | Teste antes de usar"}
        ],
        "full_screen": False
    },
    {
        "num": 5,
        "name": "b3_05_api_que_transforma_sites_em_dados.mp4",
        "sub": "b3_v05.ass",
        "title": "A API QUE TRANSFORMA SITES EM DADOS",
        "segments": [{"ss": 4937.0, "t": 40.0}],
        "total_t": 40.0,
        "zooms": [(8.0, 25.0)],
        "cards": [
            {"s": 0, "e": 10, "text": "Envie uma URL -> Receba Screenshot, PDF e Dados"},
            {"s": 15, "e": 35, "text": "Microlink: Previews, monitoramento e arquivamento"}
        ],
        "full_screen": False
    },
    {
        "num": 6,
        "name": "b3_06_api_gratuita_banco_mundial.mp4",
        "sub": "b3_v06.ass",
        "title": "16 MIL INDICADORES ECONOMICOS EM UMA API",
        "segments": [{"ss": 5341.0, "t": 56.0}],
        "total_t": 56.0,
        "zooms": [(10.0, 35.0)],
        "cards": [
            {"s": 0, "e": 12, "text": "Dados de +200 paises sem criar sua propria base"},
            {"s": 20, "e": 45, "text": "Entendendo o contexto economico dos clientes"}
        ],
        "full_screen": False
    },
    {
        "num": 7,
        "name": "b3_r01_bug_contraditorio_do_tiktok.mp4",
        "sub": "b3_r01.ass",
        "title": "O BUG MAIS CONTRADITORIO DO TIKTOK",
        "segments": [{"ss": 4653.0, "t": 24.0}],
        "total_t": 24.0,
        "zooms": [],
        "cards": [
            {"s": 0, "e": 8, "text": "Indisponivel para usar | Impossivel de remover"},
            {"s": 12, "e": 22, "text": "Qual e o sentido desse erro? 😂"}
        ],
        # Trata o trecho preenchido em tela cheia (Full Scale & Crop)
        "full_screen": True
    }
]

def render_video(v):
    out_path = os.path.join(out_dir, v["name"])
    print(f"\n[{v['num']}/7] Renderizando com LEGENDAS ASS + EDIÇÃO ESPECIAL: {v['name']}")
    
    # Prepara legenda temporária
    orig_sub = os.path.join(subs_dir, v["sub"])
    temp_sub = os.path.join(temp_subs_dir, f"sub_{v['num']}.ass")
    shutil.copy2(orig_sub, temp_sub)
    sub_param = temp_sub.replace("\\", "/").replace(":", "\\:")
    
    segs = v["segments"]
    
    if len(segs) == 1:
        base_clip = os.path.join(out_dir, f"_base_b3_{v['num']}.mp4")
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
            tmp = os.path.join(out_dir, f"_tmp_b3_{v['num']}_{i}.mp4")
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
        
        concat_list = os.path.join(out_dir, f"_concat_b3_{v['num']}.txt")
        with open(concat_list, "w", encoding="utf-8") as f:
            for c in tmp_clips:
                f.write(f"file '{c}'\n")
        
        base_clip = os.path.join(out_dir, f"_base_b3_{v['num']}.mp4")
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

    # Filtergraph Inteligente
    title_text = v["title"].replace("'", "").replace(":", "")
    
    if v["full_screen"]:
        # Se for o video com área escura/do bug, faz um zoom maior preenchendo a tela toda 9:16
        vf_parts = [
            "scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920",
        ]
    else:
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
        f"drawtext=fontfile='C\\:/Windows/Fonts/arialbd.ttf':text='{title_text}':fontcolor=white:fontsize=34:x=(w-text_w)/2:y=470"
    )
    
    # POP-INS EDITORIAIS
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
print("RE-RENDERIZANDO BLOCO 3 COM LEGENDAS ASS E FULL-SCREEN BUG FIX")
print("=" * 60)

ok, fail = 0, 0
for v in videos_b3:
    if render_video(v):
        ok += 1
    else:
        fail += 1

print("\n" + "=" * 60)
print(f"RESULTADO FINAL: {ok}/7 renderizados com sucesso | {fail} falhas")
print(f"Pasta de saída: {out_dir}")
print("=" * 60)
