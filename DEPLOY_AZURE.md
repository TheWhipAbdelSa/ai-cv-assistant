# Publisering til eksisterende Azure-oppsett

Prosjektet har to GitHub Actions som kjører ved push til `main`: frontend til Azure Static Web Apps og backend til App Service `abdel-ai-cv-assistant-api`. Ingen manuell opplasting av mapper er nødvendig.

## 1. Klargjør Azure før push

Åpne backendens App Service i Azure Portal → Settings → Environment variables → App settings. Sett følgende og lagre:

| Navn | Verdi |
| --- | --- |
| `ADMIN_TOKEN` | Tilfeldig hemmelig nøkkel på minst 32 tegn |
| `OPENAI_API_KEY` | Din eksisterende API-nøkkel |
| `CONTENT_DATA_DIR` | `/home/data/cv-assistant` |
| `SCM_DO_BUILD_DURING_DEPLOYMENT` | `true` |

Generer administratornøkkelen lokalt med `python -c "import secrets; print(secrets.token_urlsafe(32))"`. Oppbevar den i en passordbehandler. Ikke legg den i GitHub-koden eller frontendens miljøvariabler.

Backend skal bruke Linux / Python 3.12 og én instans. Workflowen setter oppstartskommando til `python -m uvicorn main:app --host 0.0.0.0 --port 8000`. Behold persistent App Service-lagring under `/home`. Oppsettet er beregnet på eksisterende Python App Service, ikke en egendefinert Docker-container.

Eksisterende Azure-pålogging og deployment secrets i GitHub må fortsatt være gyldige. Frontendens offentlige backendadresse er allerede satt i workflowen.

## 2. Kontroller og publiser fra VS Code

Kjør fra prosjektroten:

```powershell
.\backend\venv\Scripts\python.exe -m unittest backend.test_content
npm --prefix frontend run build
git status
git diff --check
```

I Source Control: se gjennom endringene, stage kildekode, dokumentasjon, `.env.example` og workflow-filer. Ikke stage `.env`, `backend/storage`, virtuelle miljøer, `node_modules` eller generert `build`. Disse er ignorert. Commit for eksempel med `Add admin panel and prepare Azure deployment`, og push til `main`. Push starter publiseringen til den eksisterende offentlige nettsiden.

Under GitHub → Actions må begge workflowene bli grønne. Backend kjører tester før deploy; frontend bygges med Node 24 før opplasting. Backendens requirements installeres også av Azure under deploy.

## 3. Test etter publisering

1. Åpne nettsiden og `/admin` direkte. Last også `/admin` på nytt for å teste rutingen.
2. Logg inn med Azure-versjonen av `ADMIN_TOKEN`.
3. Last opp CV og publiser arbeidserfaring. Åpne forsiden på nytt og kontroller innhold og nedlasting.
4. Spør AI-assistenten om arbeidserfaringen.
5. Start backendens App Service på nytt, og bekreft at oppdateringene fortsatt er lagret. Kontroller også dette etter neste deploy.

Endringene fra lokal testing ligger i `backend/storage/content.sqlite3` og sendes **ikke** med Git. Første Azure-start bruker `backend/data/profile.json` og den eksisterende statiske PDF-en. Legg inn den ønskede erfaringen og last opp CV via det publiserte panelet. Ta regelmessig sikkerhetskopi av databasen under `/home/data/cv-assistant`.

Ved problemer: se GitHub Actions for bygg/deploy-feil og Azure App Service → Log stream for backendfeil. 503 ved innlogging betyr at `ADMIN_TOKEN` mangler eller er for kort; 401 betyr feil nøkkel.

Referanser:
- https://learn.microsoft.com/en-us/azure/app-service/configure-language-python
- https://learn.microsoft.com/en-us/azure/static-web-apps/build-configuration
