import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import requests
import os
from datetime import datetime

st.set_page_config(page_title="Beneficios Sociales Chile", page_icon="🤝", layout="wide")

st.markdown("""
<style>
    .main-header {
        background: linear-gradient(135deg, #667eea, #764ba2);
        border-radius: 15px;
        padding: 2rem;
        margin-bottom: 2rem;
        text-align: center;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    }
    .main-header h1 { 
        font-size: 2.6rem !important; 
        font-weight: 800 !important; 
        color: white !important; 
        margin-bottom: 0.5rem !important;
    }
    .main-header p { 
        color: rgba(255,255,255,0.9) !important; 
        font-size: 1.1rem !important; 
        margin: 0 !important;
    }
    div[data-testid="stMetric"] {
        background-color: rgba(102, 126, 234, 0.08) !important;
        border: 1px solid rgba(102, 126, 234, 0.2) !important;
        padding: 1rem !important;
        border-radius: 12px !important;
    }
    .stTabs [data-baseweb="tab-list"] {
        padding-top: 0.5rem;
        padding-bottom: 0.5rem;
    }
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="main-header">
    <h1>🤝 Analizador de Beneficios Sociales</h1>
    <p>Ingreso Ético Familiar • Bono de Protección • datos.gob.cl</p>
</div>
""", unsafe_allow_html=True)

RECURSOS = {año: id for año, id in zip(range(2023, 2013, -1), 
    ["fed0c04a-3a39-4878-86d7-e9bb81d7061f", "876a675c-3d1b-4f0e-a481-128d288f9135",
     "9aaa497a-61a1-4cc7-a9dd-22128bbd56d7", "ddb40b83-f5fd-476a-b5bf-f66e556122fe",
     "3917217c-ac3d-4ecb-9e6d-a2ecb49a2ea8", "d4c92d3a-fc73-4987-b516-fa81eca74030",
     "3917217c-ac3d-4ecb-9e6d-a2ecb49a2ea8", "ddb40b83-f5fd-476a-b5bf-f66e556122fe",
     "9aaa497a-61a1-4cc7-a9dd-22128bbd56d7", "fed0c04a-3a39-4878-86d7-e9bb81d7061f"])}

COORDENADAS_REGIONES = {
    'Metropolitana de Santiago': {'lat': -33.4489, 'lon': -70.6693},
    'Santiago': {'lat': -33.4489, 'lon': -70.6693},
    'Valparaíso': {'lat': -33.0472, 'lon': -71.6127},
    'Bío Bío': {'lat': -36.8269, 'lon': -73.0498},
    'Biobío': {'lat': -36.8269, 'lon': -73.0498},
    'Maule': {'lat': -35.4264, 'lon': -71.6554},
    'La Araucanía': {'lat': -38.7359, 'lon': -72.5904},
    'Araucanía': {'lat': -38.7359, 'lon': -72.5904},
    'O\'Higgins': {'lat': -34.1708, 'lon': -70.7444},
    'Libertador B. O\'Higgins': {'lat': -34.1708, 'lon': -70.7444},
    'Coquimbo': {'lat': -29.9533, 'lon': -71.3395},
    'Antofagasta': {'lat': -23.6500, 'lon': -70.4000},
    'Los Lagos': {'lat': -41.4693, 'lon': -72.9424},
    'de los Lagos': {'lat': -41.4693, 'lon': -72.9424},
    'Los Ríos': {'lat': -39.8142, 'lon': -73.2459},
    'de los Ríos': {'lat': -39.8142, 'lon': -73.2459},
    'Tarapacá': {'lat': -20.2133, 'lon': -70.1500},
    'Atacama': {'lat': -27.3667, 'lon': -70.3333},
    'Arica y Parinacota': {'lat': -18.4746, 'lon': -70.2979},
    'Ñuble': {'lat': -36.6066, 'lon': -72.1034},
    'Aisén': {'lat': -45.5752, 'lon': -72.0662},
    'Aysén del G. Carlos Ibáñez del Campo': {'lat': -45.5752, 'lon': -72.0662},
    'Magallanes': {'lat': -53.1548, 'lon': -70.9089},
    'Magallanes y de la Antártica Chilena': {'lat': -53.1548, 'lon': -70.9089}
}

