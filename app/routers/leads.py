from fastapi import APIRouter, HTTPException, status
from app.schemas.lead import LeadCreate, LeadResponse
from app.services.lead_service import LeadService

router = APIRouter()

@router.post("/leads", response_model=LeadResponse, status_code=status.HTTP_201_CREATED)
async def create_lead(lead: LeadCreate):
    return await LeadService.create_lead(lead)

@router.get("/leads", response_model=list[LeadResponse])
async def get_leads():
    return await LeadService.get_leads()

@router.get("/leads/{id}", response_model=LeadResponse)
async def get_lead(id: str):
    lead = await LeadService.get_lead(id)
    if not lead:
        raise HTTPException(status_code=404, detail="Lead not found")
    return lead
