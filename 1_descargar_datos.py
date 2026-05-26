import pandas as pd
import requests
import time

recursos = {
    2023: {"nombre": "Bono Protección Beneficiarios 2023", "resource_id": "fed0c04a-3a39-4878-86d7-e9bb81d7061f"},
    2022: {"nombre": "Bono Protección Beneficiarios 2022", "resource_id": "876a675c-3d1b-4f0e-a481-128d288f9135"},
    2021: {"nombre": "Ingreso Ético Familiar - Beneficiarios 2021", "resource_id": "9aaa497a-61a1-4cc7-a9dd-22128bbd56d7"},
    2020: {"nombre": "Bono Protección Beneficiarios 2020", "resource_id": "ddb40b83-f5fd-476a-b5bf-f66e556122fe"},
    2019: {"nombre": "Bono Protección Beneficiarios 2019", "resource_id": "3917217c-ac3d-4ecb-9e6d-a2ecb49a2ea8"}
}

url_base = "https://datos.gob.cl/api/3/action/datastore_search"
df_total = pd.DataFrame()
registros_por_año = {}

print(" Iniciando descarga optimizada (2019-2023)...\n" + "="*60)

for año, info in recursos.items():
    print(f"\n Descargando: {info['nombre']} ({año})")
    offset = 0
    limite = 20000
    records_año = []
    
    while True:
        params = {"resource_id": info["resource_id"], "limit": limite, "offset": offset, "sort": "_id asc"}
        try:
            response = requests.get(url_base, params=params, timeout=20)
            datos = response.json()
            
            if datos["success"]:
                records = datos['result']['records']
                if not records:
                    break  
                records_año.extend(records)
                offset += limite
                print(f"   -> Acumulados {len(records_año)} registros...")
                time.sleep(0.5)  
            else:
                print(f"    Error API en año {año}: {datos.get('error')}")
                break
        except Exception as e:
            print(f"    Error de conexión: {e}")
            break
            
    if records_año:
        df_temp = pd.DataFrame(records_año)
        df_temp['Año'] = año
        df_total = pd.concat([df_total, df_temp], ignore_index=True)
        registros_por_año[año] = len(df_temp)
    else:
        registros_por_año[año] = 0

if not df_total.empty:
    df_total.to_csv("datos_sociales_2019_2023.csv", index=False)
    print("\n" + "="*60 + f"\n💾 ¡Completado! Total: {len(df_total)} registros.")