def descargar_datos(años):
    archivo = "datos_sociales.csv"
    if os.path.exists(archivo):
        df = pd.read_csv(archivo)
        if set(años).issubset(df['Año'].unique()):
            return df[df['Año'].isin(años)]
    df_total = pd.DataFrame()
    for año in años:
        try:
            r = requests.get(f"https://datos.gob.cl/api/3/action/datastore_search", 
                           params={"resource_id": RECURSOS[año], "limit": 10000})
            if r.json()["success"]:
                df = pd.DataFrame(r.json()["result"]["records"])
                df['Año'] = año
                df_total = pd.concat([df_total, df], ignore_index=True)
        except: pass
    if not df_total.empty:
        df_total.to_csv(archivo, index=False)
    return df_total

if "ejecutar_limpieza" in st.session_state:
    del st.session_state["ejecutar_limpieza"]
    if "años" in st.session_state:
        del st.session_state["años"]
    if "selector_años" in st.session_state:
        del st.session_state["selector_años"]
    st.rerun()

with st.sidebar:
    st.markdown("## Panel de Control")
    
    años = st.multiselect("Años disponibles", options=list(RECURSOS.keys()), 
                          key="selector_años", default=[], placeholder="Seleccionar años")
    
    if st.button("🚀 Cargar datos", use_container_width=True) and años:
        st.session_state['años'] = años
        st.rerun()
        
    if st.button("🗑️ Limpiar filtros", use_container_width=True):
        st.session_state["ejecutar_limpieza"] = True
        st.rerun()

