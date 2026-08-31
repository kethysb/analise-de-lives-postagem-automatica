import os
import requests
import json
import sys
import time

sys.stdout.reconfigure(encoding='utf-8')

api_key = "wsk_41af245d7b2919a4.53bec0a4a1113b33136381c74004db06ffed1831729ba4381d637dc95aa91bea"
project_id = "151419457388937216"
tiktok_account_id = "154633727815712768" # @kthyeu

out_dir = r"C:\Users\Kethely\Downloads\novos_cortes_editados"

headers = {
    "Authorization": f"Bearer {api_key}",
    "Content-Type": "application/json"
}

# 1. Clean up unused media files first
r = requests.get("https://api.woopsocial.com/v1/media", headers=headers)
if r.status_code == 200:
    for item in r.json().get("media", []):
        requests.delete(f"https://api.woopsocial.com/v1/media/{item.get('id')}", headers=headers)

# 8 Approved Videos in recommended sequence: V5, V1, V2, V4, V6, V3, V7, V8
posts = [
    {
        "num": 5,
        "title": "Nota alta não é o mesmo que aprender",
        "name": "05_nota_alta_nao_e_o_mesmo_que_aprender.mp4",
        "caption": """A IA me ajudou a transformar o material das aulas em perguntas e exercícios. Na minha experiência, isso melhorou muito minha preparação para as provas.

Mas tirar uma nota boa não significa automaticamente compreender o conteúdo.

Para aprofundar, comecei a buscar artigos, exemplos e aplicações práticas: o que eu faria como profissional e onde aquele conhecimento poderia ser usado de verdade.

A primeira etapa me ajuda na prova. A segunda é o que faz o conteúdo permanecer.

#Estudos #InteligenciaArtificial #AprenderMelhor #Psicologia""",
        "schedule": {"type": "SCHEDULE_FOR_LATER", "scheduledFor": "2026-08-03T15:00:00Z"} # Mon 03/08 12:00 BRT
    },
    {
        "num": 1,
        "title": "IA dá dinheiro mesmo?",
        "name": "01_ia_da_dinheiro_mesmo.mp4",
        "caption": """A IA não trouxe clientes automaticamente.

Eu ainda preciso divulgar meu trabalho, investir e provar que consigo entregar. O que mudou foi a velocidade: tarefas que antes poderiam levar dias passaram a levar minutos.

Para mim, o verdadeiro valor não está em dominar uma ferramenta específica. Está em entender o processo o suficiente para continuar trabalhando mesmo quando a ferramenta mudar.

O que vale mais hoje: conhecer a ferramenta ou entender o trabalho?

#InteligenciaArtificial #TrabalhoComIA #Automacao #Tecnologia""",
        "schedule": {"type": "SCHEDULE_FOR_LATER", "scheduledFor": "2026-08-03T21:00:00Z"} # Mon 03/08 18:00 BRT
    },
    {
        "num": 2,
        "title": "Quanto mais aprendo IA, menos dependo dela",
        "name": "02_quanto_mais_aprendo_ia_menos_dependo.mp4",
        "caption": """Quanto mais eu aprendo sobre IA, mais percebo que não preciso colocar IA em todas as etapas.

Uso inteligência artificial para pesquisar, planejar e construir. Depois, quando o processo já está definido, tento transformar a rotina em uma automação mais previsível e barata.

IA para construir. Automação para manter.

#InteligenciaArtificial #Automacao #Tecnologia #Produtividade""",
        "schedule": {"type": "SCHEDULE_FOR_LATER", "scheduledFor": "2026-08-04T15:00:00Z"} # Tue 04/08 12:00 BRT
    },
    {
        "num": 4,
        "title": "Não procure uma profissão chamada 'IA'",
        "name": "04_nao_procure_uma_profissao_chamada_ia.mp4",
        "caption": """“Trabalhar com IA” ainda é uma definição ampla demais.

O trabalho de verdade costuma estar em resolver um problema de programação, marketing, atendimento, dados ou operações usando essas ferramentas.

Em vez de abandonar a área de que você gosta, aprenda a combinar essa área com IA.

Qual conhecimento você juntaria com inteligência artificial?

#CarreiraEmTecnologia #InteligenciaArtificial #Programacao #Automacao""",
        "schedule": {"type": "SCHEDULE_FOR_LATER", "scheduledFor": "2026-08-04T21:00:00Z"} # Tue 04/08 18:00 BRT
    },
    {
        "num": 6,
        "title": "O pior jeito de prospectar empresas novas",
        "name": "06_o_pior_jeito_de_prospectar_empresas.mp4",
        "caption": """Encontrar uma empresa que acabou de abrir não significa que ela queira receber o mesmo texto que outras cinquenta pessoas já enviaram.

Dados podem ajudar a pesquisar e entender uma empresa. Mas, sem contexto, a prospecção vira apenas mais uma mensagem genérica na caixa de entrada.

Antes de abordar alguém, entenda o negócio e descubra se existe um problema real que você consegue resolver.

#Prospeccao #VendasB2B #MarketingDigital #Empreendedorismo""",
        "schedule": {"type": "SCHEDULE_FOR_LATER", "scheduledFor": "2026-08-05T15:00:00Z"} # Wed 05/08 12:00 BRT
    },
    {
        "num": 3,
        "title": "Por que sua IA responde genérico?",
        "name": "03_por_que_ia_responde_generico.mp4",
        "caption": """Às vezes, o problema não é a ferramenta. É o caminho que você apresentou para ela.

Objetivo, contexto, referências e limites ajudam a reduzir respostas genéricas. A comparação com ensinar uma pessoa é apenas uma analogia: uma IA não aprende durante uma conversa exatamente como um ser humano.

Trocar de modelo sem melhorar o contexto pode produzir a mesma resposta genérica em uma ferramenta mais cara.

#PromptEngineering #InteligenciaArtificial #Automacao #Produtividade""",
        "schedule": {"type": "SCHEDULE_FOR_LATER", "scheduledFor": "2026-08-05T21:00:00Z"} # Wed 05/08 18:00 BRT
    },
    {
        "num": 7,
        "title": "Por que parei de construir tudo do zero",
        "name": "07_por_que_parei_de_construir_do_zero.mp4",
        "caption": """Eu gosto de controlar e personalizar minhas próprias ferramentas. Mas existe uma diferença entre construir uma solução e refazer toda a infraestrutura sempre que começo um projeto.

Estou testando o Agent Zero como uma base aberta para reunir ambiente, navegador, skills e diferentes integrações.

Não é deixar de construir. É escolher melhor qual parte realmente precisa ser criada por mim.

#AgentZero #AgentesDeIA #OpenSource #Automacao""",
        "schedule": {"type": "SCHEDULE_FOR_LATER", "scheduledFor": "2026-08-06T15:00:00Z"} # Thu 06/08 12:00 BRT
    },
    {
        "num": 8,
        "title": "Por que computer use ainda erra tanto?",
        "name": "08_por_que_computer_use_ainda_erra_tanto.mp4",
        "caption": """Controlar um computador olhando para a tela e tentando clicar em coordenadas ainda pode ser frágil.

Por isso estou estudando alternativas em que mais ações possam ser executadas por comandos e estruturas previsíveis, reduzindo a dependência de cliques visuais.

Este é o sistema que estou tentando montar agora: combinar agentes, navegador, Linux e automação sem depender completamente de uma única plataforma.

#ComputerUse #AgentesDeIA #OpenSource #Automacao""",
        "schedule": {"type": "SCHEDULE_FOR_LATER", "scheduledFor": "2026-08-06T21:00:00Z"} # Thu 06/08 18:00 BRT
    }
]

