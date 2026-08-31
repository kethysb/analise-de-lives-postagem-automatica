"""
Script de Agendamento do Bloco 2 no TikTok via WoopSocial
Como todas as 9 mídias já foram enviadas com sucesso no WoopSocial,
usamos diretamente os mediaIDs gerados para criar os posts!
"""
import os
import requests
import json
import sys
import time

sys.stdout.reconfigure(encoding='utf-8')

api_key = "wsk_41af245d7b2919a4.53bec0a4a1113b33136381c74004db06ffed1831729ba4381d637dc95aa91bea"
tiktok_account_id = "154633727815712768" # @kthyeu

headers = {
    "Authorization": f"Bearer {api_key}",
    "Content-Type": "application/json"
}

# MediaIDs já enviados com sucesso na tentativa anterior
calendar_bloco2 = [
    {
        "num": 1,
        "name": "b2_01_o_problema_nao_era_cobrar_barato.mp4",
        "media_id": "155883429555077120",
        "date_brt": "Segunda, 03/08 - 12:00",
        "scheduledFor": "2026-08-03T15:00:00Z",
        "caption": """O problema nunca foi cobrar barato, mas sim o modelo de entrega! 💡
No início do projeto, cobrei um valor baixo pensando no volume. Mas quando a demanda cresceu, o custo operacional e o suporte viraram um gargalo enorme.

Você já passou por isso ao precificar um serviço de tecnologia?

#Tecnologia #Empreendedorismo #Desenvolvimento #DevBrasil #SoftwareHouse #IA"""
    },
    {
        "num": 2,
        "name": "b2_02_eu_amo_trabalhar_mas_odeio_ser_cobrada.mp4",
        "media_id": "155883486153015296",
        "date_brt": "Segunda, 03/08 - 20:00",
        "scheduledFor": "2026-08-03T23:00:00Z",
        "caption": """Eu amo trabalhar e criar sistemas do zero, mas odeio ter alguém me cobrando o tempo todo! 😂
Foi exatamente por isso que decidi automatizar processos e criar produtos próprios. A liberdade de construir no meu ritmo vale qualquer desafio.

E você, prefere trabalhar com prazos rígidos de terceiros ou gerenciar seus próprios projetos?

#Programacao #DevLife #Autonomia #Freelancer #Devs"""
    },
    {
        "num": 3,
        "name": "b2_03_por_que_sistemas_em_nuvem_sao_caros.mp4",
        "media_id": "155883542524461056",
        "date_brt": "Terça, 04/08 - 12:00",
        "scheduledFor": "2026-08-04T15:00:00Z",
        "caption": """Por que manter sistemas na nuvem fica tão caro de uma hora para outra? ☁️💸
Muita gente acha que criar o app é o maior custo, mas o investimento real está na infraestrutura, bancos de dados escaláveis, balanceamento e segurança.

#Cloud #AWS #DevOps #Backend #Programacao #Infraestrutura"""
    },
    {
        "num": 4,
        "name": "b2_04_o_medo_de_lancar_esta_me_atrasando.mp4",
        "media_id": "155883616281296896",
        "date_brt": "Terça, 04/08 - 20:00",
        "scheduledFor": "2026-08-04T23:00:00Z",
        "caption": """Eu já poderia ter lançado o sistema há semanas, mas o medo de entregar algo incompleto estava me atrasando. 🚀
O perfeccionismo às vezes é o maior inimigo do lançamento. É preciso aprender a lançar a primeira versão, colher feedbacks reais e evoluir rápido.

#Startups #MVP #Produto #Desenvolvimento #Programador"""
    },
    {
        "num": 5,
        "name": "b2_05_o_sistema_que_estou_construindo.mp4",
        "media_id": "155883692961562624",
        "date_brt": "Quarta, 05/08 - 12:00",
        "scheduledFor": "2026-08-05T15:00:00Z",
        "caption": """Um spoiler rápido do sistema de automação que estou construindo! 🛠️🤖
A ideia é transformar dados brutos em fluxos completos de conteúdo e automação em 24h, sem perder a autenticidade humana na edição.

#InteligenciaArtificial #Automation #Python #EngenhariaDeSoftware #Tech"""
    },
    {
        "num": 6,
        "name": "b2_06_como_estudar_virais_sem_copiar.mp4",
        "media_id": "155883764226981888",
        "date_brt": "Quarta, 05/08 - 20:00",
        "scheduledFor": "2026-08-05T23:00:00Z",
        "caption": """Como estudar vídeos virais sem cair na armadilha de apenas copiar! 📈
Estudar tendências significa analisar a estrutura: a força do gancho, a retenção visual, a velocidade de corte e a entrega do valor final.

#CriaçãoDeConteúdo #EstratégiaDigital #Virais #MarketingDigital #SocialMedia"""
    },
    {
        "num": 7,
        "name": "b2_07_antes_de_criar_um_app_faca_isso.mp4",
        "media_id": "155883820346769408",
        "date_brt": "Quinta, 06/08 - 12:00",
        "scheduledFor": "2026-08-06T15:00:00Z",
        "caption": """Antes de escrever qualquer linha de código para o seu app, faça isso! ⚠️
Codar é a parte divertida. O erro clássico de todo dev é passar meses programando algo que ninguém realmente precisa. Valide a dor do público primeiro.

#Programador #Software #DicasDeDev #NegóciosDigitais #Startups"""
    },
    {
        "num": 8,
        "name": "b2_r01_nunca_trabalhei_clt.mp4",
        "media_id": "155883873937391616",
        "date_brt": "Quinta, 06/08 - 20:00",
        "scheduledFor": "2026-08-06T23:00:00Z",
        "caption": """Nunca trabalhei de carteira assinada (CLT). Minha trajetória foi direto no digital e projetos próprios. 💭
Tem dias em que me pergunto se ter pulado a experiência corporativa foi bom ou ruim, mas a bagagem prática resolvendo problemas reais não tem preço.

#CarreiraTech #Freelancer #TrabalhoRemoto #Autonoma #Dev"""
    },
    {
        "num": 9,
        "name": "b2_r02_o_erro_de_seguranca_que_cometo.mp4",
        "media_id": "155883915804934144",
        "date_brt": "Sexta, 07/08 - 12:00",
        "scheduledFor": "2026-08-07T15:00:00Z",
        "caption": """O erro de segurança que quase me custou caro no passado. 🔒🚨
Subir arquivos com chaves de API desprotegidas ou sem isolamento é um risco gigante. Depois disso, verificação em dois fatores e variáveis de ambiente viraram lei!

#SegurancaDaInformacao #CyberSecurity #DevOps #Python #Desenvolvimento"""
    }
]

