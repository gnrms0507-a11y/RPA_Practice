from fastapi import FastAPI, File, HTTPException, UploadFile
from pydantic import BaseModel, Field
from .extractor import extract_case_numbers, extract_subject

MAX_EML_SIZE = 10 * 1024 * 1024
app = FastAPI(title="EML Case Number API", version="1.0.0")

class SubjectRequest(BaseModel):
    subject: str = Field(min_length=1)

class ExtractionResponse(BaseModel):
    success: bool = True
    subject: str
    caseNumber: str | None
    caseNumbers: list[str]

def make_response(subject: str) -> ExtractionResponse:
    numbers = extract_case_numbers(subject)
    return ExtractionResponse(subject=subject, caseNumber=numbers[0] if numbers else None, caseNumbers=numbers)

@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}

@app.post("/api/emails/extract-case-number", response_model=ExtractionResponse)
async def extract_from_eml(file: UploadFile = File(...)) -> ExtractionResponse:
    if not (file.filename or "").lower().endswith(".eml"):
        raise HTTPException(status_code=400, detail="Only .eml files are supported")
    eml_bytes = await file.read(MAX_EML_SIZE + 1)
    if len(eml_bytes) > MAX_EML_SIZE:
        raise HTTPException(status_code=413, detail="EML file exceeds the 10 MB limit")
    try:
        subject = extract_subject(eml_bytes)
    except (ValueError, UnicodeError) as exc:
        raise HTTPException(status_code=400, detail="Invalid EML file") from exc
    return make_response(subject)

@app.post("/api/subjects/extract-case-number", response_model=ExtractionResponse)
def extract_from_subject(request: SubjectRequest) -> ExtractionResponse:
    return make_response(request.subject.strip())
