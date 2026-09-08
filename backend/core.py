from __future__ import annotations

from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from enum import Enum
from typing import Any
from uuid import uuid4


class RiskLevel(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class PolicyDecision(str, Enum):
    ALLOW = "allow"
    REVIEW = "review"
    REQUIRE_APPROVAL = "require_approval"


class ActionState(str, Enum):
    READY = "ready"
    WAITING_POLICY = "waiting_policy"
    WAITING_APPROVAL = "waiting_approval"


@dataclass(frozen=True)
class ActionReceipt:
    receipt_id: str
    action_type: str
    description: str
    risk: str
    external_effect: bool
    decision: str
    state: str
    created_at: str

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


def evaluate_action(
    *,
    action_type: str,
    description: str,
    risk: RiskLevel,
    external_effect: bool,
) -> ActionReceipt:
    """Evaluate a proposed action without executing it.

    The core is deliberately conservative:
    - high-risk actions always require explicit approval;
    - any action that can create an external effect requires approval;
    - medium-risk actions stop for policy review;
    - only low-risk, read-only/local proposals can become READY.
    """

    if risk is RiskLevel.HIGH or external_effect:
        decision = PolicyDecision.REQUIRE_APPROVAL
        state = ActionState.WAITING_APPROVAL
    elif risk is RiskLevel.MEDIUM:
        decision = PolicyDecision.REVIEW
        state = ActionState.WAITING_POLICY
    else:
        decision = PolicyDecision.ALLOW
        state = ActionState.READY

    return ActionReceipt(
        receipt_id=str(uuid4()),
        action_type=action_type,
        description=description,
        risk=risk.value,
        external_effect=external_effect,
        decision=decision.value,
        state=state.value,
        created_at=datetime.now(timezone.utc).isoformat(),
    )


def core_reply(mode: str, message: str) -> dict[str, str]:
    """Return a truthful core-routing response.

    This repository does not pretend that a model provider or tool executor is
    configured when one is not. The response proves the routing layer works and
    preserves the safety boundary: conversation is separate from execution.
    """

    normalized = mode.strip().lower()

    if normalized == "nova":
        reply = (
            "NOVA core received the request. No external action was executed. "
            "The request is ready for an approved reasoning/model provider."
        )
    elif normalized == "dragon":
        reply = (
            "DRAGON core received the request. Execution remains blocked until "
            "a tool plan passes policy and any required approval."
        )
    elif normalized == "eve":
        reply = (
            "EVE core received the request. This foundation currently provides "
            "routing and safety controls, not an unconfigured AI provider."
        )
    else:
        raise ValueError("Invalid mode. Use nova, dragon, or eve.")

    return {
        "mode": normalized,
        "reply": reply,
        "request_preview": message[:120],
        "executed": "false",
        "provider": "core-only",
    }
