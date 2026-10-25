"""Shared portfolio content and authenticated editing endpoints."""
import json
import os
import secrets
import sqlite3
from datetime import datetime, timezone
from pathlib import Path
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from fastapi.responses import Response
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from pydantic import BaseModel, Field, ConfigDict

BASE = Path(__file__).resolve().parent
router = APIRouter()
bearer = HTTPBearer(auto_error=False)
MAX_PDF = 10 * 1024 * 1024


def connect():
    default = '/home/data/cv-assistant' if os.getenv('WEBSITE_SITE_NAME') else str(BASE / 'storage')
    directory = Path(os.getenv('CONTENT_DATA_DIR', default))
    directory.mkdir(parents=True, exist_ok=True)
    db = sqlite3.connect(directory / 'content.sqlite3', timeout=15)
    db.execute('CREATE TABLE IF NOT EXISTS content (key TEXT PRIMARY KEY, value BLOB NOT NULL)')
    return db


def read_value(key):
    db = connect()
    try:
        row = db.execute('SELECT value FROM content WHERE key = ?', (key,)).fetchone()
        return row[0] if row else None
    finally:
        db.close()


def write_values(values):
    db = connect()
    try:
        with db:
            db.executemany('INSERT OR REPLACE INTO content VALUES (?, ?)', values)
    finally:
        db.close()


def load_profile():
    profile = json.loads((BASE / 'data' / 'profile.json').read_text(encoding='utf-8'))
    experience = read_value('experience')
    if experience is not None:
        profile['work_experience'] = json.loads(experience)
    return profile


def require_admin(credentials: Optional[HTTPAuthorizationCredentials] = Depends(bearer)):
    expected = os.getenv('ADMIN_TOKEN', '')
    if len(expected) < 32:
        raise HTTPException(503, 'Administratorpålogging er ikke konfigurert på serveren.')
    if not credentials or not secrets.compare_digest(credentials.credentials.encode(), expected.encode()):
        raise HTTPException(401, 'Feil administratornøkkel.', headers={'WWW-Authenticate': 'Bearer'})


class Experience(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True, extra='forbid')
    company: str = Field(min_length=1, max_length=200)
    role: str = Field(min_length=1, max_length=200)
    period: str = Field(min_length=1, max_length=100)
    country: str = Field(default='', max_length=100)
    tasks: List[str] = Field(default_factory=list, max_length=30)


class ExperienceUpdate(BaseModel):
    experience: List[Experience] = Field(max_length=100)


@router.get('/content')
def public_content():
    metadata = read_value('cv_metadata')
    return {'experience': load_profile()['work_experience'],
            'cv': json.loads(metadata) if metadata else None}


@router.get('/admin/content', dependencies=[Depends(require_admin)])
def admin_content():
    return public_content()


@router.put('/admin/experience', dependencies=[Depends(require_admin)])
def update_experience(payload: ExperienceUpdate):
    entries = [entry.model_dump() for entry in payload.experience]
    if any(len(task) > 2000 for entry in entries for task in entry['tasks']):
        raise HTTPException(422, 'En arbeidsoppgave kan være maks 2000 tegn.')
    write_values([('experience', json.dumps(entries, ensure_ascii=False))])
    return {'experience': entries}


@router.post('/admin/cv', dependencies=[Depends(require_admin)])
async def upload_cv(file: UploadFile = File(...)):
    try:
        data = await file.read(MAX_PDF + 1)
    finally:
        await file.close()
    if len(data) > MAX_PDF:
        raise HTTPException(413, 'PDF-filen kan være maks 10 MB.')
    if not (file.filename or '').lower().endswith('.pdf') or not data.startswith(b'%PDF-') or b'%%EOF' not in data[-4096:]:
        raise HTTPException(422, 'Velg en gyldig PDF-fil.')
    metadata = {'filename': 'Abdel-Sadaqi-CV.pdf', 'size': len(data),
                'updated_at': datetime.now(timezone.utc).isoformat()}
    write_values([('cv', data), ('cv_metadata', json.dumps(metadata))])
    return {'cv': metadata}


@router.get('/cv')
def download_cv():
    data = read_value('cv')
    if data is None:
        raise HTTPException(404, 'Ingen CV er lastet opp ennå.')
    return Response(data, media_type='application/pdf', headers={
        'Content-Disposition': 'attachment; filename="Abdel-Sadaqi-CV.pdf"',
        'Cache-Control': 'no-store', 'X-Content-Type-Options': 'nosniff'})
