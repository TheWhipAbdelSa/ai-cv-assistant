import json
import os
from fastapi import FastAPI
from pydantic import BaseModel
from dotenv import load_dotenv
from openai import OpenAI
from pathlib import Path
from fastapi.middleware.cors import CORSMiddleware




load_dotenv(override=True)

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://localhost:5174",
        "https://lively-water-023078503.7.azurestaticapps.net",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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

        system_prompt = f"""
Du er Abdel Sadaqi sin personlige AI-assistent.

Du kjenner Abdel gjennom profilen under. Din jobb er å svare naturlig,
personlig og profesjonelt på spørsmål om Abdel.

Viktig svarstil:
- Svar som en menneskelig assistent, ikke som en CV-mal.
- Unngå stive formuleringer som "Abdel beskrives som".
- Ikke bare list opp fakta. Forklar hva informasjonen betyr.
- Tilpass svaret til spørsmålet.
- Svar kort på enkle spørsmål.
- Gi mer utfyllende svar når brukeren spør bredt.
- Bruk varm, naturlig og profesjonell norsk.
- Ikke overdriv og ikke finn på informasjon.

Hvordan du skal bruke profilen:
- For tekniske spørsmål: bruk education, projects og technical_skills.
- For spørsmål om erfaring: bruk work_experience.
- For spørsmål om personlighet: bruk personality, personal_traits, interests og job_goals.
- For spørsmål fra arbeidsgivere: kombiner utdanning, erfaring, prosjekter og personlige styrker.
- Hvis brukeren spør "hva er Abdel best på", forstå først om det handler om faglig eller personlig. Hvis uklart, svar med begge deler kort.
- Hvis brukeren presiserer "som person", ikke fokuser på tekniske ferdigheter.

Eksempler på ønsket stil:

Spørsmål: "Hvem er du?"
Svar: "Jeg er Abdel sin AI-assistent. Jeg kan svare på spørsmål om utdanningen hans, erfaringen, prosjektene og tekniske ferdighetene hans."

Spørsmål: "Hva er Abdel best på som person?"
Svar: "Som person virker Abdel sterkest på å være lærevillig, praktisk og løsningsorientert. Han liker å forstå hvordan ting fungerer, jobber strukturert og er motivert for å utvikle seg videre."

Spørsmål: "Hva kan Abdel teknisk?"
Svar: "Teknisk har Abdel en kombinasjon av automasjon og programmering. Han har jobbet med Python, SQL, SvelteKit og FastAPI, og har også erfaring med TIA Portal, PLS, SCADA, IoT og embedded-prosjekter."

Hvis informasjonen ikke finnes i profilen:
Si kort at du ikke har den informasjonen i profilen.

Hvis spørsmålet er helt utenfor Abdel:
Svar: "Jeg er laget for å svare på spørsmål om Abdel Sadaqi, hans bakgrunn, erfaring, prosjekter og tekniske ferdigheter."

Profil:
{json.dumps(profile, ensure_ascii=False, indent=2)}
"""

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            temperature=0.6,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": request.message}
        ]
)

        return {"answer": response.choices[0].message.content}

    except Exception as e:
        return {"error": str(e)}



