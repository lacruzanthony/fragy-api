from fastapi import APIRouter, File, UploadFile, HTTPException
from app.services.recognition import scan_perfume_image
from app.services.supabase import supabase_client

router = APIRouter()

@router.post("/identify")
async def identify_perfume(file: UploadFile = File(...)):
    # Leemos los bytes de la imagen
    image_bytes = await file.read()
    
    # Llamamos al servicio
    perfume = await scan_perfume_image(image_bytes)
    
    if not perfume:
        raise HTTPException(status_code=404, detail="No se encontró el perfume en nuestra base de datos")
    
    return {
        "id": perfume.get("id"),
        "name": perfume.get("name"),
    }

@router.get("/{perfume_id}")
async def get_perfume(perfume_id: int):
    try:
        response = supabase_client.table("perfumes") \
            .select("*") \
            .eq("id", perfume_id) \
            .execute()

        if not response.data:
            return None

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

    except Exception as e:
        print(f"Error querying Supabase: {e}")
        return None