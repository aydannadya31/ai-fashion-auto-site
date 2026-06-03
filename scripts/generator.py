import requests
import base64
import os
import time
import json
import random

CF_API_TOKEN = os.environ.get('CF_API_TOKEN', '')
CF_ACCOUNT_ID = os.environ.get('CF_ACCOUNT_ID', '')

BASE_URL = "https://raw.githubusercontent.com/aydannadya31/ai-fashion-auto-site/main/"
API_URL = f"https://api.cloudflare.com/client/v4/accounts/{CF_ACCOUNT_ID}/ai/run/@cf/stabilityai/stable-diffusion-xl-base-1.0"
HEADERS = {"Authorization": f"Bearer {CF_API_TOKEN}"}

BASE_PROMPT = ""

def load_base_prompt():
    global BASE_PROMPT
    base = {}
    rules = {}

    if os.path.exists('data.json'):
        base = json.load(open('data.json'))
    if os.path.exists('content/rules.json'):
        rules = json.load(open('content/rules.json'))

    parts = []

    rp = rules.get('imagePromptRules', {})

    parts.append("FASHION PHOTOGRAPHY PROMPT")

    directives = rp.get('base_directives', [])
    if directives:
        parts.append("Directives: " + "; ".join(directives))

    if base.get('model'):
        parts.append("Model: " + base['model'])
    sb = rp.get('structure_blocks', {})
    for k, v in sb.items():
        parts.append(f"{k}: {v}")

    if base.get('clothing'):
        parts.append("Clothing: " + base['clothing'])
    gr = rules.get('garmentRules', {})
    if gr.get('silhouette'):
        parts.append("Silhouette: " + random.choice(gr['silhouette']))
    if gr.get('materials'):
        parts.append("Material: " + random.choice(gr['materials']))
    if gr.get('construction'):
        parts.append("Construction: " + random.choice(gr['construction']))

    if base.get('scene'):
        parts.append("Scene: " + base['scene'])
    de = rp.get('dynamic_elements', {})
    if de.get('environments'):
        parts.append("Environment: " + random.choice(de['environments']))
    if de.get('lighting'):
        parts.append("Lighting: " + random.choice(de['lighting']))

    if base.get('technical'):
        parts.append("Technical: " + base['technical'])
    if rp.get('technical_tags'):
        parts.append("Technical: " + rp['technical_tags'])

    if base.get('negative'):
        parts.append("Negative: " + base['negative'])

    qr = rp.get('quality_rule', '')
    if qr:
        parts.append("Quality: " + qr)

    BASE_PROMPT = ". ".join(parts)


def generate(i):
    payload = {
        "prompt": BASE_PROMPT,
        "negative_prompt": "low quality, blurry, cartoon, anime, watermark, text",
        "num_steps": 30
    }

    res = requests.post(API_URL, headers=HEADERS, json=payload, timeout=120)
    print("STATUS:", res.status_code)

    result = res.json()
    print("RAW RESULT KEYS:", list(result.keys()) if isinstance(result, dict) else "not dict")

    img_b64 = None

    try:
        img_b64 = result["result"]["image"]
    except Exception:
        try:
            img_b64 = result["result"]["response"]
        except Exception:
            try:
                img_b64 = result["result"]
            except Exception:
                raise Exception("Image format unknown from API response")

    if isinstance(img_b64, dict):
        img_b64 = img_b64.get("image") or img_b64.get("response")

    if isinstance(img_b64, list):
        img_b64 = img_b64[0]

    if not img_b64 or not isinstance(img_b64, str):
        raise Exception(f"Unexpected image data format: {type(img_b64)}")

    img = base64.b64decode(img_b64)

    os.makedirs("content/images", exist_ok=True)

    filename = f"fashion_{int(time.time())}_{i}.jpg"
    local_path = f"content/images/{filename}"

    with open(local_path, "wb") as f:
        f.write(img)

    public_url = BASE_URL + local_path
    print("Saved:", public_url)

    return public_url


def main():
    load_base_prompt()
    print("PROMPT:", BASE_PROMPT[:200] + "...")

    if not CF_API_TOKEN or not CF_ACCOUNT_ID:
        print("CF_API_TOKEN or CF_ACCOUNT_ID not set, skipping generation")
        return

    images = []
    for i in range(4):
        try:
            url = generate(i)
            images.append(url)
        except Exception as e:
            print(f"Image {i} failed:", e)

    if not images:
        print("No images generated, keeping existing post.json")
        return

    post = {
        "style": "luxury high-end studio shoot",
        "prompt": BASE_PROMPT,
        "images": images,
        "caption": "AI Fashion Drop — luxury high-end studio shoot",
        "timestamp": int(time.time())
    }

    with open("content/post.json", "w", encoding="utf-8") as f:
        json.dump(post, f, indent=2, ensure_ascii=False)

    print("Done. Generated", len(images), "images")


if __name__ == "__main__":
    main()
