import os
import json
import requests
import base64
import time

# =========================
# CLOUDFARE CONFIG
# =========================
CF_API_TOKEN = os.environ["CF_API_TOKEN"]
CF_ACCOUNT_ID = os.environ["CF_ACCOUNT_ID"]

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
negative = data.get("negative", "")

# =========================
# PROMPT
# =========================
prompt = f"""
{model},
{clothing},
{scene},
{environment},
{technical},
ultra realistic fashion photography, cinematic lighting, editorial style
"""

print("Prompt created:")
print(prompt)

# =========================
# IMAGE GENERATION
# =========================
def generate_image(prompt):
    url = f"https://api.cloudflare.com/client/v4/accounts/{CF_ACCOUNT_ID}/ai/run/@cf/black-forest-labs/flux-1-schnell"

    headers = {
        "Authorization": f"Bearer {CF_API_TOKEN}",
        "Content-Type": "application/json"
    }

    payload = {
        "prompt": prompt
    }

    response = requests.post(url, headers=headers, json=payload)

    print("STATUS:", response.status_code)
    print("RAW RESPONSE:", response.text[:500])

    if response.status_code != 200:
        raise Exception(f"HTTP ERROR: {response.text}")

    try:
        result = response.json()
    except Exception:
        raise Exception(f"Invalid JSON response: {response.text}")

    if not result.get("success"):
        raise Exception(f"Cloudflare error: {result}")

    image_base64 = result["result"]["image"]

    image_bytes = base64.b64decode(image_base64)

    if len(image_bytes) < 1000:
        raise Exception("Empty or invalid image received")

    # =========================
    # SAVE IMAGE (STABLE)
    # =========================
    os.makedirs("content/images", exist_ok=True)

    filename = f"fashion_{int(time.time())}.jpg"
    path = f"content/images/{filename}"

    with open(path, "wb") as f:
        f.write(image_bytes)

    print("Image saved:", path)

    return path

# =========================
# RUN
# =========================
if __name__ == "__main__":
    generate_image(prompt)
