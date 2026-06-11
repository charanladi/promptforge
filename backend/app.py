from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from optimizer import optimize_prompt
import os

app = FastAPI(title="PromptForge API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class OptimizeRequest(BaseModel):
    prompt: str
    target_model: str = "claude"
    style: str = "general"

class OptimizeResponse(BaseModel):
    original: str
    optimized: str
    issues_found: list[str]
    improvement_score: int

@app.post("/optimize", response_model=OptimizeResponse)
async def optimize(req: OptimizeRequest):
    if not req.prompt.strip():
        raise HTTPException(status_code=400, detail="Prompt cannot be empty")
    if len(req.prompt) > 2000:
        raise HTTPException(status_code=400, detail="Prompt too long (max 2000 chars)")
    result = await optimize_prompt(req.prompt, req.target_model, req.style)
    return result

@app.get("/health")
def health():
    return {"status": "ok", "service": "PromptForge"}

app.mount("/", StaticFiles(directory="../frontend", html=True), name="static")
