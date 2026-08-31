import json
import re
import os

json_path = r"C:\Users\Kethely\.gemini\antigravity\brain\9dbd3421-ae5c-4f63-9d99-553453c42d0e\scratch\transcript_2026-07-23-23-55-30.json"

with open(json_path, encoding="utf-8") as f:
    data = json.load(f)

segments = data.get("segments", [])

# Let's map target text fragments for each of the 16 videos to find exact start & end seconds
targets = [
    {
        "id": 1,
        "name": "video_01_chatgpt_5reais",
        "title": "COMO EU ENCONTREI CHATGPT POR R$ 5",
        "start_kw": "Como eu descobri esse site",
        "end_kw": "foi esse daqui"
    },
    {
        "id": 2,
        "name": "video_02_plataforma_72desconto",
        "title": "ACHEI UMA PLATAFORMA COM 72% DE DESCONTO",
        "start_kw": "Outra que também tá muito boa",
        "end_kw": "compense mais o ChatGPT"
    },
    {
        "id": 3,
        "name": "video_03_um_testei_outro_nao",
        "title": "UM EU TESTEI. O OUTRO, NAO",
        "start_kw": "esse site que eu tô mostrando agora eu nunca comprei",
        "end_kw": "O outro eu ainda vou testar"
    },
    {
        "id": 4,
        "name": "video_04_de_onde_vem_apis_baratas",
        "title": "DE ONDE VEM O PRECO TAO BAIXO?",
        "start_kw": "Eu vou explicar pra vocês como funciona essa API",
        "end_kw": "outro provedor empresarial"
    },
    {
        "id": 5,
        "name": "video_05_api_nao_realmente_sua",
        "title": "ESSA API E REALMENTE SUA?",
        "start_kw": "estavam falando que talvez essas informações não fossem totalmente seguras",
        "end_kw": "Eu não colocaria numa API dessas"
    },
    {
        "id": 6,
        "name": "video_06_quando_usaria_api_barata",
        "title": "QUANDO O BARATO DEIXA DE COMPENSAR",
        "start_kw": "Isso é uma alternativa barata",
        "end_kw": "quando a empresa cresce, o risco também muda"
    },
    {
        "id": 7,
        "name": "video_07_nao_coloque_codigo_empresa",
        "title": "VOCE COLOCARIA O CODIGO DA EMPRESA AQUI?",
        "start_kw": "Eu até vi um caso que aconteceu",
        "end_kw": "informação inteira numa ferramenta externa"
    },
    {
        "id": 8,
        "name": "video_08_diversao_virou_trabalhar",
        "title": "MEU HOBBY VIROU MEU TRABALHO",
        "start_kw": "Eu parei de jogar faz um tempinho",
        "end_kw": "fazer alguma coisa longe do computador"
    },
    {
        "id": 9,
        "name": "video_09_beneficios_para_empresas",
        "title": "SUA EMPRESA PODE TER ACESSO A ISSO",
        "start_kw": "Gente, vou mostrar uma plataforma pra vocês",
        "end_kw": "que as empresas nem sabem que podem solicitar"
    },
    {
        "id": 10,
        "name": "video_10_5mil_dolares_creditos",
        "title": "US$ 5 MIL EM CREDITOS DE IA?",
        "start_kw": "Esse aqui é da Amazon e da Microsoft",
        "end_kw": "realmente davam pra conseguir"
    },
    {
        "id": 11,
        "name": "video_11_3reais_100dolares",
        "title": "R$ 3 = US$ 100?",
        "start_kw": "que é esse link aqui, ele não tá pegando agora pra comprar",
        "end_kw": "continua seguindo a tabela dela"
    },
    {
        "id": 12,
        "name": "video_12_quanto_gastei_apis",
        "title": "7 MILHOES DE TOKENS POR US$ 2,42?",
        "start_kw": "Eu já gastei um pouco aqui pra vocês verem",
        "end_kw": "separar corretamente quanto cada modelo gastou"
    },
    {
        "id": 13,
        "name": "video_13_almoco_gratis_vai_acabar",
        "title": "O ALMOCO GRATIS VAI ACABAR",
        "start_kw": "a gente tá comendo o almoço grátis",
        "end_kw": "vai ficar caro. Vai ficar caro."
    },
    {
        "id": 14,
        "name": "video_14_ia_me_ensinou_aprender",
        "title": "A IA ME ENSINOU A APRENDER",
        "start_kw": "Eu amo IA, cara. Virou meu vício",
        "end_kw": "comecei a conseguir entrar em qualquer assunto"
    },
    {
        "id": 15,
        "name": "video_15_psicologia_ia_programacao",
        "title": "O QUE PSICOLOGIA TEM A VER COM IA?",
        "start_kw": "estudo o YA e programação, só que eu estou fazendo faculdade de psicologia",
        "end_kw": "comecei a trabalhar com programação"
    },
    {
        "id": 16,
        "name": "video_16_meu_site_maior_orgulho",
        "title": "MEU MAIOR ORGULHO AGORA",
        "start_kw": "Deixa eu mostrar pra vocês o meu orgulhozinho",
        "end_kw": "não tá com ela, você não tá bonitinho"
    }
]

print("Scanning segments...")
results = []
for t in targets:
    start_time = None
    end_time = None
    
    # Simple keyword search across transcript segments
    skw = t["start_kw"].lower()
    ekw = t["end_kw"].lower()
    
    for seg in segments:
        text = seg["text"].lower()
        if start_time is None and any(word in text for word in skw.split()[:3]):
            # check fuzzy match
            start_time = seg["start"]
        if start_time is not None and any(word in text for word in ekw.split()[-3:]):
            end_time = seg["end"]
            if end_time - start_time >= 15.0: # valid duration
                break
    
    if start_time is not None and end_time is not None:
        dur = round(end_time - start_time, 1)
        results.append({
            "id": t["id"],
            "name": t["name"],
            "title": t["title"],
            "start": round(start_time, 2),
            "end": round(end_time, 2),
            "dur": dur
        })
        print(f"MATCH [{t['id']}] {t['name']}: {start_time:.1f}s -> {end_time:.1f}s ({dur}s)")
    else:
        print(f"MISS [{t['id']}] {t['name']}: start={start_time}, end={end_time}")

with open(r"C:\Users\Kethely\.gemini\antigravity\brain\9dbd3421-ae5c-4f63-9d99-553453c42d0e\scratch\timestamp_matches.json", "w", encoding="utf-8") as f:
    json.dump(results, f, indent=2)
