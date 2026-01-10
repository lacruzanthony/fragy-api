from app.services.vision import analyze_perfume_image
from app.services.supabase import supabase_client

async def scan_perfume_image(image_bytes: bytes):
    # 1. Llamamos al servicio de Vision (Gemini)
    # Este nos devolverá algo como {"brand": "Creed", "name": "Aventus"} o None
    prediction = await analyze_perfume_image(image_bytes)
    
    if not prediction:
        return None
    
    brand = prediction["brand"]
    name = prediction["name"]

    # 2. Buscamos en la base de datos de Supabase
    # Usamos .ilike para que la búsqueda no sea sensible a mayúsculas/minúsculas
    # y soporte pequeñas variaciones en el nombre.
    try:
        response = supabase_client.table("perfumes") \
            .select("id, name") \
            .ilike("name", f"%{name}%") \
            .ilike("brand", f"%{brand}%") \
            .execute()

        if not response.data:
            return None

        # Retornamos el primer resultado encontrado
        return response.data[0]

    except Exception as e:
        print(f"Error querying Supabase: {e}")
        return None