if 'años' in st.session_state and st.session_state['años']:
    df = descargar_datos(st.session_state['años'])
    if df is None or df.empty:
        st.warning("No se pudieron cargar los datos")
        st.stop()

    col_region = next((c for c in df.columns if any(k in c.lower() for k in ['region', 'comuna', 'applicantregion'])), None)
    
    st.markdown("## Panorama General")
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Total Beneficiarios", f"{len(df):,}")
    c2.metric("Años Evaluados", df['Año'].nunique())
    c3.metric("Regiones / Zonas", df[col_region].nunique() if col_region else "N/A")
    c4.metric("Año Récord", df.groupby('Año').size().idxmax())
    
    st.markdown("---")
    st.markdown("## 📊 Visualización")
    
    tab1, tab2, tab3 = st.tabs(["📈 Evolución Anual", "🗺️ Mapa de Distribución", "📅 Análisis por Fecha"])
    
    with tab1:
        evol = df.groupby('Año').size()
        fig, ax = plt.subplots(figsize=(10, 4))
        ax.bar(evol.index.astype(str), evol.values, color='#667eea', edgecolor='white')
        ax.set_title("Beneficiarios por Año", fontsize=12, pad=10)
        ax.spines[['top','right']].set_visible(False)
        st.pyplot(fig)
        plt.close(fig)
    
    with tab2:
        if col_region:
            st.markdown("### 🗺️ Distribución Territorial de Beneficiarios")
            
            df_regiones = df[df[col_region].notna() & (df[col_region] != 'No disponible')]
            conteos = df_regiones[col_region].value_counts()
            
            mapa_data = []
            for name, count in conteos.items():
                clean_name = str(name).strip()
                if clean_name in COORDENADAS_REGIONES:
                    mapa_data.append({
                        'Región': clean_name,
                        'lat': COORDENADAS_REGIONES[clean_name]['lat'],
                        'lon': COORDENADAS_REGIONES[clean_name]['lon'],
                        'Beneficiarios': count
                    })
            
            df_mapa = pd.DataFrame(mapa_data)
            
            if not df_mapa.empty:
                col_map, col_tabla = st.columns([2, 1])
                
                with col_map:
                    st.info("Usa el scroll para hacer zoom y arrastra para desplazarte por Chile.")
              
                    FACTOR_ESCALA = 20  
                    
                    df_mapa_escalado = df_mapa.copy()
                    df_mapa_escalado['Beneficiarios_escalado'] = df_mapa_escalado['Beneficiarios'] * FACTOR_ESCALA
                    
                    st.map(df_mapa_escalado, 
                           latitude='lat', 
                           longitude='lon', 
                           size='Beneficiarios_escalado', 
                           color='#764ba2')
                    
                with col_tabla:
                    st.markdown("#### **Ranking por Región**")
                    df_ranking = df_mapa[['Región', 'Beneficiarios']].sort_values(by='Beneficiarios', ascending=False)
                    st.dataframe(df_ranking, hide_index=True, use_container_width=True)
            else:
                st.warning("Las regiones encontradas en el dataset no coinciden con el diccionario geográfico estándar.")
        else:
            st.info("No se encontró columna geográfica estructurada en el dataset.")
        
    
    with tab3:
        fecha_col = next((c for c in df.columns if 'fecha' in c.lower() or 'date' in c.lower()), None)
        
        if fecha_col:
            df['fecha_dt'] = pd.to_datetime(df[fecha_col], errors='coerce')
            fechas = df.dropna(subset=['fecha_dt']).copy()
            
            if not fechas.empty:
                ini = fechas['fecha_dt'].min().date()
                fin = fechas['fecha_dt'].max().date()
                
                st.markdown(f"### Rango disponible: {ini} a {fin}")
                
                col1, col2 = st.columns(2)
                with col1:
                    fecha_inicio = st.date_input("Fecha inicio", ini, min_value=ini, max_value=fin)
                with col2:
                    fecha_fin = st.date_input("Fecha fin", fin, min_value=ini, max_value=fin)
                
                if fecha_inicio > fecha_fin:
                    st.error("La fecha de inicio no puede ser mayor a la fecha de fin.")
                else:
                    mask = (fechas['fecha_dt'].dt.date >= fecha_inicio) & (fechas['fecha_dt'].dt.date <= fecha_fin)
                    filtro = fechas[mask]
                    
                    if not filtro.empty:
                        st.success(f"Mostrando {len(filtro):,} registros entre {fecha_inicio} y {fecha_fin}")
                        
                        dias_unicos = filtro['fecha_dt'].dt.date.nunique()
                        st.metric("Días con registros en el rango", dias_unicos)
                        
                        fig, ax = plt.subplots(figsize=(12, 4))
                        serie_diaria = filtro.groupby(filtro['fecha_dt'].dt.date).size()
                        
                        ax.plot(serie_diaria.index, serie_diaria.values, 
                               marker='o', linewidth=2, markersize=4, color='#764ba2')
                        ax.set_title("Evolución de Registros Diarios", fontsize=12, pad=10)
                        ax.set_xlabel("Fecha", fontsize=10)
                        ax.set_ylabel("N° de Registros", fontsize=10)
                        plt.xticks(rotation=45)
                        ax.spines[['top', 'right']].set_visible(False)
                        ax.grid(axis='y', alpha=0.3)
                        st.pyplot(fig)
                        plt.close(fig)
                    else:
                        st.warning("No hay registros en el rango de fechas seleccionado. Probá con un rango más amplio.")
            else:
                st.warning("No se pudieron convertir las fechas. Revisá el formato de la columna de fecha.")
        else:
            st.info("No se encontró una columna de fecha en el dataset. Algunos años pueden no incluir este dato.")
    
    with st.expander("Ver matriz de datos detallados"):
        st.dataframe(df.head(100), use_container_width=True)

else:
    st.info("Selecciona uno o más años en el panel izquierdo y haz clic en 'Cargar datos' para iniciar el análisis.")

st.markdown("---")
st.markdown('<div style="text-align: center; padding: 1rem; color: #888; font-size: 0.85rem;">🤝 Ingreso Ético Familiar • 🇨🇱 datos.gob.cl • 2014-2023</div>', unsafe_allow_html=True)