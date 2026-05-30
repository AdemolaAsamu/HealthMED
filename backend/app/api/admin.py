"""
Admin authentication endpoints.
"""
import os
import secrets

from fastapi import APIRouter, HTTPException

from app import schemas

router = APIRouter(prefix="/api/admin", tags=["admin"])


@router.post("/login", response_model=schemas.AdminLoginResponse)
def admin_login(request: schemas.AdminLoginRequest):
    expected_key = os.getenv("ADMIN_API_KEY")
    if not expected_key:
        raise HTTPException(status_code=503, detail="Admin login is not configured")

    if not secrets.compare_digest(request.admin_key, expected_key):
        raise HTTPException(status_code=401, detail="Invalid admin key")

    return schemas.AdminLoginResponse(authenticated=True)
