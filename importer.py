import os
import time
import re
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
from supabase import create_client, Client

load_dotenv()
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

def extraer_detalle(html):
    soup = BeautifulSoup(html, 'html.parser')
    
    brand_elem = soup.select_one('span[itemprop="brand"] span[itemprop="name"]')
    brand = brand_elem.text.strip() if brand_elem else "N/A"
    
    h1 = soup.find('h1', class_='p_name_h1')
    name_full = h1.get_text(" ", strip=True) if h1 else "N/A"
    name = re.sub(r'\s\d{4}$', '', name_full.replace(brand, "").strip())

    blacklist = [
        "Top Notes", "Heart Notes", "Base Notes", 
        "Notas de Salida", "Notas de Corazón", "Notas de Fondo",
        "Pyramid", "More", "View"
    ]

    def limpiar_lista(raw_list):
        return [n.strip() for n in raw_list if n.strip() and n.strip() not in blacklist]

    top = limpiar_lista([img['alt'] for img in soup.select('.pyramid_block.nb_t img[alt]')])
    heart = limpiar_lista([img['alt'] for img in soup.select('.pyramid_block.nb_m img[alt]')])
    base = limpiar_lista([img['alt'] for img in soup.select('.pyramid_block.nb_b img[alt]')])
    
    flat = []
    if not (top or heart or base):
        flat_raw = [img.get('alt') for img in soup.select('.notes_list img[alt], .notes_items img[alt]')]
        flat = limpiar_lista(flat_raw)

    img_tag = soup.select_one('img.p-main-img, img[itemprop="image"]')
    image_url = img_tag['src'] if img_tag else None

    return {
        "brand": brand,
        "name": name,
        "notes_top": ", ".join(top),
        "notes_heart": ", ".join(heart),
        "notes_base": ", ".join(base),
        "notes_flat": ", ".join(list(dict.fromkeys(flat))),
        "image_url": image_url
    }

def ejecutar_limpieza():
    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    
    try:
        print("🔍 Obteniendo URLs existentes de la base de datos...")
        existing_urls_data = supabase.table("perfumes").select("source_url").execute()
        existing_urls = {item['source_url'] for item in existing_urls_data.data}
        print(f"✅ Se encontraron {len(existing_urls)} URLs existentes.")
    except Exception as e:
        print(f"⚠️ No se pudo obtener las URLs existentes. Error: {e}")
        existing_urls = set()

    try:
        print("🔍 Accediendo a la página de marcas...")
        driver.get("https://www.parfumo.com/Brands")
        time.sleep(5)

        brand_links = [el.get_attribute('href') for el in driver.find_elements(By.CSS_SELECTOR, ".blist a")]
        print(f"✅ Se encontraron {len(brand_links)} marcas.")

        all_perfume_links = []
        for brand_link in brand_links:
            print(f"   > Procesando marca: {brand_link.split('/')[-1]}")
            driver.get(brand_link)
            time.sleep(3)
            
            perfume_elements = driver.find_elements(By.CSS_SELECTOR, ".pgrid a.grey")
            for el in perfume_elements:
                perfume_href = el.get_attribute('href')
                if "/Perfumes/" in perfume_href:
                    all_perfume_links.append(perfume_href)

        unique_perfume_links = sorted(list(set(all_perfume_links)))
        new_perfume_links = [link for link in unique_perfume_links if link not in existing_urls]
        
        print(f"✅ Se encontraron {len(unique_perfume_links)} perfumes en total.")
        print(f"🆕 Se procesarán {len(new_perfume_links)} perfumes nuevos.")

        for i, link in enumerate(new_perfume_links[:30]): # Procesar de 30 en 30
            print(f"[{i+1}/{len(new_perfume_links)}] Procesando: {link.split('/')[-1]}")
            driver.get(link)
            
            driver.execute_script("window.scrollTo(0, 500);")
            time.sleep(3)
            
            data = extraer_detalle(driver.page_source)
            data["source_url"] = link
            
            try:
                supabase.table("perfumes").upsert(data, on_conflict="source_url").execute()
                print(f"   ✨ Guardado: {data['brand']} - {data['name']}")
            except Exception as e:
                print(f"   ❌ Error en DB: {e}")
                
    finally:
        driver.quit()
        print("\n🏁 ¡Proceso de importación terminado!")

if __name__ == "__main__":
    ejecutar_limpieza()
r.quit()
        print("\n🏁 ¡Limpieza terminada!")

if __name__ == "__main__":
    ejecutar_limpieza()