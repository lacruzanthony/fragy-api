from fastapi import APIRouter, File, UploadFile, HTTPException
from app.services.recognition import scan_perfume
from app.services.exceptions import (
    ImageUnreadableError, 
    PerfumeNotFoundError, 
    ServiceError
)
from app.services.supabase import supabase_client

router = APIRouter()

@router.post("/identify")
async def identify_perfume(file: UploadFile = File(...)):
    try:
        image_bytes = await file.read()
        perfume = await scan_perfume(image_bytes)
        
        return {
            "id": perfume.get("id"),
            "name": perfume.get("name"),
        }

    except ImageUnreadableError as e:
        raise HTTPException(
            status_code=422, 
            detail="Could not clearly identify the perfume bottle. Please try a clearer photo."
        )
    except PerfumeNotFoundError as e:
        raise HTTPException(
            status_code=404, 
            detail="Perfume identified but not found in our database."
        )
    except ServiceError as e:
        raise HTTPException(
            status_code=500, 
            detail="The identification service is currently unavailable."
        )
    except Exception as e:
        print(f"Unexpected error: {e}")
        raise HTTPException(
            status_code=500, 
            detail="An unexpected error occurred during identification."
        )

@router.get("/{perfume_id}")
async def get_perfume(perfume_id: int):
    try:
        response = supabase_client.table("perfumes") \
            .select("*") \
            .eq("id", perfume_id) \
            .execute()

        if not response.data:
            raise HTTPException(status_code=404, detail="Perfume metadata not found.")

        perfume = response.data[0]

        return {
            "id": perfume.get("id"),
            "name": perfume.get("name"),
            "brand": perfume.get("brand"),
            "image_url": perfume.get("image_url"),
            "notes": {
                "top": perfume.get("notes_top"),
                "heart": perfume.get("notes_heart"),
                "base": perfume.get("notes_base"),
                "flat": perfume.get("notes_flat"),
            }
        }

    except HTTPException:
        raise
    except Exception as e:
        print(f"Error querying Supabase: {e}")
        raise HTTPException(status_code=500, detail="Error retrieving perfume metadata.")
