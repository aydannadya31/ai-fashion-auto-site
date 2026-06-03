import requests
import base64
import os
import time
import json
import random

CF_API_TOKEN = os.environ.get('CF_API_TOKEN', '')
CF_ACCOUNT_ID = os.environ.get('CF_ACCOUNT_ID', '')
HF_TOKEN = os.environ.get('HF_TOKEN', '')

BASE_URL = "https://raw.githubusercontent.com/aydannadya31/ai-fashion-auto-site/main/"

PROMPT = (
    "hyper realistic fashion model, editorial face, soft skin texture, "
    "high fashion futuristic outfit, glossy fabric, runway style, "
    "dark studio, cinematic lighting, soft fog, reflective floor, "
    "luxury fashion photography studio setup, "
    "8K RAW, DSLR, 85mm lens, f/1.4, ISO 100, "
    "ultra realistic fashion photography, cinematic lighting, high detail"
)

NEGATIVE = "low quality, blurry, cartoon, anime, watermark, text"

CF_BASE = f"https://api.cloudflare.com/client/v4/accounts/{CF_ACCOUNT_ID}/ai/run"

MODELS = []

if CF_API_TOKEN and CF_ACCOUNT_ID:
    MODELS += [
        {"id": "@cf/black-forest-labs/flux-2-dev",           "platform": "CF",  "type": "flux"},
        {"id": "@cf/black-forest-labs/flux-2-klein-9b",      "platform": "CF",  "type": "flux"},
        {"id": "@cf/black-forest-labs/flux-2-klein-4b",      "platform": "CF",  "type": "flux"},
        {"id": "@cf/black-forest-labs/flux-1-dev",           "platform": "CF",  "type": "flux"},
        {"id": "@cf/black-forest-labs/flux-1-schnell",       "platform": "CF",  "type": "flux"},
        {"id": "@cf/stabilityai/stable-diffusion-xl-base-1.0", "platform": "CF", "type": "sdxl"},
        {"id": "@cf/lykon/dreamshaper-8-lcm",                "platform": "CF",  "type": "sdxl"},
    ]

if HF_TOKEN:
    MODELS += [
        {"id": "black-forest-labs/FLUX.1-dev",                "platform": "HF",  "type": "hf"},
        {"id": "black-forest-labs/FLUX.1-schnell",            "platform": "HF",  "type": "hf"},
        {"id": "black-forest-labs/FLUX.1-Krea-dev",           "platform": "HF",  "type": "hf"},
        {"id": "stabilityai/stable-diffusion-3.5-large",      "platform": "HF",  "type": "hf"},
        {"id": "stabilityai/stable-diffusion-xl-base-1.0",    "platform": "HF",  "type": "hf"},
        {"id": "ByteDance/Hyper-SD",                          "platform": "HF",  "type": "hf"},
    ]

def save_image(data, filename):
    os.makedirs("content/images", exist_ok=True)
    path = f"content/images/{filename}"
    with open(path, "wb") as f:
        f.write(data)
    return BASE_URL + path


