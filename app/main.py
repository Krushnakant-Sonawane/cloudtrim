import os

from botocore.exceptions import BotoCoreError, ClientError
from fastapi import FastAPI, HTTPException

from app.scanner import run_scan

app = FastAPI(title="CloudTrim", description="Read-only AWS cost-waste scanner")


@app.get("/")
def root():
    return {
        "name": "CloudTrim",
        "docs": "/docs",
        "health": "/health",
        "findings": "/findings",
    }


@app.get("/health")
def health():
    return {"status": "ok", "version": os.getenv("APP_VERSION", "dev")}


@app.get("/findings")
def findings(region: str = "us-east-1"):
    try:
        return run_scan(region)
    except (BotoCoreError, ClientError) as e:  # AWS/credential problems only
        raise HTTPException(
            status_code=502, detail=f"Scan failed: {type(e).__name__}"
        ) from e