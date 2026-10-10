
from typing import Optional
from uuid import uuid4

from fastapi import FastAPI, HTTPException
from fastapi.concurrency import run_in_threadpool
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from agent.loop import Agent


# ============================================================
# FastAPI Application
# ============================================================

app = FastAPI(
    title="Agentic AI Assistant API",
    description="Backend API for the Agentic AI Assistant",
    version="1.0.0",
)


# ============================================================
# CORS
# ============================================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ============================================================
# Request / Response Schemas
# ============================================================

class AgentRequest(BaseModel):
    message: str = Field(..., min_length=1)
    session_id: Optional[str] = None


class AgentAPIResponse(BaseModel):
    session_id: str
    response: str


# ============================================================
# Initialize Agent
# ============================================================

agent = Agent(
    model="qwen2.5:latest",
    debug=True,
)


# ============================================================
# Health Checks
# ============================================================

@app.get("/")
async def root():
    return {
        "name": "Agentic AI Assistant API",
        "status": "running",
        "version": "1.0.0",
    }


@app.get("/health")
async def health():
    return {
        "status": "healthy",
    }


# ============================================================
# Agent Execution
# ============================================================

async def run_agent(
    message: str,
    session_id: str,
) -> str:
    """
    Run the agent in a worker thread.

    The agent handles direct LLM answers and tool execution.
    """

    result = await run_in_threadpool(
        agent.run,
        message,
        session_id,
    )

    if not result.success:
        raise HTTPException(
            status_code=502,
            detail={
                "message": result.response,
                "error": result.error,
                "session_id": result.session_id,
            },
        )

    return result.response


# ============================================================
# Agent Endpoint
# ============================================================

@app.post(
    "/agent/run",
    response_model=AgentAPIResponse,
)
async def agent_run(request: AgentRequest):
    session_id = request.session_id or str(uuid4())

    try:
        response = await run_agent(
            message=request.message,
            session_id=session_id,
        )

        return AgentAPIResponse(
            session_id=session_id,
            response=response,
        )

    except HTTPException:
        raise

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=f"Agent execution failed: {exc}",
        ) from exc


# ============================================================
# Session Endpoint
# ============================================================

@app.get("/agent/session/{session_id}")
async def get_session(session_id: str):
    return {
        "session_id": session_id,
        "status": "active",
    }
