import json
import os
from fastapi import FastAPI
from pydantic import BaseModel
from dotenv import load_dotenv
from openai import OpenAI
from pathlib import Path




load_dotenv(override=True)

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

app = FastAPI()

class ChatRequest(BaseModel):
    message: str



#Reading JSON file-------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent
PROFILE_PATH = BASE_DIR / "data" / "profile.json"


def load_profile():
    with open(PROFILE_PATH, "r", encoding="utf-8") as file:
        return json.load(file)

#-------------------------------------

#Readin json file test-----------------------------
@app.get("/test-json")
def test_json():
    try:
        profile = load_profile()

        return {
            "status": "OK",
            "profile_path": str(PROFILE_PATH),
            "profile": profile
        }

    except Exception as e:
        return {
            "status": "ERROR",
            "profile_path": str(PROFILE_PATH),
            "error": str(e)
        }

#-------------------------------------

@app.get("/")
def root():
    return {"message":"AI CV Assistant backend Running"}


@app.post("/chat")
def chat(request: ChatRequest):
    try:
        profile = load_profile()

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": f"""
Du er en AI-assistent for Abdel Sadaqi.
Du skal kun svare basert på informasjonen under.
Hvis spørsmålet ikke handler om Abdel, svar:
"Jeg kan bare svare på spørsmål om Abdel Sadaqi."

Informasjon om Abdel:
{json.dumps(profile, ensure_ascii=False, indent=2)}
"""
                },
                {
                    "role": "user",
                    "content": request.message
                }
            ]
        )

        return {"answer": response.choices[0].message.content}

    except Exception as e:
        return {"error": str(e)}

    print("ROUTES:")
for route in app.routes:
    print(route.path)



