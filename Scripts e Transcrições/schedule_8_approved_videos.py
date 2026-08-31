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

# Recommended publication order: V5, V1, V2, V4, V6, V3, V7, V8 (2 videos/day starting Monday 03/08)
posts = [
    {
        "num": 5,
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
        "name": "02_quanto_mais_aprendo_ia_menos_dependo.mp4",
        "caption": """Quanto mais eu aprendo sobre IA, mais percebo que não preciso colocar IA em todas as etapas.

Uso inteligência artificial para pesquisar, planejar e construir. Depois, quando o processo já está definido, tento transformar a rotina em uma automação mais previsível e barata.

IA para construir. Automação para manter.

#InteligenciaArtificial #Automacao #Tecnologia #Produtividade""",
        "schedule": {"type": "SCHEDULE_FOR_LATER", "scheduledFor": "2026-08-04T15:00:00Z"} # Tue 04/08 12:00 BRT
    },
    {
        "num": 4,
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
        "name": "06_o_pior_jeito_de_prospectar_empresas.mp4",
        "caption": """Encontrar uma empresa que acabou de abrir não significa que ela queira receber o mesmo texto que outras cinquenta pessoas já enviaram.

Dados podem ajudar a pesquisar e entender uma empresa. Mas, sem contexto, a prospecção vira apenas mais uma mensagem genérica na caixa de entrada.

Antes de abordar alguém, entenda o negócio e descubra se existe um problema real que você consegue resolver.

#Prospeccao #VendasB2B #MarketingDigital #Empreendedorismo""",
        "schedule": {"type": "SCHEDULE_FOR_LATER", "scheduledFor": "2026-08-05T15:00:00Z"} # Wed 05/08 12:00 BRT
    },
    {
        "num": 3,
        "name": "03_por_que_ia_responde_generico.mp4",
        "caption": """Às vezes, o problema não é a ferramenta. É o caminho que você apresentou para ela.

Objetivo, contexto, referências e limites ajudam a reduzir respostas genéricas. A comparação com ensinar uma pessoa é apenas uma analogia: uma IA não aprende durante uma conversa exatamente como um ser humano.

Trocar de modelo sem melhorar o contexto pode produzir a mesma resposta genérica em uma ferramenta mais cara.

#PromptEngineering #InteligenciaArtificial #Automacao #Produtividade""",
        "schedule": {"type": "SCHEDULE_FOR_LATER", "scheduledFor": "2026-08-05T21:00:00Z"} # Wed 05/08 18:00 BRT
    },
    {
        "num": 7,
        "name": "07_por_que_parei_de_construir_do_zero.mp4",
        "caption": """Eu gosto de controlar e personalizar minhas próprias ferramentas. Mas existe uma diferença entre construir uma solução e refazer toda a infraestrutura sempre que começo um projeto.

Estou testando o Agent Zero como uma base aberta para reunir ambiente, navegador, skills e diferentes integrações.

Não é deixar de construir. É escolher melhor qual parte realmente precisa ser criada por mim.

#AgentZero #AgentesDeIA #OpenSource #Automacao""",
        "schedule": {"type": "SCHEDULE_FOR_LATER", "scheduledFor": "2026-08-06T15:00:00Z"} # Thu 06/08 12:00 BRT
    },
    {
        "num": 8,
        "name": "08_por_que_computer_use_ainda_erra_tanto.mp4",
        "caption": """Controlar um computador olhando para a tela e tentando clicar em coordenadas ainda pode ser frágil.

Por isso estou estudando alternativas em que mais ações possam ser executadas por comandos e estruturas previsíveis, reduzindo a dependência de cliques visuais.

Este é o sistema que estou tentando montar agora: combinar agentes, navegador, Linux e automação sem depender completamente de uma única plataforma.

#ComputerUse #AgentesDeIA #OpenSource #Automacao""",
        "schedule": {"type": "SCHEDULE_FOR_LATER", "scheduledFor": "2026-08-06T21:00:00Z"} # Thu 06/08 18:00 BRT
    }
]

print("Starting WoopSocial API Automation for the 8 Approved Videos...")

results = []

for item in posts:
    v_path = os.path.join(out_dir, item["name"])
    print(f"\n==============================================")
    print(f"Processing Approved Video [{item['num']}]: {item['name']}")
    
    if not os.path.exists(v_path):
        print(f"Error: Video file not found: {v_path}")
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
        print(f"Upload session err: {sess_resp.status_code} {sess_resp.text}")
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
                print(f"Upload part error: {put_resp.status_code}")
    
    # 3. Complete Upload
    comp_resp = requests.post(
        f"https://api.woopsocial.com/v1/media/upload-sessions/{upload_session_id}/complete",
        headers=headers
    )
    if comp_resp.status_code not in [200, 201]:
        print(f"Complete upload err: {comp_resp.status_code} {comp_resp.text}")
        continue
    
    media_id = comp_resp.json()["mediaId"]
    print(f"Media uploaded! Media ID: {media_id}")
    
    # 4. Schedule Post in WoopSocial
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
        results.append({"num": item["num"], "name": item["name"], "status": "SCHEDULED", "postId": p_id})
    else:
        print(f"Publish Post Error: {post_resp.status_code} {post_resp.text}")
        results.append({"num": item["num"], "name": item["name"], "status": "ERROR", "error": post_resp.text})
    
    time.sleep(1)

print("\n==============================================")
print("FINAL RESULTS OF 8 APPROVED VIDEOS SCHEDULING:")
print(json.dumps(results, indent=2))
