# app/services/vision.py
from google.genai import Client
from app.core.config import settings
from fastapi import HTTPException

# El nuevo SDK usa un cliente centralizado
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
        # La nueva forma de llamar a Gemini 1.5 Flash
        response = client.models.generate_content(
            model="gemini-1.5-flash",
            contents=[prompt, image_bytes]
        )
        
        if not response.text or "Unknown" in response.text:
            return None
            
        parts = response.text.split("|")
        if len(parts) == 2:
            return {
                "brand": parts[0].strip(),
                "name": parts[1].strip()
            }
        return None

    except Exception as e:
        print(f"Error en Gemini Vision: {e}")
        raise HTTPException(status_code=500, detail="Error processing image")