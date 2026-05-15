import os
import json
import time
import base64
from openai import OpenAI

# ===============================
# OPENAI CLIENT
# ===============================

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)

# ===============================
# LOAD DATA.JSON
# ===============================

with open("data.json", "r", encoding="utf-8") as f:
    data = json.load(f)

model_features = data["model"]
clothing_features = data["clothing"]
environment_features = data["environment"]
technical_tags = data["technical"]

# ===============================
# BUILD PROMPT
# ===============================

timestamp = int(time.time())
title = f"Luxury AI Fashion Look {timestamp}"

prompt = f"""
[MODEL FEATURES]
{model_features}

[CLOTHING FEATURES]
{clothing_features}

[EDITORIAL ENVIRONMENT]
{environment_features}

[TECHNICAL TAGS]
{technical_tags}

The models' faces must not change or become distorted.
No anatomical distortion allowed.

NEGATIVE PROMPT:
anime, illustration, drawing, male, child, watermark, logo, text
"""

print("Prompt created.")

# ===============================
# GENERATE IMAGE
# ===============================

print("Generating AI image...")

result = client.images.generate(
    model="gpt-image-1",
    prompt=prompt,
    size="1024x1024"
)

image_base64 = result.data[0].b64_json
image_bytes = base64.b64decode(image_base64)

image_name = f"fashion_{timestamp}.png"
image_path = f"images/{image_name}"

os.makedirs("images", exist_ok=True)

with open(image_path, "wb") as img:
    img.write(image_bytes)

print("Image saved:", image_path)

# ===============================
# CREATE CONTENT POST
# ===============================

os.makedirs("content", exist_ok=True)

post_path = f"content/post-{timestamp}.md"

with open(post_path, "w", encoding="utf-8") as f:
    f.write(f"# {title}\n\n")
    f.write(f"![AI Fashion](/images/{image_name})\n\n")
    f.write(prompt)

print("Post created:", post_path)