def try_cf_model(model, i):
    url = f"{CF_BASE}/{model['id']}"
    headers = {"Authorization": f"Bearer {CF_API_TOKEN}"}

    if model["type"] == "flux":
        import io
        boundary = "----WebKitFormBoundary" + str(random.randint(100000, 999999))
        body = (
            f"--{boundary}\r\n"
            f'Content-Disposition: form-data; name="prompt"\r\n\r\n'
            f"{PROMPT}\r\n"
            f"--{boundary}\r\n"
            f'Content-Disposition: form-data; name="guidance"\r\n\r\n'
            f"7.0\r\n"
            f"--{boundary}--\r\n"
        )
        headers["Content-Type"] = f"multipart/form-data; boundary={boundary}"
        res = requests.post(url, headers=headers, data=body.encode(), timeout=120)
    else:
        payload = {"prompt": PROMPT, "negative_prompt": NEGATIVE, "num_steps": 25}
        res = requests.post(url, headers=headers, json=payload, timeout=120)

    print(f"  {model['id']}: HTTP {res.status_code}", end="")
    if res.status_code != 200:
        print(f" {res.text[:100]}")
        return None

    ct = res.headers.get("Content-Type", "")
    if "image" in ct:
        img_data = res.content
    else:
        data = res.json()
        if model["type"] == "flux":
            try:
                img_data = data.get("result", {}).get("image")
                if img_data:
                    img_data = base64.b64decode(img_data)
                else:
                    print(" no image key")
                    return None
            except Exception:
                print(" parse error")
                return None
        else:
            try:
                raw = data["result"]["image"]
                if isinstance(raw, dict):
                    raw = raw.get("image") or raw.get("response")
                if isinstance(raw, list):
                    raw = raw[0]
                img_data = base64.b64decode(raw)
            except Exception:
                try:
                    raw = data["result"]["response"]
                    img_data = base64.b64decode(raw)
                except Exception:
                    print(" unexpected format")
                    return None

    ts = int(time.time())
    fname = f"fashion_{ts}_{i}.jpg"
    url = save_image(img_data, fname)
    print(f" OK -> {fname}")
    return url


def try_hf_model(model, i):
    url = f"https://api-inference.huggingface.co/models/{model['id']}"
    headers = {"Authorization": f"Bearer {HF_TOKEN}"}
    payload = {
        "inputs": PROMPT,
        "parameters": {
            "negative_prompt": NEGATIVE,
            "num_inference_steps": 25
        }
    }

    res = requests.post(url, headers=headers, json=payload, timeout=180)
    print(f"  {model['id']}: HTTP {res.status_code}", end="")

    if res.status_code != 200:
        try:
            err = res.json()
            print(f" {err.get('error', str(err)[:100])}")
        except Exception:
            print(f" {res.text[:100]}")
        return None

    ct = res.headers.get("Content-Type", "")
    if "image" in ct:
        img_data = res.content
    else:
        data = res.json()
        if isinstance(data, list) and len(data) > 0:
            item = data[0]
            if isinstance(item, dict) and "image" in item.get("content-type", ""):
                b64 = item.get("image", item.get("encoded", ""))
                if b64:
                    img_data = base64.b64decode(b64)
                else:
                    print(" no base64")
                    return None
            elif isinstance(item, bytes):
                img_data = item
            else:
                print(f" unexpected: {str(item)[:100]}")
                return None
        elif isinstance(data, dict) and "image" in data:
            img_data = base64.b64decode(data["image"])
        else:
            print(f" unknown: {str(data)[:100]}")
            return None

    ts = int(time.time())
    fname = f"fashion_{ts}_{i}.jpg"
    url = save_image(img_data, fname)
    print(f" OK -> {fname}")
    return url


def main():
    print(f"=== AI Fashion Multi-Model Generator ===")
    print(f"Total models: {len(MODELS)}")
    print()

    if not MODELS:
        print("No API tokens configured — exiting")
        return

    results = []

    for idx, m in enumerate(MODELS):
        try:
            if m["platform"] == "CF":
                url = try_cf_model(m, idx)
            else:
                url = try_hf_model(m, idx)

            if url:
                results.append({"url": url, "model": m["id"]})
                print()
        except Exception as e:
            print(f"  {m['id']}: EXCEPTION {e}")
            print()

    print(f"\n=== Results: {len(results)}/{len(MODELS)} models succeeded ===")

    if not results:
        print("No images generated — keeping existing post.json")
        return

    post = {
        "prompt": PROMPT,
        "images": results,
        "caption": f"AI Fashion Multi-Model — {len(results)} models",
        "count": len(results),
        "timestamp": int(time.time())
    }

    with open("content/post.json", "w", encoding="utf-8") as f:
        json.dump(post, f, indent=2, ensure_ascii=False)

    print(f"Saved {len(results)} images to post.json")


if __name__ == "__main__":
    main()
