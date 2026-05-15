def generate_image(prompt):
    url = f"https://api.cloudflare.com/client/v4/accounts/{CF_ACCOUNT_ID}/ai/run/@cf/black-forest-labs/flux-1-schnell"

    headers = {
        "Authorization": f"Bearer {CF_API_TOKEN}",
        "Content-Type": "application/json"
    }

    payload = {"prompt": prompt}

    response = requests.post(url, headers=headers, json=payload)

    print("STATUS:", response.status_code)
    print("RAW:", response.text[:500])

    if response.status_code != 200:
        raise Exception(f"HTTP ERROR: {response.text}")

    result = response.json()

    if not result.get("success"):
        raise Exception(result)

    image_base64 = result["result"]["image"]
    image_bytes = base64.b64decode(image_base64)

    os.makedirs("images", exist_ok=True)
    path = "images/output.png"

    with open(path, "wb") as f:
        f.write(image_bytes)

    print("Image saved:", path)
    return path
