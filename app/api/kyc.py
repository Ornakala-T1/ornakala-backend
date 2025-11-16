# python
from uuid import uuid4
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, status

from app.api.dependencies import get_current_user, get_user_kyc_repository
from app.api.schemas.kyc import KYCCreateRequest, KYCUpdateRequest, KYCResponse
from app.domain.models import User, UserKYC
from app.domain.repository import UserKYCRepository

router = APIRouter(prefix="/kyc", tags=["kyc"])

@router.get("", response_model=KYCResponse)
async def get_my_kyc(
        current_user: User = Depends(get_current_user),
        repo: UserKYCRepository = Depends(get_user_kyc_repository),
):
    kyc = await repo.get_by_user_id(current_user.id)
    if not kyc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="KYC not found")
    return KYCResponse(
        id=str(kyc.id),
        legal_name=kyc.legal_name,
        document_type=kyc.document_type,
        document_number=kyc.document_number,
        dob=kyc.dob,
        address=kyc.address,
        country=kyc.country,
        status=kyc.status,
        created_at=kyc.created_at,
        updated_at=kyc.updated_at,
    )

@router.post("", response_model=KYCResponse, status_code=status.HTTP_201_CREATED)
async def create_my_kyc(
        payload: KYCCreateRequest,
        current_user: User = Depends(get_current_user),
        repo: UserKYCRepository = Depends(get_user_kyc_repository),
):
    if await repo.exists_by_user_id(current_user.id):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="KYC already exists")

    now = datetime.utcnow()
    kyc = UserKYC(
        id=uuid4(),
        user_id=current_user.id,
        legal_name=payload.legal_name,
        document_type=payload.document_type,
        document_number=payload.document_number,
        dob=payload.dob,
        address=payload.address,
        country=payload.country,
        status="pending",
        created_at=now,
        updated_at=now,
    )
    await repo.add(kyc)
    # Commit via the concrete repository's session
    await repo.session.commit()
    return KYCResponse(
        id=str(kyc.id),
        legal_name=kyc.legal_name,
        document_type=kyc.document_type,
        document_number=kyc.document_number,
        dob=kyc.dob,
        address=kyc.address,
        country=kyc.country,
        status=kyc.status,
        created_at=kyc.created_at,
        updated_at=kyc.updated_at,
    )

@router.put("", response_model=KYCResponse)
async def update_my_kyc(
        payload: KYCUpdateRequest,
        current_user: User = Depends(get_current_user),
        repo: UserKYCRepository = Depends(get_user_kyc_repository),
):
    kyc = await repo.get_by_user_id(current_user.id)
    if not kyc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="KYC not found")

    if payload.legal_name is not None:
        kyc.legal_name = payload.legal_name
    if payload.document_type is not None:
        kyc.document_type = payload.document_type
    if payload.document_number is not None:
        kyc.document_number = payload.document_number
    if payload.dob is not None:
        kyc.dob = payload.dob
    if payload.address is not None:
        kyc.address = payload.address
    if payload.country is not None:
        kyc.country = payload.country
    if payload.status is not None:
        kyc.status = payload.status
    kyc.updated_at = datetime.utcnow()

    await repo.update(kyc)
    await repo.session.commit()
    return KYCResponse(
        id=str(kyc.id),
        legal_name=kyc.legal_name,
        document_type=kyc.document_type,
        document_number=kyc.document_number,
        dob=kyc.dob,
        address=kyc.address,
        country=kyc.country,
        status=kyc.status,
        created_at=kyc.created_at,
        updated_at=kyc.updated_at,
    )

@router.delete("", status_code=status.HTTP_204_NO_CONTENT)
async def delete_my_kyc(
        current_user: User = Depends(get_current_user),
        repo: UserKYCRepository = Depends(get_user_kyc_repository),
):
    if await repo.exists_by_user_id(current_user.id):
        await repo.delete_by_user_id(current_user.id)
        await repo.session.commit()
    return None
