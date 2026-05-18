import os
import requests
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("POLIGPT_API_KEY")
base_url = os.getenv("POLIGPT_BASE_URL", "https://api.poligpt.upv.es/v1")

print("Consultando modelos en PoliGPT...")
try:
    headers = {"Authorization": f"Bearer {api_key}"}
    # verify=False porque la UPV usa certificado autofirmado
    response = requests.get(f"{base_url}/models", headers=headers, verify=False, timeout=15)
    response.raise_for_status()
    data = response.json()
    models = data.get("data", [])
    print(f"\n¡Éxito! Se han encontrado {len(models)} modelos disponibles:\n")
    for m in models:
        print(f" - ID: {m.get('id')}")
        if 'permission' in m:
            print(f"   Permisos/Detalles: {m.get('permission')}")
except Exception as e:
    print(f"\nError al consultar los modelos: {e}")
