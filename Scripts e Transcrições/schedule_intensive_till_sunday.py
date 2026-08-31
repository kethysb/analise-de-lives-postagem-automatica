"""
Script de Agendamento Intensivo com Tratamento de Erros e Retries
Garante a realocação de TODOS os 18 vídeos inéditos até Domingo (02/08).
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

dir_b1 = r"C:\Users\Kethely\Downloads\cortes_tiktok_editados"
dir_b2 = r"C:\Users\Kethely\Downloads\cortes_bloco2_editados"

intensive_queue = [
    # QUARTA (29/07 - Hoje)
    {"id": "01", "dir": dir_b1, "filename": "07_nao_coloque_codigo_empresa_chatgpt.mp4", "date_brt": "Quarta (29/07) - 12:00 BRT", "scheduledFor": "2026-07-29T15:00:00Z", "caption": "Usar IA para revisar código é extremamente útil. O problema é colar trechos confidenciais da empresa sem saber como os dados estão sendo tratados na plataforma! 🔒 #Programacao #CleanCode #Seguranca #Dev"},
    {"id": "02", "dir": dir_b1, "filename": "09_beneficios_para_empresas.mp4", "date_brt": "Quarta (29/07) - 15:00 BRT", "scheduledFor": "2026-07-29T18:00:00Z", "caption": "Descobri uma plataforma que reúne benefícios, créditos e períodos gratuitos oferecidos por grandes empresas de tecnologia para startups e negócios cadastrados. 🚀 #Startups #Negocios #Tech"},
    {"id": "03", "dir": dir_b1, "filename": "10_5mil_dolares_creditos_ia.mp4", "date_brt": "Quarta (29/07) - 18:00 BRT", "scheduledFor": "2026-07-29T21:00:00Z", "caption": "Quando encontrei esse programa, o valor que mais chamou atenção foi US$ 5 mil em créditos de IA. Entenda como funcionam esses incentivos e o que é exigido. 💻 #Azure #Microsoft #IA"},
    {"id": "04", "dir": dir_b1, "filename": "11_3reais_por_100dolares_creditos.mp4", "date_brt": "Quarta (29/07) - 21:00 BRT", "scheduledFor": "2026-07-30T00:00:00Z", "caption": "Durante a live, mostrei uma plataforma onde poucos reais liberavam US$ 100 de saldo interno. Entenda a relação entre o preço do saldo e o consumo dos modelos! 📊 #Tokens #LLM #IA"},

    # QUINTA (30/07)
    {"id": "05", "dir": dir_b1, "filename": "12_quanto_gastei_usando_apis.mp4", "date_brt": "Quinta (30/07) - 09:00 BRT", "scheduledFor": "2026-07-30T12:00:00Z", "caption": "Mostrei no painel um consumo de 7 milhões de tokens por US$ 2,42 e 1 milhão de tokens no Claude. Saiba por que é essencial acompanhar o gasto exato por modelo! 💵 #Claude #OpenAI #Tokens"},
    {"id": "06", "dir": dir_b1, "filename": "13_almoco_gratis_ia_vai_acabar.mp4", "date_brt": "Quinta (30/07) - 13:00 BRT", "scheduledFor": "2026-07-30T16:00:00Z", "caption": "A gente está aproveitando a fase do 'almoço grátis' da inteligência artificial, mas essa fase de subsídio não dura para sempre. Aprenda a usar modelos Open Source! 🤖 #OpenSource #Llama #IA"},
    {"id": "07", "dir": dir_b1, "filename": "08_minha_diversao_virou_trabalhar.mp4", "date_brt": "Quinta (30/07) - 17:00 BRT", "scheduledFor": "2026-07-30T20:00:00Z", "caption": "Eu amava jogar Valorant e passar horas no computador. Mas quando passei a trabalhar o dia inteiro na tela, minha diversão virou trabalhar — e ao terminar, só quero sair da frente do PC! 🎮 #DevLife #Gamer"},
    {"id": "08", "dir": dir_b1, "filename": "14_ia_me_ensinou_a_aprender.mp4", "date_brt": "Quinta (30/07) - 21:00 BRT", "scheduledFor": "2026-07-31T00:00:00Z", "caption": "A maior mudança que a IA trouxe para mim não foi fazer código por mim, mas me ensinar a aprender do jeito certo: com artigos científicos, evidências e autonomia! 📚 #Estudos #Produtividade"},

    # SEXTA (31/07)
    {"id": "09", "dir": dir_b1, "filename": "15_psicologia_ia_e_programacao.mp4", "date_brt": "Sexta (31/07) - 09:00 BRT", "scheduledFor": "2026-07-31T12:00:00Z", "caption": "Como a faculdade de Psicologia, o estudo da neurociência e a programação se conectam no meu dia a dia para criar e resolver problemas de forma única! 🧠💻 #Neurociencia #Psicologia #Programacao"},
    {"id": "10", "dir": dir_b2, "filename": "b2_01_o_problema_nao_era_cobrar_barato.mp4", "date_brt": "Sexta (31/07) - 13:00 BRT", "scheduledFor": "2026-07-31T16:00:00Z", "caption": "O problema nunca foi cobrar barato, mas sim o modelo de entrega! 💡 No início do projeto, cobrei um valor baixo pensando no volume. Mas quando a demanda cresceu, virou um gargalo. #Tecnologia #Dev"},
    {"id": "11", "dir": dir_b2, "filename": "b2_02_eu_amo_trabalhar_mas_odeio_ser_cobrada.mp4", "date_brt": "Sexta (31/07) - 17:00 BRT", "scheduledFor": "2026-07-31T20:00:00Z", "caption": "Eu amo trabalhar e criar sistemas do zero, mas odeio ter alguém me cobrando o tempo todo! 😂 Foi por isso que decidi automatizar processos e criar produtos próprios. #Programacao #Autonomia"},
    {"id": "12", "dir": dir_b2, "filename": "b2_03_por_que_sistemas_em_nuvem_sao_caros.mp4", "date_brt": "Sexta (31/07) - 21:00 BRT", "scheduledFor": "2026-08-01T00:00:00Z", "caption": "Por que manter sistemas na nuvem fica tão caro de uma hora para outra? ☁️💸 Muita gente acha que criar o app é o maior custo, mas o investimento real está na infraestrutura e segurança. #Cloud #AWS"},

    # SÁBADO (01/08)
    {"id": "13", "dir": dir_b2, "filename": "b2_04_o_medo_de_lancar_esta_me_atrasando.mp4", "date_brt": "Sábado (01/08) - 10:00 BRT", "scheduledFor": "2026-08-01T13:00:00Z", "caption": "Eu já poderia ter lançado o sistema há semanas, mas o medo de entregar algo incompleto estava me atrasando. 🚀 O perfeccionismo às vezes é o maior inimigo do lançamento. #Startups #MVP"},
    {"id": "14", "dir": dir_b2, "filename": "b2_05_o_sistema_que_estou_construindo.mp4", "date_brt": "Sábado (01/08) - 15:00 BRT", "scheduledFor": "2026-08-01T18:00:00Z", "caption": "Um spoiler rápido do sistema de automação que estou construindo! 🛠️🤖 A ideia é transformar dados brutos em fluxos completos de conteúdo e automação em 24h. #InteligenciaArtificial #Automation"},
    {"id": "15", "dir": dir_b2, "filename": "b2_06_como_estudar_virais_sem_copiar.mp4", "date_brt": "Sábado (01/08) - 20:00 BRT", "scheduledFor": "2026-08-01T23:00:00Z", "caption": "Como estudar vídeos virais sem cair na armadilha de apenas copiar! 📈 Estudar tendências significa analisar a estrutura: a força do gancho, retenção visual e ritmo. #MarketingDigital #Virais"},

    # DOMINGO (02/08)
    {"id": "16", "dir": dir_b2, "filename": "b2_07_antes_de_criar_um_app_faca_isso.mp4", "date_brt": "Domingo (02/08) - 10:00 BRT", "scheduledFor": "2026-08-02T13:00:00Z", "caption": "Antes de escrever qualquer linha de código para o seu app, faça isso! ⚠️ Codar é a parte divertida. O erro clássico de todo dev é passar meses programando o que ninguém quer. Valide antes. #Software"},
    {"id": "17", "dir": dir_b2, "filename": "b2_r01_nunca_trabalhei_clt.mp4", "date_brt": "Domingo (02/08) - 15:00 BRT", "scheduledFor": "2026-08-02T18:00:00Z", "caption": "Nunca trabalhei de carteira assinada (CLT). Minha trajetória foi direto no digital e projetos próprios. 💭 A bagagem prática resolvendo problemas não tem preço. #CarreiraTech #Autonoma"},
    {"id": "18", "dir": dir_b2, "filename": "b2_r02_o_erro_de_seguranca_que_cometo.mp4", "date_brt": "Domingo (02/08) - 20:00 BRT", "scheduledFor": "2026-08-02T23:00:00Z", "caption": "O erro de segurança que quase me custou caro no passado. 🔒🚨 Subir arquivos com chaves de API desprotegidas é um risco gigante. 2FA e var de ambiente viraram lei! #CyberSecurity #DevOps"}
]

def process_item(item):
    filepath = os.path.join(item["dir"], item["filename"])
    if not os.path.exists(filepath):
        print(f"❌ Arquivo não encontrado: {filepath}")
        return False

    filesize = os.path.getsize(filepath)
    print(f"\n🚀 Processing [{item['id']}]: {item['filename']} ({round(filesize/1024/1024, 2)} MB)")
    print(f"📅 Agendando para: {item['date_brt']}")

    # Tentativa com Retry
    for attempt in range(3):
        r_init = requests.post("https://api.woopsocial.com/v1/media/upload-sessions",
                               headers=headers, json={"projectId": project_id, "fileSizeInBytes": filesize})
        if r_init.status_code in (200, 201):
            break
        print(f"  ⚠️ Tentativa {attempt+1} falhou com código {r_init.status_code}. Aguardando 3s...")
        time.sleep(3)

    if r_init.status_code not in (200, 201):
        print(f"❌ Erro definitivo ao criar sessão de upload: {r_init.status_code} - {r_init.text}")
        return False

    sess_data = r_init.json()
    upload_session_id = sess_data["uploadSessionId"]
    part_size = sess_data.get("partSizeInBytes", 10485760)
    parts = sess_data.get("parts", [])

    with open(filepath, "rb") as f:
        for idx, part in enumerate(parts):
            url = part["uploadUrl"]
            chunk = f.read(part_size)
            r_part = requests.put(url, data=chunk)
            if r_part.status_code not in (200, 201, 204):
                print(f"❌ Erro upload parte {idx+1}")
                return False

    r_comp = requests.post(f"https://api.woopsocial.com/v1/media/upload-sessions/{upload_session_id}/complete", headers=headers)
    if r_comp.status_code not in (200, 201):
        print(f"❌ Erro ao finalizar upload: {r_comp.status_code}")
        return False

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
        pid = r_post.json().get("id", "OK")
        print(f"🎉 VÍDEO AGENDADO COM SUCESSO! Post ID: {pid}")
        return True
    else:
        print(f"❌ Erro ao criar post: {r_post.status_code} - {r_post.text}")
        return False

print("=" * 60)
print("EXECUÇÃO DE RE-AGENDAMENTO INTENSIVO ATÉ DOMINGO (02/08)")
print("=" * 60)

ok_count = 0
for item in intensive_queue:
    if process_item(item):
        ok_count += 1
    time.sleep(2)

print("\n" + "=" * 60)
print(f"FINALIZADO: {ok_count}/{len(intensive_queue)} vídeos agendados!")
print("=" * 60)
