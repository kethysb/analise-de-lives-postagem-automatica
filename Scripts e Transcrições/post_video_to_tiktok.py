import os
import requests
import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

api_key = "wsk_41af245d7b2919a4.53bec0a4a1113b33136381c74004db06ffed1831729ba4381d637dc95aa91bea"
project_id = "151419457388937216"
tiktok_account_id = "154633727815712768" # @kthyeu

video_path = r"C:\Users\Kethely\Downloads\cortes_tiktok_editados\01_como_eu_encontrei_chatgpt_5reais.mp4"

caption_text = """Eu pagava cerca de R$ 5 para acessar o ChatGPT e o Codex em plataformas de revenda. Depois, os anúncios começaram a desaparecer e ficou bem mais difícil encontrar esses acessos.

Neste vídeo conto como funcionava na época da live. Lembrando que preços e políticas mudam sempre!

#IA #ChatGPT #Programacao #Tecnologia #DevBrasil"""

headers = {
    "Authorization": f"Bearer {api_key}",
    "Content-Type": "application/json"
}

file_size = os.path.getsize(video_path)
print(f"Video 01 file size: {file_size} bytes ({round(file_size/(1024*1024), 2)} MB)")

# Step 1: Create Upload Session
print("\n[Step 1/4] Creating WoopSocial Upload Session...")
sess_resp = requests.post(
    "https://api.woopsocial.com/v1/media/upload-sessions",
    headers=headers,
    json={"projectId": project_id, "fileSizeInBytes": file_size}
)

sess_data = sess_resp.json()
upload_session_id = sess_data.get("uploadSessionId")
part_size = sess_data.get("partSizeInBytes", 10485760)
parts = sess_data.get("parts", [])
print(f"Upload session created! ID: {upload_session_id}, Chunk size: {part_size} bytes, Parts count: {len(parts)}")

# Step 2: Upload file parts
print("\n[Step 2/4] Uploading video binary chunks to Cloudflare R2 presigned URLs...")
with open(video_path, "rb") as f:
    for idx, part in enumerate(parts):
        part_num = part.get("partNumber", idx + 1)
        upload_url = part["uploadUrl"]
        chunk = f.read(part_size)
        print(f"Uploading part {part_num}/{len(parts)} ({len(chunk)} bytes)...")
        put_resp = requests.put(upload_url, data=chunk)

# Step 3: Complete Upload Session
print("\n[Step 3/4] Completing Upload Session...")
comp_resp = requests.post(
    f"https://api.woopsocial.com/v1/media/upload-sessions/{upload_session_id}/complete",
    headers=headers
)

comp_data = comp_resp.json()
media_id = comp_data.get("mediaId")
print(f"SUCCESS! Media upload finalized! Media ID: {media_id}")

# Step 4: Publish Post directly to TikTok (@kthyeu)
print("\n[Step 4/4] Publishing Post to TikTok account @kthyeu...")

post_payload = {
    "content": [
        {
            "media": [
                {
                    "mediaId": media_id,
                    "type": "MEDIA_LIBRARY"
                }
            ],
            "text": caption_text
        }
    ],
    "schedule": {
        "type": "PUBLISH_NOW"
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

post_resp = requests.post(
    "https://api.woopsocial.com/v1/posts",
    headers=headers,
    json=post_payload
)

print(f"\nPublish Status Code: {post_resp.status_code}")
print("Publish Response:", json.dumps(post_resp.json(), indent=2))
