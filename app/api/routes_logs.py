from fastapi import APIRouter, Query
from app.services.logging_service import get_recent_decisions

router = APIRouter(prefix="/logs", tags=["Logs"])


@router.get("/decisions")
def read_recent_decisions(limit: int = Query(default=10, ge=1, le=100)):
    return {
        "count": limit,
        "records": get_recent_decisions(limit=limit)
    }