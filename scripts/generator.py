import random, time, json, urllib.parse, os

timestamp = int(time.time())

# ---------- MODEL BLOĞU ----------
models = [
"full body female fashion model, sharp jawline, porcelain skin texture, intense editorial gaze, sleek wet hair",
"full body female couture model, symmetrical face, flawless skin microtexture, confident runway pose",
]

# ---------- KUMAŞ ----------
fabrics = [
"liquid metal fabric reflecting sharp studio highlights",
"micro ribbed technical silk with specular reflections",
"transparent technical mesh with layered tension",
]

# ---------- ORTAM ----------
environments = [
"brutalist concrete studio with volumetric fog",
"black reflective void chamber",
"liquid chrome editorial environment",
]

# ---------- IŞIK ----------
lighting = [
"cinematic rim lighting, high contrast minimal shadows",
"blade runner neon reflections with controlled shadow gradients",
"editorial studio flash system with volumetric diffusion",
]

model = random.choice(models)
fabric = random.choice(fabrics)
environment = random.choice(environments)
light = random.choice(lighting)

imagePrompt = f"""
[MODEL FEATURES]: {model}
[CLOTHING FEATURES]: bodycon architectural dress, laser cut edges, reinforced seams, anatomical precision interacting with body structure, {fabric}
[EDITORIAL ENVIRONMENT]: {environment}, {light}
[TECHNICAL TAGS]: Phase One XF, 80mm lens, f/1.4, ISO 100, 8K RAW fashion photography

The models' faces must not change or become distorted; their facial features must be preserved from every shooting angle. There must be no anatomical distortion.
"""

displayDescription = "A high-fashion editorial piece exploring material precision, architectural silhouette, and modern couture aesthetics."

slug = f"ai-fashion-look-{timestamp}"

seo = {
"title": "AI High Fashion Editorial Look",
"slug": slug,
"category": "AI Fashion",
"pinterest": "High Fashion AI Editorial Outfit Inspiration",
"hashtags": "#AIFashion #HighFashion #EditorialFashion #FashionDesign"
}

data = {
"title": seo["title"],
"prompt": imagePrompt,
"description": displayDescription,
"seo": seo
}

os.makedirs("content/images", exist_ok=True)

safe_prompt = urllib.parse.quote(imagePrompt)

image_url = f"https://image.pollinations.ai/prompt/{safe_prompt}"
file = f"content/images/{slug}.jpg"

os.system(f'curl -L "{image_url}" -o "{file}"')

data["image"] = file
data["date"] = time.ctime()

with open("data.json","w") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)
f.write("\n")
