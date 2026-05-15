import os
import json
import requests
import base64
import time
import random

# =========================
# CONFIG
# =========================
CF_API_TOKEN = os.environ["CF_API_TOKEN"]
CF_ACCOUNT_ID = os.environ["CF_ACCOUNT_ID"]

url = f"https://api.cloudflare.com/client/v4/accounts/{CF_ACCOUNT_ID}/ai/run/@cf/black-forest-labs/flux-1-schnell"

headers = {
    "Authorization": f"Bearer {CF_API_TOKEN}",
    "Content-Type": "application/json"
}

# =========================
# LOAD DATA
# =========================
with open("data.json", "r", encoding="utf-8") as f:
    data = json.load(f)

if isinstance(data, list):
    data = data[0]

model = data.get("model", "")
clothing = data.get("clothing", "")
scene = data.get("scene", "")
environment = data.get("environment", "")
technical = data.get("technical", "")

# =========================
# STYLE VARIANTS
# =========================
styles = [
    "editorial runway fashion photography",
    "luxury high-end studio shoot",
    "cinematic fashion portrait lighting",
    "avant-garde fashion magazine cover"
]

style = random.choice(styles)

# =========================
# PROMPT
# =========================
base_prompt = f"""
{model},
{clothing},
{scene},
{environment},
{technical},
{style},
ultra realistic fashion photography, cinematic lighting, high detail
"""

print("Prompt created")
print(base_prompt)

# =========================
# IMAGE GENERATION
# =========================
BASE_URL = "https://raw.githubusercontent.com/aydannadya31/ai-fashion-auto-site/main/"

def generate(i):
    res = requests.post(url, headers=headers, json={"prompt": base_prompt})

    print("\nSTATUS:", res.status_code)

    result = res.json()

    img = base64.b64decode(result["result"]["image"])

    os.makedirs("content/images", exist_ok=True)

    filename = f"fashion_{int(time.time())}_{i}.jpg"
    local_path = f"content/images/{filename}"

    with open(local_path, "wb") as f:
        f.write(img)

    # 🔥 IMPORTANT FIX: PUBLIC URL
    public_url = BASE_URL + local_path

    print("Saved:", public_url)

    return public_url

# =========================
# RUN 4 IMAGES
# =========================
paths = []

for i in range(4):
    paths.append(generate(i))
    time.sleep(1)

# =========================
# POST JSON (FEED)
# =========================
os.makedirs("content", exist_ok=True)

post = {
    "style": style,
    "prompt": base_prompt,
    "images": paths,
    "caption": f"AI Fashion Drop — {style}",
    "timestamp": int(time.time())
}

with open("content/post.json", "w", encoding="utf-8") as f:
    json.dump(post, f, indent=2)

print("\nPOST CREATED -> content/post.json")
print("DONE ✔ SYSTEM READY")