def schedule_post(item):
    print(f"\n🚀 Agendando [{item['num']}/9]: {item['name']}")
    print(f"📅 Data: {item['date_brt']}")

    post_payload = {
        "content": [
            {
                "media": [
                    {
                        "mediaId": item["media_id"],
                        "type": "MEDIA_LIBRARY"
                    }
                ],
                "text": item["caption"]
            }
        ],
        "schedule": {
            "type": "SCHEDULE_FOR_LATER",
            "scheduledFor": item["scheduledFor"]
        },
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

    r_post = requests.post("https://api.woopsocial.com/v1/posts", headers=headers, json=post_payload)
    if r_post.status_code in (200, 201):
        post_id = r_post.json().get("id", "OK")
        print(f"🎉 VÍDEO AGENDADO COM SUCESSO! Post ID: {post_id}")
        return True
    else:
        print(f"❌ Erro ao agendar: {r_post.status_code} - {r_post.text}")
        return False

print("=" * 60)
print("CRIANDO AGENDAMENTOS NO TIKTOK VIA WOOPSOCIAL")
print("=" * 60)

success_count = 0
for item in calendar_bloco2:
    if schedule_post(item):
        success_count += 1
    time.sleep(1.5)

print("\n" + "=" * 60)
print(f"RESULTADO: {success_count}/9 vídeos agendados com sucesso!")
print("=" * 60)
