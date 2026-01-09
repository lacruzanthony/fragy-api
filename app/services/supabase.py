from supabase import create_client, Client
from app.core.config import settings

# Inicializamos el cliente una sola vez usando los settings validados
supabase_client: Client = create_client(settings.SUPABASE_URL, settings.SUPABASE_KEY)