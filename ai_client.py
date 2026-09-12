import os
import requests

BASE_URL = "https://copa.codyssey.kr/v1/messages"

def generate_text(prompt, system_prompt="", model="claude-sonnet-4", max_tokens=1024, temperature=0.7):
    api_key = os.environ.get("AI_API_KEY")

    if not api_key:
        print("[ERROR] AI_API_KEY 환경변수가 설정되지 않았습니다.")
        return None

    response = requests.post(
        BASE_URL,
        headers={
            "x-api-key": api_key,
            "anthropic-version": "2023-06-01",
        },
        json={
            "model": model,
            "max_tokens": max_tokens,
            "temperature": temperature,
            "system": system_prompt,
            "messages": [{"role": "user", "content": prompt}],
        },
    )

    return response.json()["content"][0]["text"]
