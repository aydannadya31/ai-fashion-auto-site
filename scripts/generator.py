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

EXISTING_IMAGES = [
    "https://raw.githubusercontent.com/aydannadya31/ai-fashion-auto-site/main/content/images/fashion_1778855211_0.jpg",
    "https://raw.githubusercontent.com/aydannadya31/ai-fashion-auto-site/main/content/images/fashion_1778855213_1.jpg",
    "https://raw.githubusercontent.com/aydannadya31/ai-fashion-auto-site/main/content/images/fashion_1778855216_2.jpg",
    "https://raw.githubusercontent.com/aydannadya31/ai-fashion-auto-site/main/content/images/fashion_1778855218_3.jpg",
    "https://raw.githubusercontent.com/aydannadya31/ai-fashion-auto-site/main/content/images/fashion_1778854616_0.jpg",
    "https://raw.githubusercontent.com/aydannadya31/ai-fashion-auto-site/main/content/images/fashion_1778854618_1.jpg",
    "https://raw.githubusercontent.com/aydannadya31/ai-fashion-auto-site/main/content/images/fashion_1778854621_2.jpg",
    "https://raw.githubusercontent.com/aydannadya31/ai-fashion-auto-site/main/content/images/fashion_1778854624_3.jpg",
    "https://raw.githubusercontent.com/aydannadya31/ai-fashion-auto-site/main/content/images/fashion_1778853260_0.jpg",
    "https://raw.githubusercontent.com/aydannadya31/ai-fashion-auto-site/main/content/images/fashion_1778853263_1.jpg",
    "https://raw.githubusercontent.com/aydannadya31/ai-fashion-auto-site/main/content/images/fashion_1778853265_2.jpg",
    "https://raw.githubusercontent.com/aydannadya31/ai-fashion-auto-site/main/content/images/fashion_1778853268_3.jpg",
    "https://raw.githubusercontent.com/aydannadya31/ai-fashion-auto-site/main/content/images/fashion_1778853043.jpg",
    "https://raw.githubusercontent.com/aydannadya31/ai-fashion-auto-site/main/content/images/fashion_1778844399.jpg",
]

PROMPT = (
    "hyper realistic fashion model, editorial face, soft skin texture, "
    "high fashion futuristic outfit, glossy fabric, runway style, "
    "dark studio, cinematic lighting, soft fog, reflective floor, "
    "luxury fashion photography studio setup, "
    "8K RAW, DSLR, 85mm lens, f/1.4, ISO 100, "
    "ultra realistic fashion photography, cinematic lighting, high detail"
)

CAPTION = "AI Fashion Drop — luxury high-end studio shoot"


def generate_from_api(i):
    payload = {
        "prompt": PROMPT,
        "negative_prompt": "low quality, blurry, cartoon, anime, watermark, text",
        "num_steps": 30
    }

    res = requests.post(API_URL, headers=HEADERS, json=payload, timeout=120)
    print(f"  Image {i}: status {res.status_code}")

    result = res.json()

    if not result.get("success"):
        print(f"  API error: {result}")
        return None

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
                pass

    if isinstance(img_b64, dict):
        img_b64 = img_b64.get("image") or img_b64.get("response")
    if isinstance(img_b64, list) and img_b64:
        img_b64 = img_b64[0]

    if not img_b64 or not isinstance(img_b64, str):
        print(f"  Unexpected image data: {type(img_b64)}")
        return None

    img = base64.b64decode(img_b64)
    os.makedirs("content/images", exist_ok=True)
    filename = f"fashion_{int(time.time())}_{i}.jpg"
    local_path = f"content/images/{filename}"

    with open(local_path, "wb") as f:
        f.write(img)

    url = BASE_URL + local_path
    print(f"  Saved: {url}")
    return url


def main():
    print("=== AI Fashion Generator ===")

    new_images = []

    if CF_API_TOKEN and CF_ACCOUNT_ID:
        print("Cloudflare API configured, attempting generation...")
        for i in range(4):
            try:
                url = generate_from_api(i)
                if url:
                    new_images.append(url)
            except Exception as e:
                print(f"  Image {i} failed: {e}")
    else:
        print("Cloudflare API not configured (missing CF_API_TOKEN or CF_ACCOUNT_ID)")

    if not new_images:
        print("Using existing images as fallback")
        new_images = random.sample(EXISTING_IMAGES, min(4, len(EXISTING_IMAGES)))

    post = {
        "style": "luxury high-end studio shoot",
        "prompt": PROMPT,
        "images": new_images,
        "caption": CAPTION,
        "timestamp": int(time.time())
    }

    with open("content/post.json", "w", encoding="utf-8") as f:
        json.dump(post, f, indent=2, ensure_ascii=False)

    print(f"Done — {len(new_images)} images in post.json")


if __name__ == "__main__":
    main()
