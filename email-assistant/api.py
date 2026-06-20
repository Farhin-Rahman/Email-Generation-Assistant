"""
FastAPI service exposing the email generation assistant via HTTP.

Endpoints:
  GET  /health          — liveness check
  POST /generate        — generate one email from intent, facts, and tone
  POST /evaluate        — generate + score an email with all 3 metrics
"""

import os
from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from generator import generate_email
from evaluator import evaluate_email

app = FastAPI(
    title="Email Generation Assistant",
    description="LLM-powered professional email generator with custom evaluation metrics.",
    version="1.0.0",
)

VALID_MODELS = {"mistral-large-latest", "mistral-small-latest"}


class GenerateRequest(BaseModel):
    intent: str
    facts: list[str]
    tone: str
    model: str = "mistral-large-latest"


class GenerateResponse(BaseModel):
    model: str
    email: str


class EvaluateResponse(BaseModel):
    model: str
    email: str
    scores: dict


@app.get("/health")
async def health():
    return {"status": "ok"}


@app.post("/generate", response_model=GenerateResponse)
async def generate(req: GenerateRequest):
    if req.model not in VALID_MODELS:
        raise HTTPException(status_code=400, detail=f"model must be one of {VALID_MODELS}")
    email = generate_email(req.intent, req.facts, req.tone, req.model)
    return GenerateResponse(model=req.model, email=email)


@app.post("/evaluate", response_model=EvaluateResponse)
async def evaluate(req: GenerateRequest):
    if req.model not in VALID_MODELS:
        raise HTTPException(status_code=400, detail=f"model must be one of {VALID_MODELS}")
    email = generate_email(req.intent, req.facts, req.tone, req.model)
    scores = evaluate_email({"intent": req.intent, "facts": req.facts, "tone": req.tone}, email)
    return EvaluateResponse(model=req.model, email=email, scores=scores)