print("Starting Sequential Upload & Scheduling for All 8 Approved Videos...")

scheduled_results = []

for item in posts:
    num = item["num"]
    name = item["name"]
    v_path = os.path.join(out_dir, name)
    
    print(f"\n----------------------------------------------")
    print(f"Processing Video [{num}]: {name}")
    
    if not os.path.exists(v_path):
        print(f"Error: File not found {v_path}")
        continue
    
    file_size = os.path.getsize(v_path)
    print(f"File size: {file_size} bytes ({round(file_size/(1024*1024), 2)} MB)")
    
    # 1. Create Upload Session
    sess_resp = requests.post(
        "https://api.woopsocial.com/v1/media/upload-sessions",
        headers=headers,
        json={"projectId": project_id, "fileSizeInBytes": file_size}
    )
    
    if sess_resp.status_code not in [200, 201]:
        print(f"Upload session error: {sess_resp.status_code} {sess_resp.text}")
        continue
    
    sess_data = sess_resp.json()
    upload_session_id = sess_data["uploadSessionId"]
    part_size = sess_data.get("partSizeInBytes", 10485760)
    parts = sess_data.get("parts", [])
    
    # 2. Upload Chunks
    with open(v_path, "rb") as f:
        for idx, part in enumerate(parts):
            upload_url = part["uploadUrl"]
            chunk = f.read(part_size)
            put_resp = requests.put(upload_url, data=chunk)
            if put_resp.status_code not in [200, 201, 204]:
                print(f"  Chunk {idx+1} upload error: {put_resp.status_code}")
    
    # 3. Complete Upload Session
    comp_resp = requests.post(
        f"https://api.woopsocial.com/v1/media/upload-sessions/{upload_session_id}/complete",
        headers=headers
    )
    
    if comp_resp.status_code not in [200, 201]:
        print(f"Complete upload error: {comp_resp.status_code} {comp_resp.text}")
        continue
    
    media_id = comp_resp.json()["mediaId"]
    print(f"Media Uploaded Successfully! Media ID: {media_id}")
    
    # 4. Schedule Post on TikTok @kthyeu
    post_payload = {
        "content": [
            {
                "media": [
                    {
                        "mediaId": media_id,
                        "type": "MEDIA_LIBRARY"
                    }
                ],
                "text": item["caption"]
            }
        ],
        "schedule": item["schedule"],
        "socialAccounts": [
            {
                "socialAccountId": tiktok_account_id,
                "platform": "TIKTOK",
                "postMode": "DIRECT_POST",
                "postType": "VIDEO",
                "privacyLevel": "PUBLIC_TO_EVERYONE",
                "allowComment": True,
                "allowDuet": True,
                "allowStitch": True,
                "isYourBrand": False,
                "isBrandedContent": False,
                "autoAddMusic": True
            }
        ]
    }
    
    post_resp = requests.post(
        "https://api.woopsocial.com/v1/posts",
        headers=headers,
        json=post_payload
    )
    
    if post_resp.status_code in [200, 201]:
        p_data = post_resp.json()
        p_id = p_data.get("id")
        print(f"SUCCESS! Post Scheduled! Post ID: {p_id}")
        scheduled_results.append({
            "num": num,
            "title": item["title"],
            "fileName": name,
            "postId": p_id,
            "scheduledFor": item["schedule"]["scheduledFor"],
            "status": "SCHEDULED"
        })
    else:
        print(f"Publish Post Error: {post_resp.status_code} {post_resp.text}")
    
    # Delete uploaded media to preserve storage quota for next videos
    requests.delete(f"https://api.woopsocial.com/v1/media/{media_id}", headers=headers)
    time.sleep(1)

print("\n==============================================")
print(f"SUCCESSFULLY SCHEDULED {len(scheduled_results)}/8 APPROVED VIDEOS ON TIKTOK @kthyeu:")
print(json.dumps(scheduled_results, indent=2, ensure_ascii=False))
