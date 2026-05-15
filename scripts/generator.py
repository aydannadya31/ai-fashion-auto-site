import os
import json
import requests
import base64
import time
import random

CF_API_TOKEN = os.environ["CF_API_TOKEN"]
CF_ACCOUNT_ID = os.environ["CF_ACCOUNT_ID"]

url = f"https://api.cloudflare.com/client/v4/accounts/{CF_ACCOUNT_ID}/ai/run/@cf/black-forest-labs/flux-1-schnell"

headers = {
    "Authorization": f"Bearer {CF_API_TOKEN}",
    "Content-Type": "application/json"
}

with open("data.json", "r", encoding="utf-8") as f:
    data = json.load(f)

if isinstance(data, list):
    data = data[0]

styles = [
    "editorial runway fashion",
    "luxury fashion studio shoot",
    "cinematic high fashion portrait",
    "avant-garde magazine cover"
]

style = random.choice(styles)

base_prompt = f"""
{data.get('model','')},
{data.get('clothing','')},
{data.get('scene','')},
{data.get('environment','')},
{data.get('technical','')},
{style},
ultra realistic fashion photography
"""

print("Prompt created")

def generate(i):
    res = requests.post(url, headers=headers, json={"prompt": base_prompt})

    print("STATUS:", res.status_code)

    result = res.json()

    img = base64.b64decode(result["result"]["image"])

    os.makedirs("content/images", exist_ok=True)

    path = f"content/images/fashion_{int(time.time())}_{i}.jpg"

    with open(path, "wb") as f:
        f.write(img)

    return path

paths = []

for i in range(4):
    paths.append(generate(i))
    time.sleep(1)

caption = f"AI Fashion Drop — {style}"

meta = {
    "style": style,
    "prompt": base_prompt,
    "images": paths,
    "caption": caption,
    "timestamp": int(time.time())
}

os.makedirs("content", exist_ok=True)

with open("content/post.json", "w") as f:
    json.dump(meta, f, indent=2)

print("LEVEL 4 COMPLETE")
