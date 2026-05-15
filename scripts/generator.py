import os
import json
import requests
import base64

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

# safety: list gelirse düzelt
if isinstance(data, list):
    data = data[0]

model = data.get("model", "")
clothing = data.get("clothing", "")
scene = data.get("scene", "")
environment = data.get("environment", "")
technical = data.get("technical", "")
negative = data.get("negative", "")

# =========================
# PROMPT BUILD
# =========================
prompt = f"""
{model},
{clothing},
{scene},
{environment},
{technical},
ultra realistic fashion photography, editorial style, cinematic lighting
"""

print("Prompt created.")
print(prompt)

# =========================
# CLOUDFARE IMAGE GENERATION
# =========================
def generate_image(prompt):
    url = f"https://api.cloudflare.com/client/v4/accounts/{CF_ACCOUNT_ID}/ai/run/@cf/stabilityai/stable-diffusion-xl-base-1.0"

    headers = {
        "Authorization": f"Bearer {CF_API_TOKEN}",
        "Content-Type": "application/json"
    }

    payload = {
        "prompt": prompt
    }

    response = requests.post(url, headers=headers, json=payload)
    result = response.json()

    if not result.get("success"):
        raise Exception(f"Cloudflare error: {result}")

    # Cloudflare SDXL base64 image döndürür
    image_base64 = result["result"]["image"]
    image_bytes = base64.b64decode(image_base64)

    # klasör oluştur
    os.makedirs("images", exist_ok=True)

    path = "images/output.png"

    with open(path, "wb") as f:
        f.write(image_bytes)

    print("Image saved:", path)
    return path

# =========================
# RUN
# =========================
if __name__ == "__main__":
    generate_image(prompt)
