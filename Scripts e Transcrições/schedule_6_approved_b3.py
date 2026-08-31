"""
Script para Agendar os 6 Novos Vídeos Aprovados da Minutagem Analisada
Entram nos horários intercalados de hoje (29/07), amanhã (30/07) e sexta (31/07).
"""
import os
import requests
import json
import sys
import time

sys.stdout.reconfigure(encoding='utf-8')

api_key = "wsk_41af245d7b2919a4.53bec0a4a1113b33136381c74004db06ffed1831729ba4381d637dc95aa91bea"
project_id = "151419457388937216"
tiktok_account_id = "154633727815712768"

headers = {
    "Authorization": f"Bearer {api_key}",
    "Content-Type": "application/json"
}

out_dir = r"C:\Users\Kethely\Downloads\cortes_bloco3_editados"

approved_b3 = [
    {
        "num": 1,
        "filename": "b3_01_primeiros_clientes_do_zero.mp4",
        "date_brt": "Quarta (29/07) - 13:30 BRT",
        "scheduledFor": "2026-07-29T16:30:00Z",
        "caption": """Eu comecei vendendo perfume como freelancer e ganhando R$70 por dia. Em vez de esperar aparecer uma oportunidade, estudei o negócio da pessoa para quem eu trabalhava, montei uma ideia e pedi uma reunião para apresentar o projeto. 💡

Meus primeiros clientes vieram de pessoas que acompanharam meu trabalho, confiaram em mim e começaram a me indicar. Agora meu próximo desafio é construir um processo que não dependa somente de indicação.

#PrimeirosClientes #Empreendedorismo #Freelancer #MarketingDigital #DevBrasil"""
    },
    {
        "num": 2,
        "filename": "b3_02_vendi_maquina_50mil_com_100reais.mp4",
        "date_brt": "Quarta (29/07) - 16:30 BRT",
        "scheduledFor": "2026-07-29T19:30:00Z",
        "caption": """Meus primeiros clientes chegaram por confiança e indicação. Depois, comecei a testar se conseguiria alcançar pessoas que ainda não me conheciam. 📈

Em uma das campanhas, anunciei uma máquina de alto valor (R$30k a R$50k) e a venda aconteceu com aproximadamente R$100 investidos em mídia.

O anúncio não trabalhou sozinho: existiam produto, oferta, atendimento e negociação. Mas foi um sinal claro de que o canal funcionava!

#TrafegoPago #MetaAds #MarketingDigital #Vendas #Startups"""
    },
    {
        "num": 3,
        "filename": "b3_03_fluxo_de_trabalho_comeca_por_audio.mp4",
        "date_brt": "Quarta (29/07) - 22:30 BRT",
        "scheduledFor": "2026-07-30T01:30:00Z",
        "caption": """Quando tenho uma ideia, não espero chegar ao computador. Gravo um áudio, transformo em texto e organizo a próxima ação! 🎙️

Se a tarefa puder ser executada por um agente, envio a instrução. Se precisar de mais trabalho, deixo registrado. O maior benefício é não perder a ideia no momento em que ela aparece!

#Produtividade #InteligenciaArtificial #Automacao #AgentesDeIA #Python"""
    },
    {
        "num": 4,
        "filename": "b3_04_testei_api_vagas_ao_vivo.mp4",
        "date_brt": "Quinta (30/07) - 11:30 BRT",
        "scheduledFor": "2026-07-30T14:30:00Z",
        "caption": """Pedi para a API encontrar vagas de técnico de segurança. Na primeira tentativa, ela explicou a profissão em vez de apresentar vagas! 🤦‍♀️

Depois de corrigir a solicitação, apareceram alguns resultados, mas vários estavam pouco relevantes. Minha nota foi 4/10. Ferramenta gratuita também precisa ser testada antes de ir pra produção!

#APIs #Programacao #VagasDeEmprego #InteligenciaArtificial #DevLife"""
    },
    {
        "num": 5,
        "filename": "b3_05_api_que_transforma_sites_em_dados.mp4",
        "date_brt": "Quinta (30/07) - 15:30 BRT",
        "scheduledFor": "2026-07-30T18:30:00Z",
        "caption": """A Microlink recebe uma URL e pode retornar metadados, captura de tela, PDF, paleta de cores e outras informações da página. 🌐⚡

Isso é incrível para criar previews, monitorar páginas, arquivar versões e alimentar processos automáticos com dados estruturados.

#Microlink #APIs #AutomacaoWeb #Programacao #Tech"""
    },
    {
        "num": 6,
        "filename": "b3_06_api_gratuita_banco_mundial.mp4",
        "date_brt": "Quinta (30/07) - 19:30 BRT",
        "scheduledFor": "2026-07-30T22:30:00Z",
        "caption": """O Banco Mundial mantém uma API pública com milhares de séries de indicadores econômicos, sociais e demográficos. 📊🏦

Ela ajuda a entender o contexto macro do mercado: população, urbanização, renda, emprego, acesso à internet e vários outros indicadores!

#Dados #BancoMundial #PesquisaDeMercado #APIs #Economia"""
    }
]

print("=" * 60)
print("AGENDANDO OS 6 NOVOS VÍDEOS APROVADOS DA MINUTAGEM NO TIKTOK")
print("=" * 60)

success_count = 0
for item in approved_b3:
    filepath = os.path.join(out_dir, item["filename"])
    if not os.path.exists(filepath):
        print(f"❌ Não encontrado: {filepath}")
        continue

    filesize = os.path.getsize(filepath)
    print(f"\n🚀 Agendando [{item['num']}/6]: {item['filename']} ({round(filesize/1024/1024, 2)} MB)")
    print(f"📅 Data programada: {item['date_brt']}")

    r_init = requests.post("https://api.woopsocial.com/v1/media/upload-sessions",
                           headers=headers, json={"projectId": project_id, "fileSizeInBytes": filesize})
    if r_init.status_code not in (200, 201):
        print(f"❌ Err init: {r_init.status_code} {r_init.text}")
        continue

    sess_data = r_init.json()
    upload_session_id = sess_data["uploadSessionId"]
    part_size = sess_data.get("partSizeInBytes", 10485760)
    parts = sess_data.get("parts", [])

    with open(filepath, "rb") as f:
        for part in parts:
            chunk = f.read(part_size)
            requests.put(part["uploadUrl"], data=chunk)

    r_comp = requests.post(f"https://api.woopsocial.com/v1/media/upload-sessions/{upload_session_id}/complete", headers=headers)
    if r_comp.status_code not in (200, 201):
        print(f"❌ Complete err: {r_comp.status_code}")
        continue

    media_id = r_comp.json()["mediaId"]

    post_payload = {
        "content": [{"media": [{"mediaId": media_id, "type": "MEDIA_LIBRARY"}], "text": item["caption"]}],
        "schedule": {"type": "SCHEDULE_FOR_LATER", "scheduledFor": item["scheduledFor"]},
        "socialAccounts": [{
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
        }]
    }

    r_post = requests.post("https://api.woopsocial.com/v1/posts", headers=headers, json=post_payload)
    if r_post.status_code in (200, 201):
        post_id = r_post.json().get("id", "OK")
        print(f"🎉 SUCESSO! Post ID: {post_id}")
        success_count += 1
    else:
        print(f"❌ Erro post: {r_post.status_code} {r_post.text}")
    
    time.sleep(1.5)

print("\n" + "=" * 60)
print(f"FINALIZADO: {success_count}/6 vídeos agendados com sucesso!")
print("=" * 60)
