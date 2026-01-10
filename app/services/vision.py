from google.genai import Client, types
from app.core.config import settings
from fastapi import HTTPException

client = Client(api_key=settings.AI_API_KEY)

async def analyze_perfume_image(image_bytes: bytes):
    prompt = """
    You are an expert in fine perfumery. Analyze the image of this perfume bottle and strictly 
    return the brand and the specific name of the fragrance.
    
    Response format: Brand | Name
    Example: Parfums de Marly | Layton
    
    If you cannot identify the perfume with certainty, respond only with: Unknown.
    """
    
    try:
        # 1. Envolvemos los bytes correctamente para el nuevo SDK
        image_part = types.Part.from_bytes(
            data=image_bytes,
            mime_type="image/jpeg"
        )

        # 2. Usamos gemini-1.5-flash (el modelo con cuota gratuita real)
        response = client.models.generate_content(
            model="gemini-2.5-flash-lite",
            contents=[prompt, image_part]
        )
        
        # 3. Validamos que la IA haya devuelto texto
        if not response.text or "Unknown" in response.text:
            return None
            
        # 4. Parseamos el resultado
        if "|" in response.text:
            parts = response.text.split("|")
            return {
                "brand": parts[0].strip(),
                "name": parts[1].strip()
            }
        
        return None

    except Exception as e:
        # Imprimimos el error en la consola para saber si es cuota o región
        print(f"Error en Gemini Vision: {e}")
        raise HTTPException(status_code=500, detail="Error al procesar la imagen con Gemini")