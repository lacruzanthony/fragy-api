from fastapi import APIRouter, File, UploadFile, HTTPException
from app.services.recognition import predict_and_get_metadata

router = APIRouter()

@router.post("/identify")
async def identify_perfume(file: UploadFile = File(...)):
    # Leemos los bytes de la imagen
    image_bytes = await file.read()
    
    # Llamamos al servicio
    perfume_data = await predict_and_get_metadata(image_bytes)
    
    if not perfume_data:
        raise HTTPException(status_code=404, detail="No se encontró el perfume en nuestra base de datos")
    
    return {
        "id": perfume_data.get("id"),
        "brand": perfume_data.get("brand"),
        "name": perfume_data.get("name"),
        "image_url": perfume_data.get("image_url"),
        "created_at": perfume_data.get("created_at"),
        "notes": {
            "top": perfume_data.get("notes_top"),
            "heart": perfume_data.get("notes_heart"),
            "base": perfume_data.get("notes_base"),
            "flat": ""
        }
    }

@router.get("/{perfume_id}")
async def get_perfume(perfume_id: int):
    # Ejemplo de otro endpoint para obtener info por ID
    return {"perfume_id": perfume_id, "data": "Metadata aquí"}