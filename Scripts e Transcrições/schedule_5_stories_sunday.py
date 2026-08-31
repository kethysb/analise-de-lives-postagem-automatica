"""
Agenda as 5 Histórias Narrativas TODAS no Domingo 03/08
Horários: 09:00 / 12:00 / 15:00 / 18:00 / 21:00 BRT
"""
import os, requests, time, sys
sys.stdout.reconfigure(encoding='utf-8')

API_KEY = "wsk_41af245d7b2919a4.53bec0a4a1113b33136381c74004db06ffed1831729ba4381d637dc95aa91bea"
PROJECT_ID = "151419457388937216"
TIKTOK_ID = "154633727815712768"
OUT_DIR = r"C:\Users\Kethely\Downloads\cortes_narrativos_5historias"

headers = {"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"}

videos = [
    {
        "num": 1,
        "filename": "historia_01_do_perfume_a_maquina_50k.mp4",
        "scheduledFor": "2026-08-03T12:00:00Z",  # 09:00 BRT
        "date_brt": "Domingo (03/08) às 09:00 BRT",
        "caption": """Eu comecei vendendo perfume como freelancer e ganhava R$70 por dia.

Em vez de só vender, comecei a observar o negócio. Estudei a empresa, montei uma ideia e pedi uma reunião para apresentar o projeto.

Foi assim que conquistei os primeiros clientes: pela confiança.

Depois quis descobrir se conseguiria vender para pessoas que não me conheciam. Fiz tráfego pago para uma máquina que custava entre R$30 mil e R$50 mil. A venda aconteceu com aproximadamente R$100 investidos.

Vendedora ambulante → cliente por confiança → primeira venda por tráfego pago. Cada etapa foi real.

#Empreendedorismo #TrafegoPago #PrimeirosClientes #MarketingDigital #Freelancer #JornadaEmpreendedora"""
    },
    {
        "num": 2,
        "filename": "historia_02_ia_estudar_psicologia_para_construir_ia.mp4",
        "scheduledFor": "2026-08-03T15:00:00Z",  # 12:00 BRT
        "date_brt": "Domingo (03/08) às 12:00 BRT",
        "caption": """Quando comecei a usar IA na faculdade, eu transformava o material em questões e minha nota melhorou.

Mas percebi que tirar nota não significava entender o conteúdo de verdade. Então passei a buscar artigos, pensar em aplicações e estudar como profissional.

Hoje aconteceu uma inversão: eu não estou usando IA para estudar Psicologia.

Estou usando Psicologia para construir um sistema de IA.

No processo seletivo, penso em quanto tempo a pessoa ficará na tela, quando começa a ficar cansativo e como estruturar a jornada do candidato.

Eu nunca imaginei trabalhar com tecnologia. Mas consegui juntar as áreas de que gosto.

Mas ainda tenho muito a aprender. 🧠

#Psicologia #InteligenciaArtificial #DesenvolvimentoPessoal #UX #Programacao #JornadaEmpreendedora"""
    },
    {
        "num": 3,
        "filename": "historia_03_clientes_baratos_agencia_automatica.mp4",
        "scheduledFor": "2026-08-03T18:00:00Z",  # 15:00 BRT
        "date_brt": "Domingo (03/08) às 15:00 BRT",
        "caption": """Eu comecei prestando serviços, mas tive uma experiência que me desgastou muito.

Quando o pacote não estava bem definido e o preço era baixo, parecia que a pessoa tinha comprado minha disponibilidade inteira. Estava trabalhando todos os dias, sem folga, respondendo cobrança o tempo todo.

O problema é que eu amo criar projetos. O que eu odeio é perder autonomia.

Foi daí que surgiu a vontade de criar uma plataforma automática: a empresa coloca os dados e recebe posts e vídeos prontos para 30 dias.

O desafio é fazer isso sem o conteúdo ter cara de IA genérica.

Eu não quero parar de trabalhar. Quero criar um produto que não dependa de eu executar cada tarefa manualmente para cada cliente.

#AgenciaDigital #Automacao #Empreendedorismo #Marketing #Escalabilidade #JornadaEmpreendedora"""
    },
    {
        "num": 4,
        "filename": "historia_04_testei_duas_apis_gratuitas_perdi_tempo.mp4",
        "scheduledFor": "2026-08-03T21:00:00Z",  # 18:00 BRT
        "date_brt": "Domingo (03/08) às 18:00 BRT",
        "caption": """Eu separei várias APIs gratuitas porque queria automatizar partes dos meus projetos.

Na primeira, pedi para encontrar vagas de técnico de segurança. Em vez de mostrar vagas, ela começou a explicar o que um técnico de segurança faz.

Corrigi o pedido. Os resultados continuaram fracos. Dei nota 4.

Depois testei uma API financeira. Achei que conseguiria usá-la para entender o mercado de uma serraria. Quando fui testar, descobri que ela trabalhava principalmente com empresas de capital aberto.

Também não servia para o meu problema.

No fim, as duas APIs eram gratuitas. Mas eu gastei um bom tempo descobrindo que não resolveriam o que eu precisava.

Gratuito não é barato quando custa horas de teste. 🧪

#APIs #Programacao #InteligenciaArtificial #DevLife #Automacao #Aprendizado"""
    },
    {
        "num": 5,
        "filename": "historia_05_minha_plataforma_esta_pronta_o_problema_sou_eu.mp4",
        "scheduledFor": "2026-08-04T00:00:00Z",  # 21:00 BRT do Domingo 03/08
        "date_brt": "Domingo (03/08) às 21:00 BRT",
        "caption": """Estou construindo uma plataforma que cria posts e vídeos para empresas.

Ela já está quase pronta. Mas eu ainda não coloquei tráfego, não mostrei direito e nem comecei a vender.

Não é porque não acredito no projeto.

É porque tenho medo de colocar algo no mercado antes de ter certeza de que funciona.

Eu sei que já poderia ter lançado uma versão há bastante tempo. Só que sempre vejo algo que poderia ficar melhor. Não consigo entregar algo que considero meia-boca.

E eu sei que isso está me prejudicando, porque enquanto tento deixar perfeito, continuo trabalhando todos os dias sem lançar.

O problema não é o produto. O problema sou eu. 🚀

#Empreendedorismo #Lancamento #Produto #Perfeccionismo #Startup #JornadaEmpreendedora"""
    }
]

