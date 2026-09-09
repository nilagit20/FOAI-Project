from fastapi import FastAPI
from pydantic import BaseModel
from knowledge_base import classify_attack, determine_severity

app = FastAPI()


# This defines the "shape" of data we expect to receive.
# FastAPI uses this to automatically check incoming requests are valid.
class IncidentData(BaseModel):
    attackType: str
    failedAttempts: int | None = None
    targetAsset: str | None = None


@app.get("/health")
def health_check():
    return {"status": "AI engine is running"}


@app.post("/analyze")
def analyze_incident(incident: IncidentData):
    classification = classify_attack(incident.attackType, incident.failedAttempts)
    severity = determine_severity(classification, incident.targetAsset)

    return {
        "classification": classification,
        "severity": severity
    }