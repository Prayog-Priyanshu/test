from fastapi import FastAPI, File, UploadFile, Form
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import base64
import requests

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_methods=["*"],
    allow_headers=["*"],
)

API_KEY = "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"
API_URL = "https://openrouter.ai/api/v1/chat/completions"
MODEL = "google/gemini-2.0-flash-exp:free"

lang_prompts = {
    "Hindi": "Translate the following medical info to Hindi:",
    "Tamil": "Translate the following medical info to Tamil:",
    "Telugu": "Translate the following medical info to Telugu:"
}

@app.post("/analyze-image/")
async def analyze_image(file: UploadFile = File(...)):
    try:
        img_bytes = await file.read()
        img_base64 = base64.b64encode(img_bytes).decode("utf-8")

        data = {
            "model": MODEL,
            "messages": [
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": "You are a medical expert. You are given a medicine name and you have to suggest a generic medicine of the same medicine. Generate a list of 3 to 5 generic medicines which is same/similar to original medicine with its recent price:"},
                        {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{img_base64}"}}
                    ]
                }
            ]
        }

        headers = {
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json"
        }

        response = requests.post(API_URL, headers=headers, json=data)
        result = response.json()

        reply = result['choices'][0]['message']['content']
        return {"reply": reply}

    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

@app.post("/translate/")
async def translate_response(original_text: str = Form(...), language: str = Form(...)):
    if language not in lang_prompts:
        return JSONResponse(status_code=400, content={"error": "Unsupported language"})

    prompt = f"{lang_prompts[language]}

{original_text}"

    data = {
        "model": MODEL,
        "messages": [
            {
                "role": "user",
                "content": [{"type": "text", "text": prompt}]
            }
        ]
    }

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    try:
        response = requests.post(API_URL, headers=headers, json=data)
        result = response.json()
        translated_text = result['choices'][0]['message']['content']
        return {"translated": translated_text}
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})