print("=" * 60)
print("AGENDANDO AS 5 HISTÓRIAS — TUDO NO DOMINGO 03/08")
print("=" * 60)

success = 0
for item in videos:
    filepath = os.path.join(OUT_DIR, item["filename"])
    if not os.path.exists(filepath):
        print(f"❌ Arquivo não encontrado: {filepath}")
        continue

    filesize = os.path.getsize(filepath)
    print(f"\n🚀 [{item['num']}/5] {item['filename']}")
    print(f"   📅 {item['date_brt']} | {round(filesize/1024/1024, 2)} MB")

    r_init = requests.post("https://api.woopsocial.com/v1/media/upload-sessions",
                           headers=headers, json={"projectId": PROJECT_ID, "fileSizeInBytes": filesize})
    if r_init.status_code not in (200, 201):
        print(f"   ❌ Erro init: {r_init.status_code} {r_init.text[:100]}")
        continue

    sess = r_init.json()
    upload_session_id = sess["uploadSessionId"]
    part_size = sess.get("partSizeInBytes", 10485760)
    parts = sess.get("parts", [])

    with open(filepath, "rb") as f:
        for part in parts:
            chunk = f.read(part_size)
            requests.put(part["uploadUrl"], data=chunk)

    r_comp = requests.post(
        f"https://api.woopsocial.com/v1/media/upload-sessions/{upload_session_id}/complete",
        headers=headers
    )
    if r_comp.status_code not in (200, 201):
        print(f"   ❌ Erro complete: {r_comp.status_code}")
        continue

    media_id = r_comp.json()["mediaId"]

    payload = {
        "content": [{"media": [{"mediaId": media_id, "type": "MEDIA_LIBRARY"}], "text": item["caption"]}],
        "schedule": {"type": "SCHEDULE_FOR_LATER", "scheduledFor": item["scheduledFor"]},
        "socialAccounts": [{
            "socialAccountId": TIKTOK_ID,
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

    r_post = requests.post("https://api.woopsocial.com/v1/posts", headers=headers, json=payload)
    if r_post.status_code in (200, 201):
        post_id = r_post.json().get("id", "OK")
        print(f"   🎉 SUCESSO! Post ID: {post_id}")
        success += 1
    else:
        print(f"   ❌ Erro post: {r_post.status_code} {r_post.text[:150]}")

    time.sleep(1.5)

print("\n" + "=" * 60)
print(f"FINALIZADO: {success}/5 histórias agendadas no Domingo 03/08!")
print("=" * 60)
