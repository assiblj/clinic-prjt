# core/ai_assistant.py
import json
import urllib.request
import urllib.error


def ask_gemini(messages, system_prompt=""):
    api_key = "AIzaSyBDhR5tccIhWuNGfFVOl-7KXCj_i9Uh_rE"

    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={api_key}"

    headers = {
        "Content-Type": "application/json"
    }

    body = json.dumps({
    "systemInstruction": {
        "parts": [
            {
                "text": system_prompt
            }
        ]
    },
    "contents": [
        {
            "parts": [
                {
                    "text": messages[-1]["content"]
                }
            ]
        }
    ]
}).encode("utf-8")

    req = urllib.request.Request(url, data=body, headers=headers, method="POST")

    try:
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read().decode("utf-8"))
            return data["candidates"][0]["content"]["parts"][0]["text"]

    except urllib.error.HTTPError as e:
        return f"Erreur API: {e.code} — {e.read().decode()}"

    except Exception as e:
        return f"Erreur: {str(e)}"