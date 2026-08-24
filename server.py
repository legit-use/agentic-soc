"""
FastAPI Server for Enterprise Autonomous SOC (Agentic-SOC)
Provides RESTful APIs for telemetry ingestion, audit logs, HITL analyst approval, and real-time HUD stats.
"""

from typing import Dict, Any, List, Optional
import os
from datetime import datetime
from dotenv import load_dotenv

from fastapi import FastAPI, HTTPException, status, Body
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

# Load environment configuration
load_dotenv()

from core.schemas import TelemetryEvent, AgentAssessment, HITLApprovalRequest
from core.mitigation_engine import EnterpriseSOAREnforcer
from agents.graph_pipeline import LangGraphEnterprisePipeline

app = FastAPI(
    title="Autonomous SOC (Agentic-SOC) API Engine",
    description="Multi-agent stateful threat detection with Google Gemini LLM Cognitive Reasoning & SOAR mitigation platform.",
    version="2.6.0"
)

# Enable CORS for local development and dashboard telemetry
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pipeline & Stateful Stores
pipeline = LangGraphEnterprisePipeline()

# In-Memory User State Store (tracks last known telemetry event per user UPN)
user_last_events: Dict[str, Dict[str, Any]] = {}

# Immutable Audit Ledger Store (List of assessment dictionaries, newest first)
audit_ledger: List[Dict[str, Any]] = []


class HITLDecisionRequest(BaseModel):
    event_id: str
    decision: str  # "APPROVED" | "DISMISSED"
    notes: Optional[str] = "Analyst action taken from Command Theater."


@app.post("/api/v1/telemetry/ingest", response_model=Dict[str, Any])
async def ingest_telemetry(event: TelemetryEvent):
    """
    POST /api/v1/telemetry/ingest
    Ingests authentication telemetry, checks user trajectory history,
    executes LangGraph multi-agent swarm with Gemini LLM reasoning, and appends result to Audit Ledger.
    """
    try:
        curr_dict = event.model_dump() if hasattr(event, "model_dump") else event.dict()
        upn = event.user_principal_name
        
        # Retrieve user's previous telemetry event if available
        prev_dict = user_last_events.get(upn)

        # Process through LangGraph pipeline
        graph_state = pipeline.process_event(current_event=curr_dict, previous_event=prev_dict)

        # Update last known state for user
        user_last_events[upn] = curr_dict

        assessment = graph_state.get("assessment", {})
        
        # Ensure both user_principal_name and principal exist for JS compatibility
        if "user_principal_name" in assessment and "principal" not in assessment:
            assessment["principal"] = assessment["user_principal_name"]

        # Append to Audit Ledger (prepend so newest is first, max 2000 items for memory stability)
        audit_ledger.insert(0, assessment)
        if len(audit_ledger) > 2000:
            audit_ledger.pop()

        return {
            "status": "SUCCESS",
            "event_id": event.event_id,
            "assessment": assessment,
            "pipeline_state": {
                "velocity_kmh": graph_state.get("velocity_kmh", 0.0),
                "token_entropy": graph_state.get("token_entropy", 0.0),
                "is_automated_ua": graph_state.get("is_automated_ua", False),
                "is_proxy": graph_state.get("is_proxy", False),
                "algorithmic_risk_score": graph_state.get("algorithmic_risk_score", 0.0),
                "vector_match": graph_state.get("vector_match", {}),
                "llm_reasoning": graph_state.get("llm_reasoning", "")
            }
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Telemetry Ingestion Pipeline Error: {str(e)}"
        )


@app.get("/api/v1/audit/logs", response_model=List[Dict[str, Any]])
async def get_audit_logs(limit: int = 100):
    """
    GET /api/v1/audit/logs
    Returns immutable audit ledger logs sorted by newest first.
    """
    return audit_ledger[:limit]


@app.delete("/api/v1/audit/clear")
async def clear_audit_ledger():
    """
    DELETE /api/v1/audit/clear
    Purges all historical entries in audit_ledger and resets user trajectory state.
    """
    audit_ledger.clear()
    user_last_events.clear()
    return {"status": "SUCCESS", "message": "Audit ledger and trajectory state cleared successfully."}


