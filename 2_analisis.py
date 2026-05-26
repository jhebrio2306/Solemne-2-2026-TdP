import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("datos_sociales_2019_2023.csv")

print("ANÁLISIS DE DATOS SOCIALES - Bono de Protección / Ingreso Ético Familiar")
print("=" * 60)

print(f"\n Total de registros: {len(df)}")
print(f" Período: {df['Año'].min()} - {df['Año'].max()}")
print(f" Años disponibles: {sorted(df['Año'].unique())}")
print(f" Columnas: {list(df.columns)}")

print("\n" + "=" * 60)
print("BENEFICIARIOS POR AÑO")
print("=" * 60)

beneficiarios_por_año = df.groupby('Año').size()
for año, count in beneficiarios_por_año.items():
    print(f"   {año}: {count:,} registros")

# Gráfico de barras: Evolución anual
plt.figure(figsize=(10, 6))
beneficiarios_por_año.plot(kind='bar', color='#D62728', edgecolor='white')
plt.title('Evolución de Beneficiarios del Programa Social (2019-2023)', fontsize=14, pad=15)
plt.xlabel('Año', fontsize=12)
plt.ylabel('Número de Beneficiarios', fontsize=12)
plt.xticks(rotation=0)
plt.grid(axis='y', alpha=0.3)
for i, v in enumerate(beneficiarios_por_año.values):
    plt.text(i, v + 100, str(v), ha='center', fontsize=10, fontweight='bold')
plt.tight_layout()
plt.savefig('beneficiarios_por_año.png')
print("\n Gráfico guardado como 'beneficiarios_por_año.png'")

print("\n" + "=" * 60)
print("DISTRIBUCIÓN GEOGRÁFICA")
print("=" * 60)

columna_region = None
for col in df.columns:
    if 'region' in col.lower() or 'comuna' in col.lower():
        columna_region = col
        break

if columna_region:
    top_regiones = df[columna_region].value_counts().head(10)
    print(f"\nTop 10 {columna_region}:")
    for region, count in top_regiones.items():
        print(f"   {region}: {count:,}")
    
    plt.figure(figsize=(12, 6))
    top_regiones.sort_values().plot(kind='barh', color='#2CA02C', edgecolor='white')
    plt.title(f'Top 10 {columna_region} con más beneficiarios', fontsize=14, pad=15)
    plt.xlabel('Número de Beneficiarios', fontsize=12)
    plt.ylabel('') 
    
    plt.tight_layout()
    plt.savefig('beneficiarios_por_region.png')
    print("\n Gráfico guardado como 'beneficiarios_por_region.png'")
else:
    print("No se encontró columna de región en los datos")

print("\n" + "=" * 60)
print("COMPARATIVA POR MES (último año)")
print("=" * 60)

columna_fecha = None
for col in df.columns:
    if 'fecha' in col.lower() or 'date' in col.lower():
        columna_fecha = col
        break

if columna_fecha:
    df[columna_fecha] = pd.to_datetime(df[columna_fecha], errors='coerce')
    df_ultimo_año = df[df['Año'] == df['Año'].max()].copy()
    
    if not df_ultimo_año.empty:
        df_ultimo_año['Mes'] = df_ultimo_año[columna_fecha].dt.month
        beneficiarios_mes = df_ultimo_año.groupby('Mes').size()
        meses_nombres = ['Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun', 'Jul', 'Ago', 'Sep', 'Oct', 'Nov', 'Dic']
        
        plt.figure(figsize=(12, 5))
        plt.plot(range(1, 13), [beneficiarios_mes.get(m, 0) for m in range(1, 13)], 
                marker='o', linewidth=2, markersize=8, color='#1F77B4')
        plt.fill_between(range(1, 13), [beneficiarios_mes.get(m, 0) for m in range(1, 13)], 0, alpha=0.2)
        plt.xticks(range(1, 13), meses_nombres)
        plt.title(f'Beneficiarios por Mes - {df["Año"].max()}', fontsize=14, pad=15)
        plt.xlabel('Mes', fontsize=12)
        plt.ylabel('Número de Beneficiarios', fontsize=12)
        plt.grid(axis='y', alpha=0.3)
        plt.tight_layout()
        plt.savefig('beneficiarios_por_mes.png')
        print(f"\n Gráfico guardado como 'beneficiarios_por_mes.png'")
else:
    print("No se encontró columna de fecha en los datos")

print("\n" + "=" * 60)
print("Análisis completado")