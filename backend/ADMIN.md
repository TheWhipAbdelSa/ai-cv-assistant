# Kontrollpanel

Åpne `/admin` på nettsiden. Panelet lar deg publisere PDF-CV (maks 10 MB) og legge til, endre, sortere og fjerne arbeidserfaring. Arbeidserfaring deles av nettsiden og AI-assistenten. PDF-innhold importeres ikke automatisk til AI-profilen.

## Konfigurasjon

- Sett `ADMIN_TOKEN` i backendens miljøvariabler til en tilfeldig, hemmelig nøkkel på minst 32 tegn. Generer for eksempel med `python -c "import secrets; print(secrets.token_urlsafe(32))"`. Lokalt kan nøkkelen legges i `backend/.env`. Bruk nøkkelen som passord i panelet. Den lagres bare i sidens minne; en omlasting krever ny innlogging. Ikke legg den i frontend eller Git.
- Sett `VITE_API_URL` til backendens adresse ved frontend-bygg. Lokal standard er `http://localhost:8000`.
- Bruk HTTPS ved publisering.
- `CONTENT_DATA_DIR` angir mappe for SQLite-databasen, inkludert CV-filen. Standard lokalt er `backend/storage`; på Azure App Service er den `/home/data/cv-assistant`. Bruk et varig, skrivbart volum utenfor deploymappen. Bekreft at App Service-lagring er aktivert og ta sikkerhetskopi av databasen. Denne første versjonen er laget for én backend-instans.
- Deploy både frontend og backend. `staticwebapp.config.json` gir direkte tilgang til `/admin` på Azure Static Web Apps.

Ingen administratornøkkel er sjekket inn. Administrasjon er sperret til nøkkelen er satt. Endringer publiseres først når du trykker publiser/last opp; navigasjon bort fra siden forkaster ulagrede skjemaendringer.

## Verifisering

Fra prosjektroten: `python -m unittest backend.test_content` og `npm --prefix frontend run build`.
