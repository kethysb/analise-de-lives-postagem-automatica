import json
import re

json_path = r"C:\Users\Kethely\.gemini\antigravity\brain\9dbd3421-ae5c-4f63-9d99-553453c42d0e\scratch\transcript_2026-07-23-23-55-30.json"

with open(json_path, encoding="utf-8") as f:
    data = json.load(f)

segments = data.get("segments", [])

# Let's map target text fragments for each of the 16 videos
videos = [
    {
        "id": 1,
        "name": "video_01_chatgpt_5reais",
        "title": "EU PAGAVA R$ 5 NO CHATGPT",
        "start_phrase": "Como eu descobri esse site? Eu entrei no G2G",
        "end_phrase": "foi esse daqui"
    },
    {
        "id": 2,
        "name": "video_02_plataforma_72desconto",
        "title": "72% MAIS BARATO. COMO?",
        "start_phrase": "Outra que também tá, é muito boa que eu ainda não testei",
        "end_phrase": "compensa mais chatia PT"
    },
    {
        "id": 3,
        "name": "video_03_um_testei_outro_nao",
        "title": "UM EU TESTEI. O OUTRO, NAO.",
        "start_phrase": "esse que eu nunca comprei",
        "end_phrase": "O outro eu ainda vou testar"
    },
    {
        "id": 4,
        "name": "video_04_de_onde_vem_apis_baratas",
        "title": "DE ONDE VEM O PRECO TAO BAIXO?",
        "start_phrase": "Eu vou explicar pra vocês como funciona essa peita",
        "end_phrase": "AWS"
    },
    {
        "id": 5,
        "name": "video_05_api_nao_realmente_sua",
        "title": "ESSA API E REALMENTE SUA?",
        "start_phrase": "Por isso que eles estavam falando que talvez essas informações",
        "end_phrase": "não vai colocar no open identity pelo amor de Deus"
    },
    {
        "id": 6,
        "name": "video_06_quando_usaria_api_barata",
        "title": "QUANDO O BARATO DEIXA DE COMPENSAR",
        "start_phrase": "Isso é uma alternativa barata",
        "end_phrase": "Eu usaria uma API que paga"
    },
    {
        "id": 7,
        "name": "video_07_nao_coloque_codigo_empresa",
        "title": "VOCE COLOCARIA O CODIGO DA EMPRESA AQUI?",
        "start_phrase": "caso que eu vi com a cabeça",
        "end_phrase": "tacaram o chatiopet"
    },
    {
        "id": 8,
        "name": "video_08_diversao_virou_trabalhar",
        "title": "MEU HOBBY VIROU MEU TRABALHO",
        "start_phrase": "Eu parei de jogar, faz um tempinho",
        "end_phrase": "minha diversão no computador é trabalhar"
    },
    {
        "id": 9,
        "name": "video_09_beneficios_para_empresas",
        "title": "SUA EMPRESA PODE TER ACESSO A ISSO",
        "start_phrase": "Gente, vou mostrar uma plataforma pra vocês",
        "end_phrase": "Quem tem empresas aqui, gente?"
    },
    {
        "id": 10,
        "name": "video_10_5mil_dolares_creditos",
        "title": "US$ 5 MIL EM CREDITOS DE IA?",
        "start_phrase": "É o... da Amazon e o... McGrassaf Sazuri",
        "end_phrase": "Depois que eu descobri esse negócio"
    },
    {
        "id": 11,
        "name": "video_11_3reais_100dolares",
        "title": "R$ 3 = US$ 100?",
        "start_phrase": "Ele é o das reais que eu falei",
        "end_phrase": "você paga 3 reais, você tem 100 dólares"
    },
    {
        "id": 12,
        "name": "video_12_quanto_gastei_apis",
        "title": "7 MILHOES DE TOKENS POR US$ 2,42?",
        "start_phrase": "Eu gastei 3 dólares de cloud",
        "end_phrase": "7 milhões de tokens"
    },
    {
        "id": 13,
        "name": "video_13_almoco_gratis_vai_acabar",
        "title": "O ALMOCO GRATIS VAI ACABAR",
        "start_phrase": "a gente tá comendo o almoço grátis",
        "end_phrase": "vai ficar caro"
    },
    {
        "id": 14,
        "name": "video_14_ia_me_ensinou_aprender",
        "title": "A IA ME ENSINOU A APRENDER",
        "start_phrase": "eu amo e a cara virou meu vicio",
        "end_phrase": "aprendi isso da melhor prova"
    },
    {
        "id": 15,
        "name": "video_15_psicologia_ia_programacao",
        "title": "O QUE PSICOLOGIA TEM A VER COM IA?",
        "start_phrase": "eu estudo o YA e programação",
        "end_phrase": "comecei a trabalhar com programação"
    },
    {
        "id": 16,
        "name": "video_16_meu_site_maior_orgulho",
        "title": "MEU MAIOR ORGULHO AGORA",
        "start_phrase": "Deixa eu mostrar pra vocês o meu orgulhozinho",
        "end_phrase": "a gente, não tá com ela, você não tá bonitinho"
    }
]

# Print transcript with timestamps to find exact matches
print(f"Total segments: {len(segments)}")

final_map = []
for v in videos:
    s_sec = None
    e_sec = None
    sp = v["start_phrase"].lower()
    ep = v["end_phrase"].lower()
    
    for seg in segments:
        txt = seg["text"].lower()
        if s_sec is None and sp[:15] in txt:
            s_sec = seg["start"]
        if s_sec is not None and ep[:15] in txt:
            e_sec = seg["end"]
            if e_sec > s_sec:
                break
    
    if s_sec and e_sec:
        dur = round(e_sec - s_sec, 1)
        final_map.append({
            "id": v["id"],
            "name": v["name"],
            "title": v["title"],
            "start": round(s_sec, 2),
            "end": round(e_sec, 2),
            "dur": dur
        })
        print(f"OK [{v['id']}] {v['name']}: {s_sec:.1f}s -> {e_sec:.1f}s ({dur}s)")
    else:
        print(f"SEARCH FAILED [{v['id']}] {v['name']} -> s={s_sec}, e={e_sec}")

with open(r"C:\Users\Kethely\.gemini\antigravity\brain\9dbd3421-ae5c-4f63-9d99-553453c42d0e\scratch\exact_map.json", "w", encoding="utf-8") as f:
    json.dump(final_map, f, indent=2)
