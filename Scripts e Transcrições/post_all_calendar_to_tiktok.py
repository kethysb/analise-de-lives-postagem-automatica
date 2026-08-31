import os
import requests
import json
import sys
import time

sys.stdout.reconfigure(encoding='utf-8')

api_key = "wsk_41af245d7b2919a4.53bec0a4a1113b33136381c74004db06ffed1831729ba4381d637dc95aa91bea"
project_id = "151419457388937216"
tiktok_account_id = "154633727815712768" # @kthyeu

out_dir = r"C:\Users\Kethely\Downloads\cortes_tiktok_editados"

headers = {
    "Authorization": f"Bearer {api_key}",
    "Content-Type": "application/json"
}

# List of all 15 videos with exact ISO 8601 UTC timestamps for SCHEDULE_FOR_LATER
calendar_posts = [
    {
        "num": 1,
        "name": "01_como_eu_encontrei_chatgpt_5reais.mp4",
        "already_posted": True, # Published!
        "caption": """Eu pagava cerca de R$ 5 para acessar o ChatGPT e o Codex em plataformas de revenda. Depois, os anúncios começaram a desaparecer e ficou bem mais difícil encontrar esses acessos.

Neste vídeo conto como funcionava na época da live. Lembrando que preços e políticas mudam sempre!

#IA #ChatGPT #Programacao #Tecnologia #DevBrasil""",
        "schedule": {"type": "PUBLISH_NOW"}
    },
    {
        "num": 2,
        "name": "02_plataforma_72_desconto.mp4",
        "already_posted": True, # Published!
        "caption": """Encontrei uma plataforma mostrando descontos de até 72% em APIs de inteligência artificial. O plano que aparecia por US$ 30 estava sendo oferecido por US$ 8,40.

Preço baixo chama atenção, mas antes de colocar dinheiro é preciso entender quem fornece o acesso.

#InteligenciaArtificial #OpenAI #API #Desenvolvimento #Dev""",
        "schedule": {"type": "PUBLISH_NOW"}
    },
    {
        "num": 3,
        "name": "03_um_site_testei_outro_nao.mp4",
        "already_posted": False,
        "caption": """Uma coisa que sempre deixo clara: encontrar uma ferramenta não significa recomendação!

Nesse caso, uma das plataformas eu tinha realmente testado e usado. A outra eu apenas tinha encontrado e ainda precisava testar.

#Programacao #Tecnologia #DicasDeIA #Softwares""",
        "schedule": {"type": "SCHEDULE_FOR_LATER", "scheduledFor": "2026-07-27T15:00:00Z"} # Mon 12:00 BRT
    },
    {
        "num": 4,
        "name": "04_de_onde_vem_apis_baratas.mp4",
        "already_posted": False,
        "caption": """De onde vêm as APIs tão baratas? Muitas plataformas trabalham com créditos promocionais, programas empresariais ou acessos da AWS.

É barato, mas a estrutura por trás do preço importa bastante!

#AWS #CloudComputing #API #Desenvolvedores""",
        "schedule": {"type": "SCHEDULE_FOR_LATER", "scheduledFor": "2026-07-27T21:00:00Z"} # Mon 18:00 BRT
    },
    {
        "num": 5,
        "name": "05_essa_api_pode_nao_ser_sua.mp4",
        "already_posted": False,
        "caption": """Quando você compra uma API oficial, existe uma relação direta com o provedor. Em plataformas terceirizadas, seus dados podem passar por contas intermediárias.

Para testes pessoais é uma escolha; para código confidencial ou dados de clientes, o cuidado tem que ser maior!

#SegurancaDaInformacao #CyberSecurity #IA #Sistemas""",
        "schedule": {"type": "SCHEDULE_FOR_LATER", "scheduledFor": "2026-07-28T15:00:00Z"} # Tue 12:00 BRT
    },
    {
        "num": 6,
        "name": "06_quando_usaria_api_barata.mp4",
        "already_posted": False,
        "caption": """Para projetos pessoais ou estudos, uma alternativa barata faz sentido para economizar. Mas conforme a empresa cresce e lida com dados sigilosos, a prioridade muda para a segurança.

#Empreendedorismo #Startups #Backend #EngenhariaDeSoftware""",
        "schedule": {"type": "SCHEDULE_FOR_LATER", "scheduledFor": "2026-07-28T21:00:00Z"} # Tue 18:00 BRT
    },
    {
        "num": 7,
        "name": "07_nao_coloque_codigo_empresa_chatgpt.mp4",
        "already_posted": False,
        "caption": """Usar IA para revisar código é extremamente útil. O problema é colar trechos confidenciais da empresa sem saber como os dados estão sendo tratados na plataforma.

#Programacao #CleanCode #Seguranca #Desenvolvedor""",
        "schedule": {"type": "SCHEDULE_FOR_LATER", "scheduledFor": "2026-07-29T15:00:00Z"} # Wed 12:00 BRT
    },
    {
        "num": 8,
        "name": "09_beneficios_para_empresas.mp4",
        "already_posted": False,
        "caption": """Descobri uma plataforma que reúne benefícios, créditos e períodos gratuitos oferecidos por grandes empresas de tecnologia para startups e negócios cadastrados.

#Startups #Negocios #CreditosCloud #Tech""",
        "schedule": {"type": "SCHEDULE_FOR_LATER", "scheduledFor": "2026-07-29T21:00:00Z"} # Wed 18:00 BRT
    },
    {
        "num": 9,
        "name": "10_5mil_dolares_creditos_ia.mp4",
        "already_posted": False,
        "caption": """Quando encontrei esse programa, o valor que mais chamou atenção foi US$ 5 mil em créditos de IA. Entenda como funcionam esses incentivos e o que é exigido.

#Azure #Microsoft #AmazonAWS #IA""",
        "schedule": {"type": "SCHEDULE_FOR_LATER", "scheduledFor": "2026-07-30T15:00:00Z"} # Thu 12:00 BRT
    },
    {
        "num": 10,
        "name": "11_3reais_por_100dolares_creditos.mp4",
        "already_posted": False,
        "caption": """Durante a live, mostrei uma plataforma onde poucos reais liberavam US$ 100 de saldo interno. Entenda a relação entre o preço do saldo e o consumo dos modelos!

#Tokens #LLM #IA #CustoAPI""",
        "schedule": {"type": "SCHEDULE_FOR_LATER", "scheduledFor": "2026-07-30T21:00:00Z"} # Thu 18:00 BRT
    },
    {
        "num": 11,
        "name": "12_quanto_gastei_usando_apis.mp4",
        "already_posted": False,
        "caption": """Mostrei no painel um consumo de 7 milhões de tokens por US$ 2,42 e 1 milhão de tokens no Claude. Saiba por que é essencial acompanhar o gasto exato por modelo!

#Claude #OpenAI #Tokens #DevLife""",
        "schedule": {"type": "SCHEDULE_FOR_LATER", "scheduledFor": "2026-07-31T15:00:00Z"} # Fri 12:00 BRT
    },
    {
        "num": 12,
        "name": "13_almoco_gratis_ia_vai_acabar.mp4",
        "already_posted": False,
        "caption": """A gente está aproveitando a fase do "almoço grátis" da inteligência artificial, mas essa fase de subsídio não dura para sempre. Aprenda a usar modelos Open Source!

#OpenSource #Llama #InteligenciaArtificial #Tecnologia""",
        "schedule": {"type": "SCHEDULE_FOR_LATER", "scheduledFor": "2026-07-31T21:00:00Z"} # Fri 18:00 BRT
    },
    {
        "num": 13,
        "name": "08_minha_diversao_virou_trabalhar.mp4",
        "already_posted": False,
        "caption": """Eu amava jogar Valorant e passar horas no computador. Mas quando passei a trabalhar o dia inteiro na tela, minha diversão no computador virou trabalhar — e ao terminar, só quero sair da frente do PC!

#DevLife #CarreiraTech #Gamer #Programador""",
        "schedule": {"type": "SCHEDULE_FOR_LATER", "scheduledFor": "2026-08-01T15:00:00Z"} # Sat 12:00 BRT
    },
    {
        "num": 14,
        "name": "14_ia_me_ensinou_a_aprender.mp4",
        "already_posted": False,
        "caption": """A maior mudança que a IA trouxe para mim não foi fazer código por mim, mas me ensinar a aprender do jeito certo: com artigos científicos, evidências e autonomia!

#Estudos #Aprendizado #Produtividade #MindsetDev""",
        "schedule": {"type": "SCHEDULE_FOR_LATER", "scheduledFor": "2026-08-01T21:00:00Z"} # Sat 18:00 BRT
    },
    {
        "num": 15,
        "name": "15_psicologia_ia_e_programacao.mp4",
        "already_posted": False,
        "caption": """Como a faculdade de Psicologia, o estudo da neurociência e a programação se conectam no meu dia a dia para criar e resolver problemas de forma única!

#Neurociencia #Psicologia #Programacao #Carreira""",
        "schedule": {"type": "SCHEDULE_FOR_LATER", "scheduledFor": "2026-08-02T21:00:00Z"} # Sun 18:00 BRT
    }
]

print(f"Starting WoopSocial scheduling for TikTok account @kthyeu...")

results = []

for item in calendar_posts:
    v_path = os.path.join(out_dir, item["name"])
    print(f"\n==============================================")
    print(f"[{item['num']}/15] Processing: {item['name']}")
    
    if item.get("already_posted"):
        print(f"Video {item['num']} ALREADY PUBLISHED!")
        results.append({"num": item["num"], "name": item["name"], "status": "PUBLISHED"})
        continue
    
    if not os.path.exists(v_path):
        print(f"Error: Video not found: {v_path}")
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
    
    # 4. Schedule or Publish Post
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
        p_sched = item["schedule"]["type"]
        print(f"SUCCESS! Post [{p_sched}] Created! Post ID: {p_id}")
        results.append({"num": item["num"], "name": item["name"], "status": p_sched, "postId": p_id})
    else:
        print(f"Publish Post Error: {post_resp.status_code} {post_resp.text}")
        results.append({"num": item["num"], "name": item["name"], "status": "ERROR", "error": post_resp.text})
    
    time.sleep(1) # rate limit pause

print("\n==============================================")
print("FINAL RESULTS:")
print(json.dumps(results, indent=2))
