from google.genai import Client, types
from app.core.config import settings
from fastapi import HTTPException

client = Client(api_key=settings.AI_API_KEY)

async def analyze_perfume_image(image_bytes: bytes):
    prompt = """
    You are a high-end niche perfumery expert and visual analyst. Your task is to identify the perfume in this image with surgical precision.

    Follow these steps logically:
    1. BRAND IDENTIFICATION: Look for the logo or coat of arms. Is it the distinct Parfums de Marly raised horses?
    2. COLOR ANALYSIS: This is critical. 
    - If the bottle is deep navy blue/matte blue, it is LAYTON.
    - If the bottle is metallic brown/copper/dark red, it is HEROD.
    - If the bottle is silver/grey, it is PEGASUS.
    3. TEXTUAL CLUES: Try to read any text on the front label or the base of the bottle.
    4. FINAL VERIFICATION: Does the color match the characteristic bottle for that specific model?

    Return ONLY the Brand and Name in this format: "Brand Name" (e.g., "Parfums de Marly | Layton").
    Do not provide descriptions or apologies. If unsure, provide your best expert guess based on the bottle color.
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
        
        print(f"Gemini Vision response: {response.text}")
            
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