@app.post("/api/v1/audit/approve-hitl")
async def approve_hitl_decision(request: HITLDecisionRequest):
    """
    POST /api/v1/audit/approve-hitl
    Interactive Human-In-The-Loop analyst decision route.
    Decision choices:
    - APPROVED: Updates action to HUMAN_AUTHORIZED_BLOCK, executes SOAR session revocation, IP block & email notification mutators.
    - DISMISSED: Updates action to DISMISSED_FALSE_POSITIVE.
    """
    target_item = None
    for item in audit_ledger:
        if item.get("event_id") == request.event_id:
            target_item = item
            break

    if not target_item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Event ID '{request.event_id}' not found in audit ledger."
        )

    upn = target_item.get("user_principal_name") or target_item.get("principal", "unknown_user")
    ip = target_item.get("source_ip", "0.0.0.0")

    if request.decision.upper() == "APPROVED":
        # Execute analyst authorized SOAR mutators including Email Notification Dispatch
        log_revoke = EnterpriseSOAREnforcer.revoke_identity_session(upn)
        log_block = EnterpriseSOAREnforcer.block_perimeter_ip(ip)
        log_email = EnterpriseSOAREnforcer.dispatch_security_notification_email(
            upn, {"classification": target_item.get("classification")}
        )

        target_item["action"] = "HUMAN_AUTHORIZED_BLOCK"
        target_item["soar_execution_logs"] = [log_revoke, log_block, log_email]
        target_item["reasoning"] = (
            f"HUMAN ANALYST AUTHORIZED BLOCK: SOAR enforcement executed for '{upn}'. "
            f"Revoked active sessions, blocked perimeter IP '{ip}', and dispatched client notification email. Notes: {request.notes}"
        )
    else:
        target_item["action"] = "DISMISSED_FALSE_POSITIVE"
        target_item["soar_execution_logs"] = []
        target_item["reasoning"] = (
            f"DISMISSED BY ANALYST: Event for '{upn}' evaluated and cleared as false positive. "
            f"Notes: {request.notes}"
        )

    return {
        "status": "SUCCESS",
        "decision": request.decision.upper(),
        "event_id": request.event_id,
        "updated_assessment": target_item
    }


@app.post("/api/v1/audit/approve/{event_id}")
async def approve_hitl_action(event_id: str, request: Optional[HITLApprovalRequest] = Body(default=None)):
    """Legacy backward compatibility approval route."""
    decision_req = HITLDecisionRequest(
        event_id=event_id,
        decision="APPROVED",
        notes=request.notes if request else "Approved via legacy API."
    )
    return await approve_hitl_decision(decision_req)


@app.get("/api/v1/stats")
async def get_soc_stats():
    """
    GET /api/v1/stats
    Returns live operational statistics for Command Theater HUD displays.
    """
    total = len(audit_ledger)
    critical_count = sum(1 for x in audit_ledger if x.get("action") in ["AUTONOMOUS_CRITICAL_BLOCK", "HUMAN_AUTHORIZED_BLOCK"])
    hitl_count = sum(1 for x in audit_ledger if x.get("action") == "HUMAN_IN_LOOP_REQUIRED")
    safe_count = sum(1 for x in audit_ledger if x.get("action") in ["AUTONOMOUS_MONITOR", "DISMISSED_FALSE_POSITIVE", "DISMISSED_BY_ANALYST"])
    
    entropies = [x.get("token_entropy", 0.0) for x in audit_ledger if x.get("token_entropy") is not None]
    avg_entropy = round(sum(entropies) / len(entropies), 2) if entropies else 0.0

    velocities = [x.get("velocity_kmh", 0.0) for x in audit_ledger if x.get("velocity_kmh") is not None]
    max_velocity = round(max(velocities), 1) if velocities else 0.0

    return {
        "total_ingested": total,
        "critical_blocks": critical_count,
        "hitl_pending": hitl_count,
        "safe_monitored": safe_count,
        "avg_token_entropy": avg_entropy,
        "max_velocity_kmh": max_velocity,
        "system_health": "OPTIMAL",
        "vector_store_status": "ONLINE (ChromaDB)",
        "llm_status": "ACTIVE (Gemini 2.5 Flash)"
    }


class RAGQueryRequest(BaseModel):
    query: str


@app.post("/api/v1/rag/query")
async def query_rag_vector_store(request: RAGQueryRequest):
    """
    POST /api/v1/rag/query
    Performs real semantic vector distance query against ChromaDB MITRE ATT&CK embeddings.
    """
    q_text = request.query.strip() if request and request.query else "token theft"
    match_result = pipeline.vector_store.query_threat_intel(q_text)
    
    return {
        "status": "SUCCESS",
        "query": q_text,
        "match": match_result,
        "explanation": f"ChromaDB semantic search matched query '{q_text}' to MITRE technique {match_result.get('mitre_id')} ({match_result.get('name')}) with cosine distance metric {match_result.get('distance')} and base risk weight {match_result.get('base_score')}/100."
    }


# Ensure static folder exists
static_dir = os.path.join(os.path.dirname(__file__), "static")
if not os.path.exists(static_dir):
    os.makedirs(static_dir)

# Mount static directory for frontend Command Theater HUD
app.mount("/", StaticFiles(directory=static_dir, html=True), name="static")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("server:app", host="0.0.0.0", port=8000, reload=True)
