def generate(i):
    res = requests.post(url, headers=headers, json={"prompt": base_prompt})

    print("STATUS:", res.status_code)

    result = res.json()

    # 🔥 DEBUG PRINT (önemli)
    print("RAW RESULT:", result)

    img_b64 = None

    # =========================
    # SAFE PARSING (FIX)
    # =========================

    try:
        img_b64 = result["result"]["image"]
    except:
        try:
            img_b64 = result["result"]["response"]
        except:
            try:
                img_b64 = result["result"]
            except:
                raise Exception("Image format unknown from API response")

    # Eğer dict gelirse
    if isinstance(img_b64, dict):
        img_b64 = img_b64.get("image") or img_b64.get("response")

    img = base64.b64decode(img_b64)

    os.makedirs("content/images", exist_ok=True)

    filename = f"fashion_{int(time.time())}_{i}.jpg"
    local_path = f"content/images/{filename}"

    with open(local_path, "wb") as f:
        f.write(img)

    public_url = BASE_URL + local_path

    print("Saved:", public_url)

    return public_url
