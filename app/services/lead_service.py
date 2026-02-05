from app.database.mongo import db
from app.schemas.lead import LeadCreate, LeadResponse
from app.services.external_service import ExternalService
from bson import ObjectId
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

class LeadService:
    @staticmethod
    def _format_date(date_str: str | None) -> str | None:
        if not date_str:
            return None
        try:
            # Handle formats like "1996-5-30" to "1996-05-30"
            dt = datetime.strptime(date_str, "%Y-%m-%d")
            return dt.strftime("%Y-%m-%d")
        except ValueError:
            return date_str

    @staticmethod
    def _helper(lead) -> dict:
        return {
            "id": str(lead["_id"]),
            "name": lead["name"],
            "email": lead["email"],
            "phone": lead["phone"],
            "birth_date": lead.get("birth_date"),
        }

    @classmethod
    async def create_lead(cls, lead_in: LeadCreate) -> dict:
        birth_date_raw = await ExternalService.get_birth_date()
        birth_date = cls._format_date(birth_date_raw)

        lead_data = lead_in.model_dump()
        lead_data["birth_date"] = birth_date
        
        # Insert into DB
        collection = db.get_db().leads
        result = await collection.insert_one(lead_data)
        
        lead_data["_id"] = result.inserted_id
        return cls._helper(lead_data)

    @classmethod
    async def get_leads(cls) -> list[dict]:
        collection = db.get_db().leads
        leads = []
        async for lead in collection.find():
            leads.append(cls._helper(lead))
        return leads

    @classmethod
    async def get_lead(cls, lead_id: str) -> dict | None:
        collection = db.get_db().leads
        try:
            oid = ObjectId(lead_id)
        except Exception:
            return None
            
        lead = await collection.find_one({"_id": oid})
        if lead:
            return cls._helper(lead)
        return None
