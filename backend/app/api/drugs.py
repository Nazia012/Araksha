"""
Medication Lookup & Autocomplete API
Provides fast search against curated RxNorm standardized drugs.
"""

from typing import List, Dict, Any
from fastapi import APIRouter, Query
from app.core.database import search_rxnorm_medications

router = APIRouter(prefix="/api/v1/drugs", tags=["Drugs"])


@router.get("/lookup")
async def lookup_drugs(
    q: str = Query(..., min_length=1, description="Medication generic or brand name query"),
    limit: int = Query(15, ge=1, le=50, description="Max results")
) -> Dict[str, Any]:
    """
    Autocomplete/fuzzy search against local medication records.
    Returns matched generic name, RxCUI, brand names, and drug class.
    """
    matches = search_rxnorm_medications(query=q, limit=limit)
    return {
        "query": q,
        "count": len(matches),
        "results": matches
    }
