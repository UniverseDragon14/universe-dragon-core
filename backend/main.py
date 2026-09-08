from __future__ import annotations

import logging
import os
from typing import Any

from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field

from core import RiskLevel, core_reply, evaluate_action


logging.basicConfig(level=os.getenv("LOG_LEVEL", "INFO"))
logger = logging.getLogger("universal_dragon_core")


def _allowed_origins() -> list[str]:
    raw = os.getenv("FRONTEND_ORIGINS", "")
    return [origin.strip() for origin in raw.split(",") if origin.strip()]


app = FastAPI(
    title="Universal Dragon Core",
    version="0.2.0",
    description=(
        "Safe foundation API for NOVA/EVE routing, policy evaluation, and "
        "approval gating. This service does not silently execute external actions."
    ),
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=_allowed_origins(),
    allow_credentials=False,
    allow_methods=["GET", "POST"],
    allow_headers=["Content-Type"],
)


class ChatRequest(BaseModel):
    mode: str = Field(min_length=3, max_length=16)
    message: str = Field(min_length=1, max_length=4000)


class ActionPlanRequest(BaseModel):
    action_type: str = Field(min_length=1, max_length=80)
    description: str = Field(min_length=1, max_length=1000)
    risk: RiskLevel
    external_effect: bool = False


@app.exception_handler(Exception)
async def unhandled_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    logger.exception(
        "Unhandled error path=%s method=%s",
        request.url.path,
        request.method,
    )
    return JSONResponse(
        status_code=500,
        content={
            "error": "internal_error",
            "detail": "The request could not be completed safely.",
        },
    )


@app.get("/")
def home() -> dict[str, Any]:
    return {
        "status": "online",
        "system": "Universal Dragon Core",
        "version": app.version,
        "execution_policy": "no silent external execution",
    }


@app.get("/api/health")
def health() -> dict[str, str]:
    return {
        "status": "ok",
        "service": "universal-dragon-core",
        "version": app.version,
    }


@app.get("/api/capabilities")
def capabilities() -> dict[str, Any]:
    return {
        "capabilities": [
            "nova-eve-dragon-routing",
            "input-validation",
            "policy-evaluation",
            "approval-gating",
            "action-receipts",
            "safe-error-boundary",
        ],
        "external_execution_enabled": False,
    }


@app.post("/api/chat")
def chat(req: ChatRequest) -> dict[str, str]:
    try:
        return core_reply(req.mode, req.message)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@app.post("/api/actions/plan")
def plan_action(req: ActionPlanRequest) -> dict[str, Any]:
    receipt = evaluate_action(
        action_type=req.action_type,
        description=req.description,
        risk=req.risk,
        external_effect=req.external_effect,
    )

    logger.info(
        "action_plan receipt_id=%s action_type=%s risk=%s decision=%s state=%s",
        receipt.receipt_id,
        receipt.action_type,
        receipt.risk,
        receipt.decision,
        receipt.state,
    )

    return {
        "receipt": receipt.to_dict(),
        "executed": False,
        "note": "Planning only. No tool or external action was executed.",
    }
