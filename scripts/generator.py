import json
import random
import time
import os

DATA_FILE = "data.json"

ENVIRONMENTS = [
    "brutalist concrete studio",
    "liquid metal reflective floor",
    "black void reflection room",
    "minimalist luxury fashion studio"
]

LIGHTING = [
    "cinematic rim lighting",
    "high contrast editorial lighting",
    "Blade Runner neon reflections",
    "soft volumetric studio fog lighting"
]

FABRICS = [
    "ultra glossy latex",
    "micro-rib technical silk",
    "transparent engineered mesh",
    "liquid metal fabric",
    "recycled ocean polymer textile"
]

NEGATIVE = "anime, illustration, drawing, male, child, watermark, logo, text"


def generate_prompt():
    env = random.choice(ENVIRONMENTS)
    light = random.choice(LIGHTING)
    fabric = random.choice(FABRICS)

    return f"""
[MODEL ÖZELLİKLERİ]
hyper realistic female fashion model,
natural skin micro texture,
editorial gaze, modern hairstyle

[GİYİM ÖZELLİKLERİ]
tight short bodycon dress made from {fabric},
laser cut edges,
architectural silhouette,
precision structural seams

[EDİTÖRYAL ORTAM]
{env},
{light},
studio flashes,
volumetric fog

[TEKNİK ETİKETLER]
8K RAW fashion photography,
Phase One XF,
80mm lens,
f/1.4,
ISO 100

The models' faces must not change or become distorted.
No anatomical distortion allowed.

NEGATIVE PROMPT:
{NEGATIVE}
"""


def generate_seo():
    number = random.randint(1000, 9999)
    title = f"Luxury AI Fashion Look {number}"

    return {
        "seo_title": title,
        "slug": title.lower().replace(" ", "-"),
        "category": "AI Fashion Editorial",
        "pinterest_title": title + " | High Fashion AI Style",
        "hashtags": [
            "#aifashion",
            "#luxurystyle",
            "#fashioneditorial",
            "#runwaystyle",
            "#digitalfashion"
        ]
    }


def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return []


def save_data(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def main():
    data = load_data()

    entry = {
        "id": int(time.time()),
        "prompt": generate_prompt(),
        **generate_seo()
    }

    data.insert(0, entry)
    save_data(data)

    print("New fashion entry generated")


if __name__ == "__main__":
    main()
