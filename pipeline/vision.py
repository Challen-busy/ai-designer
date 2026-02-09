import base64
import os
import httpx

DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")
BASE_URL = "https://api.deepseek.com"

def encode_image(path: str) -> str:
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")

def extract_keywords(image_path: str) -> str:
    if not DEEPSEEK_API_KEY:
        raise RuntimeError("DEEPSEEK_API_KEY not set")

    b64 = encode_image(image_path)

    payload = {
        "model": "deepseek-chat",
        "messages": [
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": "Extract 8 concise visual keywords from this image."},
                    {
                        "type": "image_url",
                        "image_url": {"url": f"data:image/jpeg;base64,{b64}"}
                    }
                ]
            }
        ],
        "max_tokens": 100
    }

    headers = {
        "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
        "Content-Type": "application/json"
    }

    with httpx.Client(timeout=60) as client:
        r = client.post(f"{BASE_URL}/chat/completions", json=payload, headers=headers)
        r.raise_for_status()
        data = r.json()

    return data["choices"][0]["message"]["content"].strip()

# —— 自测入口 ——
if __name__ == "__main__":
    print("Running vision self-test...")
    print(extract_keywords("test.jpg"))
