import requests, os, time, sys
sys.stdout.reconfigure(encoding='utf-8')

api_key = "wsk_41af245d7b2919a4.53bec0a4a1113b33136381c74004db06ffed1831729ba4381d637dc95aa91bea"
project_id = "151419457388937216"
tiktok_id = "154633727815712768"
headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}

# ── 1. Limpa media órfã ──────────────────────────────────────────────────────
print("=== PASSO 1: LIMPANDO STORAGE ===")
r = requests.get(f"https://api.woopsocial.com/v1/media?projectId={project_id}&limit=100", headers=headers)
all_media = r.json().get("media", [])
print(f"Total media no storage: {len(all_media)}")

url = f"https://api.woopsocial.com/v1/social-account-posts?projectId={project_id}"
all_posts = []
while url:
    rp = requests.get(url, headers=headers)
    data = rp.json()
    all_posts.extend(data.get("socialAccountPosts", []))
    cursor = data.get("nextCursor")
    url = f"https://api.woopsocial.com/v1/social-account-posts?projectId={project_id}&cursor={cursor}" if cursor else None

used_ids = set()
for p in all_posts:
    for c in p.get("content", []):
        for m in c.get("media", []):
            used_ids.add(m.get("mediaId"))

print(f"Media em uso por posts: {len(used_ids)}")

deleted = 0
freed = 0
for m in all_media:
    mid = m["id"]
    if mid not in used_ids:
        size = m.get("fileSizeInBytes", 0)
        rd = requests.delete(f"https://api.woopsocial.com/v1/media/{mid}", headers=headers)
        if rd.status_code in (200, 204):
            deleted += 1
            freed += size

print(f"Deletados: {deleted} arquivos órfãos | Liberado: {round(freed/1024/1024,2)} MB")

# ── 2. Agenda as 2 histórias que falharam ────────────────────────────────────
print("\n=== PASSO 2: AGENDANDO AS 2 HISTÓRIAS QUE FALTARAM ===")
OUT_DIR = r"C:\Users\Kethely\Downloads\cortes_narrativos_5historias"

remaining = [
    {
        "num": 4,
        "filename": "historia_04_testei_duas_apis_gratuitas_perdi_tempo.mp4",
        "scheduledFor": "2026-08-03T21:00:00Z",
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
        "scheduledFor": "2026-08-04T00:00:00Z",
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

success = 0
for item in remaining:
    filepath = os.path.join(OUT_DIR, item["filename"])
    filesize = os.path.getsize(filepath)
    print(f"\n🚀 [{item['num']}/5] {item['filename']} | 📅 {item['date_brt']} | {round(filesize/1024/1024,2)} MB")

    r_init = requests.post("https://api.woopsocial.com/v1/media/upload-sessions",
                           headers=headers, json={"projectId": project_id, "fileSizeInBytes": filesize})
    if r_init.status_code not in (200, 201):
        print(f"   ❌ Erro init: {r_init.status_code} {r_init.text[:120]}")
        continue

    sess = r_init.json()
    part_size = sess.get("partSizeInBytes", 10485760)
    parts = sess.get("parts", [])
    with open(filepath, "rb") as f:
        for part in parts:
            requests.put(part["uploadUrl"], data=f.read(part_size))

    r_comp = requests.post(
        f"https://api.woopsocial.com/v1/media/upload-sessions/{sess['uploadSessionId']}/complete",
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
            "socialAccountId": tiktok_id, "platform": "TIKTOK", "postMode": "DIRECT_POST",
            "postType": "VIDEO", "privacyLevel": "PUBLIC_TO_EVERYONE",
            "allowComment": True, "allowDuet": True, "allowStitch": True,
            "isYourBrand": False, "isBrandedContent": False, "autoAddMusic": True
        }]
    }
    r_post = requests.post("https://api.woopsocial.com/v1/posts", headers=headers, json=payload)
    if r_post.status_code in (200, 201):
        print(f"   🎉 SUCESSO! Post ID: {r_post.json().get('id')}")
        success += 1
    else:
        print(f"   ❌ Erro: {r_post.status_code} {r_post.text[:120]}")
    time.sleep(1.5)

print(f"\n✅ {success}/2 histórias restantes agendadas com sucesso!")
