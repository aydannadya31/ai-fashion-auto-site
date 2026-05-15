import os
import json
import requests
import base64
import time
import random

# =========================
# CLOUDFARE CONFIG
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

print("Prompt created:")
print(base_prompt)

# =========================
# GENERATE MULTIPLE IMAGES
# =========================
def generate_image(prompt, index):
    payload = {"prompt": prompt}

    response = requests.post(url, headers=headers, json=payload)

    print(f"\n--- IMAGE {index} ---")
    print("STATUS:", response.status_code)
    print("RAW:", response.text[:200])

    if response.status_code != 200:
        raise Exception(response.text)

    result = response.json()

    if not result.get("success"):
        raise Exception(result)

    image_base64 = result["result"]["image"]
    image_bytes = base64.b64decode(image_base64)

    if len(image_bytes) < 1000:
        raise Exception("Empty image")

    os.makedirs("content/images", exist_ok=True)

    filename = f"fashion_{int(time.time())}_{index}.jpg"
    path = f"content/images/{filename}"

    with open(path, "wb") as f:
        f.write(image_bytes)

    print("Saved:", path)
    return path

# =========================
# RUN 4 IMAGES
# =========================
if __name__ == "__main__":
    paths = []

    for i in range(4):
        p = generate_image(base_prompt, i)
        paths.append(p)
        time.sleep(1)

    print("\nDONE:")
    print(paths)
import json
import os
import time

caption = f"""
AI Fashion Drop

Style: {style}
Concept: futuristic editorial fashion
Generated automatically by AI system
"""

meta = {
    "style": style,
    "prompt": base_prompt,
    "images": paths,
    "caption": caption,
    "timestamp": int(time.time())
}

os.makedirs("content", exist_ok=True)

with open("content/post.json", "w", encoding="utf-8") as f:
    json.dump(meta, f, indent=2)

print("\nMETA SAVED -> content/post.json")
