import os
import json
import requests
import base64
import time
import random

# =========================
# API CONFIG
# =========================
CF_API_TOKEN = os.environ["CF_API_TOKEN"]
CF_ACCOUNT_ID = os.environ["CF_ACCOUNT_ID"]

url = f"https://api.cloudflare.com/client/v4/accounts/{CF_ACCOUNT_ID}/ai/run/@cf/black-forest-labs/flux-1-schnell"

headers = {
    "Authorization": f"Bearer {CF_API_TOKEN}",
    "Content-Type": "application/json"
}

# =========================
# LOAD BASE DATA
# =========================
with open("data.json", "r", encoding="utf-8") as f:
    data = json.load(f)

if isinstance(data, list):
    data = data[0]

# =========================
# LOAD RULE ENGINE (NEW)
# =========================
rules = None
if os.path.exists("content/rules.json"):
    with open("content/rules.json", "r", encoding="utf-8") as f:
        rules = json.load(f)

# fallback rules
if not rules:
    rules = {
        "imagePromptRules": {
            "structure_blocks": {
                "MODEL_FEATURES": "facial structure, skin micro-texture, editorial gaze, hairstyle, pose",
                "CLOTHING_FEATURES": "high fashion bodycon outfit, precise tailoring, fabric tension",
                "EDITORIAL_ENVIRONMENT": "studio lighting, cinematic shadows",
                "TECHNICAL_TAGS": "8K RAW, Phase One XF, 80mm lens, f/1.4, ISO 100"
            },
            "quality_rule": "No facial distortion allowed",
            "dynamic_elements": {
                "environments": ["black studio", "liquid metal room", "fog runway"],
                "lighting": ["cinematic lighting", "neon rim light", "soft studio light"],
                "materials": ["latex", "silk", "mesh"]
            }
        },
        "garmentRules": {
            "style_language": "luxury fashion editorial"
        }
    }

# =========================
# STYLE VARIANTS
# =========================
styles = [
    "editorial runway fashion",
    "luxury fashion studio shoot",
    "cinematic fashion portrait",
    "avant-garde fashion magazine cover"
]

style = random.choice(styles)

# =========================
# PROMPT ENGINE (NEW SYSTEM)
# =========================
def build_prompt(rules):
    env = random.choice(rules["imagePromptRules"]["dynamic_elements"]["environments"])
    light = random.choice(rules["imagePromptRules"]["dynamic_elements"]["lighting"])
    mat = random.choice(rules["imagePromptRules"]["dynamic_elements"]["materials"])

    blocks = rules["imagePromptRules"]["structure_blocks"]

    prompt = f"""
MODEL FEATURES:
{blocks['MODEL_FEATURES']}

CLOTHING FEATURES:
{blocks['CLOTHING_FEATURES']} (material: {mat})

EDITORIAL ENVIRONMENT:
{env}, {light}

TECHNICAL TAGS:
{blocks['TECHNICAL_TAGS']}

QUALITY RULE:
{rules['imagePromptRules']['quality_rule']}

STYLE:
{rules['garmentRules']['style_language']}

ADDITIONAL STYLE:
{style}
"""

    return prompt

base_prompt = build_prompt(rules)

print("Prompt created")
print(base_prompt)

# =========================
# IMAGE BASE URL
# =========================
BASE_URL = "https://raw.githubusercontent.com/aydannadya31/ai-fashion-auto-site/main/"

# =========================
# GENERATE IMAGE
# =========================
def generate(i):
    res = requests.post(url, headers=headers, json={"prompt": base_prompt})

    print("STATUS:", res.status_code)

    result = res.json()

    img = base64.b64decode(result["result"]["image"])

    os.makedirs("content/images", exist_ok=True)

    filename = f"fashion_{int(time.time())}_{i}.jpg"
    local_path = f"content/images/{filename}"

    with open(local_path, "wb") as f:
        f.write(img)

    # PUBLIC URL FIX
    public_url = BASE_URL + local_path

    print("Saved:", public_url)

    return public_url

# =========================
# RUN MULTI IMAGE
# =========================
paths = []

for i in range(4):
    paths.append(generate(i))
    time.sleep(1)

# =========================
# POST JSON FEED
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

print("POST READY ✔ SYSTEM RUNNING")
