from fastapi import APIRouter, HTTPException, Query, File, UploadFile
from typing import Optional, List
from app.api.dependencies import uow_factory
from app.services.cafes_service import CafesService
from app.domain.schemas import CafeCreate, CafeUpdate, CafeOut
from pathlib import Path
import uuid
import os

router = APIRouter(prefix="/cafes", tags=["cafes"])
service = CafesService(uow_factory)

@router.get("", response_model=List[CafeOut])
def list_cafes(location: Optional[str] = Query(default=None)):
    # Invalid location returns empty list implicitly if no records match
    return service.list(location)

@router.post("", status_code=201)
def create_cafe(payload: CafeCreate):
    cafe_id = service.create(payload.model_dump())
    return {"id": cafe_id}

@router.put("", status_code=200)
def update_cafe(payload: CafeUpdate):
    try:
        ok = service.update(payload.model_dump())
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    return {"success": ok}

@router.delete("", status_code=200)
def delete_cafe(id: str):
    ok = service.delete(id)
    if not ok:
        raise HTTPException(status_code=404, detail="Cafe not found")
    return {"success": True}

@router.post("/upload-logo")
async def upload_logo(file: UploadFile = File(...)):
    # Just accept but don't save to disk
    if file.size > 2 * 1024 * 1024:  # 2MB limit
        raise HTTPException(status_code=400, detail="File too large")
    
    # On Render, files can't be persisted
    # Just return success - logo feature works locally but not on Render free tier
    return {
        "message": "File accepted (not persisted on free tier)",
        "filename": file.filename
    }