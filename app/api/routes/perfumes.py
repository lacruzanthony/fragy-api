from fastapi import APIRouter, File, UploadFile, HTTPException
from app.services.recognition import scan_perfume_image

router = APIRouter()

@router.post("/identify")
async def identify_perfume(file: UploadFile = File(...)):
    # Leemos los bytes de la imagen
    image_bytes = await file.read()
    
    # Llamamos al servicio
    perfume_data = await scan_perfume_image(image_bytes)
    
    if not perfume_data:
        raise HTTPException(status_code=404, detail="No se encontró el perfume en nuestra base de datos")
    
    return {
        "id": perfume_data.get("id"),
        "name": perfume_data.get("name"),
    }

@router.get("/{perfume_id}")
async def get_perfume(perfume_id: int):
    # Ejemplo de otro endpoint para obtener info por ID
    return {"perfume_id": perfume_id, "data": "Metadata aquí"}