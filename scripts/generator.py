import requests
import base64
import os
import time
import json

HF_TOKEN = os.environ.get('HF_TOKEN', '')
MODEL = "stabilityai/stable-diffusion-xl-base-1.0"
API_URL = f"https://api-inference.huggingface.co/models/{MODEL}"
HEADERS = {"Authorization": f"Bearer {HF_TOKEN}"}

BASE_URL = "https://raw.githubusercontent.com/aydannadya31/ai-fashion-auto-site/main/"

PROMPT = (
    "hyper realistic fashion model, editorial face, soft skin texture, "
    "high fashion futuristic outfit, glossy fabric, runway style, "
    "dark studio, cinematic lighting, soft fog, reflective floor, "
    "luxury fashion photography studio setup, "
    "8K RAW, DSLR, 85mm lens, f/1.4, ISO 100, "
    "ultra realistic fashion photography, cinematic lighting, high detail"
)

CAPTION = "AI Fashion Drop \u2014 luxury high-end studio shoot"


def generate_one(i):
    payload = {
        "inputs": PROMPT,
        "parameters": {
            "negative_prompt": "low quality, blurry, cartoon, anime, watermark, text",
            "num_inference_steps": 30
        }
    }

    res = requests.post(API_URL, headers=HEADERS, json=payload, timeout=180)
    print(f"  Image {i}: status {res.status_code}")

    content_type = res.headers.get("Content-Type", "")

    if "image" in content_type:
        img = res.content
    else:
        result = res.json()
        if isinstance(result, list) and len(result) > 0:
            item = result[0]
            if isinstance(item, dict) and "image" in item.get("content-type", ""):
                img = base64.b64decode(item.get("image", item.get("encoded", "")))
            else:
                print(f"  Unexpected response: {str(result)[:200]}")
                return None
        elif isinstance(result, dict) and "error" in result:
            print(f"  API error: {result['error']}")
            return None
        else:
            print(f"  Unknown response format: {str(result)[:200]}")
            return None

    os.makedirs("content/images", exist_ok=True)
    filename = f"fashion_{int(time.time())}_{i}.jpg"

    with open(f"content/images/{filename}", "wb") as f:
        f.write(img)

    url = BASE_URL + "content/images/" + filename
    print(f"  Saved: {url}")
    return url


def main():
    print("=== AI Fashion Generator (Hugging Face) ===")

    if not HF_TOKEN:
        print("HF_TOKEN not set — exiting without changes")
        return

    images = []
    for i in range(4):
        try:
            url = generate_one(i)
            if url:
                images.append(url)
            else:
                print(f"  Image {i} returned no URL")
        except Exception as e:
            print(f"  Image {i} failed: {e}")

    if len(images) < 4:
        print(f"Only got {len(images)}/4 images — aborting to avoid duplicates")
        return

    post = {
        "style": "luxury high-end studio shoot",
        "prompt": PROMPT,
        "images": images,
        "caption": CAPTION,
        "timestamp": int(time.time())
    }

    with open("content/post.json", "w", encoding="utf-8") as f:
        json.dump(post, f, indent=2, ensure_ascii=False)

    print(f"Done — {len(images)} new images saved to post.json")


if __name__ == "__main__":
    main()
