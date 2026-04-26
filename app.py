"""
╔══════════════════════════════════════════════════════════════════╗
║        ImportAR - Herramienta de Investigación de Productos      ║
║        para Importación a Argentina                              ║
╚══════════════════════════════════════════════════════════════════╝

INSTRUCCIONES DE EJECUCIÓN LOCAL:
──────────────────────────────────
1. Instalar dependencias:
   pip install streamlit pandas

2. Ejecutar la app:
   streamlit run app.py

3. Abrir en el navegador: http://localhost:8501

DESPLIEGUE GRATUITO EN STREAMLIT CLOUD:
──────────────────────────────────────
1. Subir este archivo a un repositorio de GitHub (público o privado).
2. Crear un archivo requirements.txt con:
      streamlit
      pandas
3. Ir a https://share.streamlit.io → "New app"
4. Conectar tu repositorio de GitHub y seleccionar app.py
5. Click en "Deploy" → ¡listo! Obtienes una URL pública gratuita.

INTEGRACIÓN DE API REAL (FUTURO):
──────────────────────────────────
Busca los comentarios con el tag [API_INTEGRATION] en el código
para saber exactamente dónde y cómo conectar SerpApi, ScraperApi
u otras fuentes de datos reales.
"""

import streamlit as st
import pandas as pd
import random
import os
import json
from datetime import datetime

# ─────────────────────────────────────────────
#  CONFIGURACIÓN GLOBAL DE LA PÁGINA
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="ImportAR Pro",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────
#  CSS PERSONALIZADO
# ─────────────────────────────────────────────
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Space+Mono:wght@400;700&family=DM+Sans:wght@300;400;500;700&display=swap');

    html, body, [class*="css"] {
        font-family: 'DM Sans', sans-serif;
    }

    .main-header {
        background: linear-gradient(135deg, #0f0c29, #302b63, #24243e);
        padding: 2rem 2.5rem;
        border-radius: 16px;
        margin-bottom: 2rem;
        border: 1px solid rgba(255,255,255,0.08);
    }
    .main-header h1 {
        font-family: 'Space Mono', monospace;
        color: #fff;
        font-size: 2.2rem;
        margin: 0;
        letter-spacing: -1px;
    }
    .main-header p {
        color: rgba(255,255,255,0.6);
        margin: 0.3rem 0 0 0;
        font-size: 0.95rem;
    }
    .badge {
        display: inline-block;
        background: #6c63ff;
        color: white;
        font-size: 0.7rem;
        font-family: 'Space Mono', monospace;
        padding: 3px 10px;
        border-radius: 20px;
        margin-right: 6px;
        letter-spacing: 1px;
        text-transform: uppercase;
    }

    .winner-card {
        background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
        border: 1px solid rgba(108, 99, 255, 0.3);
        border-radius: 14px;
        padding: 1.5rem;
        margin-bottom: 1.2rem;
        position: relative;
        overflow: hidden;
    }
    .winner-card::before {
        content: '';
        position: absolute;
        top: 0; left: 0; right: 0;
        height: 3px;
        background: linear-gradient(90deg, #6c63ff, #f72585);
    }
    .winner-card h3 {
        color: #fff;
        margin: 0 0 0.5rem 0;
        font-size: 1.05rem;
        font-weight: 600;
    }
    .rank-badge {
        font-family: 'Space Mono', monospace;
        background: linear-gradient(135deg, #6c63ff, #f72585);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 2rem;
        font-weight: 700;
        float: right;
        margin-top: -0.3rem;
    }
    .metric-row {
        display: flex;
        gap: 1rem;
        flex-wrap: wrap;
        margin: 1rem 0;
    }
    .metric-box {
        background: rgba(255,255,255,0.05);
        border-radius: 8px;
        padding: 0.6rem 1rem;
        flex: 1;
        min-width: 130px;
    }
    .metric-box .label {
        font-size: 0.7rem;
        color: rgba(255,255,255,0.45);
        text-transform: uppercase;
        letter-spacing: 1px;
        font-family: 'Space Mono', monospace;
    }
    .metric-box .value {
        font-size: 1.1rem;
        font-weight: 700;
        color: #fff;
        margin-top: 0.15rem;
    }
    .metric-box .value.green { color: #4ade80; }
    .metric-box .value.yellow { color: #facc15; }
    .metric-box .value.blue { color: #60a5fa; }

    .justification-box {
        background: rgba(108,99,255,0.08);
        border-left: 3px solid #6c63ff;
        border-radius: 0 8px 8px 0;
        padding: 0.8rem 1rem;
        margin-top: 0.8rem;
    }
    .justification-box p {
        color: rgba(255,255,255,0.7);
        margin: 0;
        font-size: 0.88rem;
        line-height: 1.5;
    }
    .justification-box .emoji { font-size: 1rem; margin-right: 4px; }

    .saved-badge {
        background: #4ade80;
        color: #052e16;
        font-size: 0.75rem;
        font-weight: 700;
        padding: 3px 10px;
        border-radius: 20px;
        font-family: 'Space Mono', monospace;
    }

    .section-title {
        font-family: 'Space Mono', monospace;
        color: rgba(255,255,255,0.9);
        font-size: 1rem;
        letter-spacing: 2px;
        text-transform: uppercase;
        margin: 2rem 0 1rem 0;
        padding-bottom: 0.5rem;
        border-bottom: 1px solid rgba(255,255,255,0.08);
    }

    /* Sidebar styling */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0f0c29 0%, #1a1a2e 100%);
    }
    [data-testid="stSidebar"] .stSelectbox label,
    [data-testid="stSidebar"] .stNumberInput label,
    [data-testid="stSidebar"] .stTextInput label,
    [data-testid="stSidebar"] label {
        color: rgba(255,255,255,0.7) !important;
        font-size: 0.85rem !important;
    }
    [data-testid="stSidebar"] h2, [data-testid="stSidebar"] h3 {
        color: white !important;
    }

    .stButton > button {
        background: linear-gradient(135deg, #6c63ff, #f72585);
        color: white;
        border: none;
        border-radius: 8px;
        font-family: 'DM Sans', sans-serif;
        font-weight: 600;
        font-size: 0.9rem;
        padding: 0.5rem 1.2rem;
        transition: opacity 0.2s;
    }
    .stButton > button:hover {
        opacity: 0.85;
    }

    div[data-testid="stDataFrame"] {
        border-radius: 10px;
        overflow: hidden;
    }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
#  CONSTANTES Y DATOS SIMULADOS
# ─────────────────────────────────────────────

CSV_PATH = "mis_productos.csv"

# Base de datos simulada de productos
# [API_INTEGRATION] → Reemplazar PRODUCTS_DB con una llamada real a:
#   - Alibaba API: https://portals.alibaba.com/portals/buy/portals.htm
#   - SerpApi (Google Shopping): https://serpapi.com/google-shopping-api
#   - ScraperApi: https://www.scraperapi.com/
#   - Ejemplo con SerpApi:
#
#   import requests
#   def fetch_products_serpapi(query, source="alibaba"):
#       params = {
#           "engine": "google_shopping",
#           "q": f"{query} site:{source}.com",
#           "api_key": st.secrets["SERPAPI_KEY"],  # guardar en .streamlit/secrets.toml
#           "gl": "cn",
#           "hl": "en",
#       }
#       r = requests.get("https://serpapi.com/search.json", params=params)
#       return r.json().get("shopping_results", [])

PRODUCTS_DB = {
    "Alibaba": [
        {
            "nombre": "Mini Proyector LED Portátil 4K",
            "categoria": "Electrónica",
            "precio_origen_usd": 28.5,
            "precio_ml_usd": 190,
            "ventas_mensuales": 8400,
            "tendencia": "alta",
            "link": "https://www.alibaba.com/product-detail/mini-led-projector_4K.html",
            "demanda": "Alta",
            "estacionalidad": "Todo el año, pico en diciembre",
        },
        {
            "nombre": "Auriculares Bluetooth TWS Premium",
            "categoria": "Electrónica",
            "precio_origen_usd": 8.2,
            "precio_ml_usd": 75,
            "ventas_mensuales": 15200,
            "tendencia": "muy alta",
            "link": "https://www.alibaba.com/product-detail/tws-bluetooth-earbuds.html",
            "demanda": "Muy Alta",
            "estacionalidad": "Todo el año",
        },
        {
            "nombre": "Cargador GaN 65W 4 Puertos",
            "categoria": "Electrónica",
            "precio_origen_usd": 12.0,
            "precio_ml_usd": 95,
            "ventas_mensuales": 6300,
            "tendencia": "alta",
            "link": "https://www.alibaba.com/product-detail/gan-charger-65w.html",
            "demanda": "Alta",
            "estacionalidad": "Pico en regreso a clases",
        },
        {
            "nombre": "Soporte Ergonómico Laptop + Hub",
            "categoria": "Oficina",
            "precio_origen_usd": 18.0,
            "precio_ml_usd": 130,
            "ventas_mensuales": 4100,
            "tendencia": "media",
            "link": "https://www.alibaba.com/product-detail/laptop-stand-hub.html",
            "demanda": "Media",
            "estacionalidad": "Pico Q1 (vuelta oficina)",
        },
        {
            "nombre": "Luz LED Ring 26cm con Trípode",
            "categoria": "Fotografía",
            "precio_origen_usd": 14.5,
            "precio_ml_usd": 110,
            "ventas_mensuales": 9800,
            "tendencia": "muy alta",
            "link": "https://www.alibaba.com/product-detail/ring-light-26cm-tripod.html",
            "demanda": "Muy Alta",
            "estacionalidad": "Todo el año, creadores de contenido",
        },
        {
            "nombre": "Teclado Mecánico RGB Compacto 65%",
            "categoria": "Periféricos",
            "precio_origen_usd": 22.0,
            "precio_ml_usd": 160,
            "ventas_mensuales": 5500,
            "tendencia": "alta",
            "link": "https://www.alibaba.com/product-detail/mechanical-keyboard-rgb-65.html",
            "demanda": "Alta",
            "estacionalidad": "Pico gaming diciembre",
        },
        {
            "nombre": "Smartwatch Fitness Band GPS",
            "categoria": "Wearables",
            "precio_origen_usd": 19.0,
            "precio_ml_usd": 145,
            "ventas_mensuales": 7200,
            "tendencia": "muy alta",
            "link": "https://www.alibaba.com/product-detail/smartwatch-fitness-gps.html",
            "demanda": "Muy Alta",
            "estacionalidad": "Pico enero (año nuevo fitness)",
        },
    ],
    "AliExpress": [
        {
            "nombre": "Fundas iPhone 15 Premium Magsafe",
            "categoria": "Accesorios Móvil",
            "precio_origen_usd": 4.5,
            "precio_ml_usd": 40,
            "ventas_mensuales": 22000,
            "tendencia": "muy alta",
            "link": "https://www.aliexpress.com/item/iphone15-magsafe-case.html",
            "demanda": "Muy Alta",
            "estacionalidad": "Todo el año, pico lanzamientos",
        },
        {
            "nombre": "Cable USB-C 240W Trenzado 2m",
            "categoria": "Accesorios",
            "precio_origen_usd": 3.2,
            "precio_ml_usd": 28,
            "ventas_mensuales": 31000,
            "tendencia": "alta",
            "link": "https://www.aliexpress.com/item/usb-c-240w-braided-cable.html",
            "demanda": "Alta",
            "estacionalidad": "Todo el año",
        },
        {
            "nombre": "Mini Drone con Cámara 4K Plegable",
            "categoria": "Drones",
            "precio_origen_usd": 45.0,
            "precio_ml_usd": 340,
            "ventas_mensuales": 3800,
            "tendencia": "alta",
            "link": "https://www.aliexpress.com/item/mini-drone-4k-foldable.html",
            "demanda": "Alta",
            "estacionalidad": "Pico diciembre y verano",
        },
        {
            "nombre": "Set Pinceles Maquillaje 15 piezas",
            "categoria": "Belleza",
            "precio_origen_usd": 6.8,
            "precio_ml_usd": 55,
            "ventas_mensuales": 18500,
            "tendencia": "alta",
            "link": "https://www.aliexpress.com/item/makeup-brushes-15pcs-set.html",
            "demanda": "Alta",
            "estacionalidad": "Todo el año",
        },
        {
            "nombre": "Organizador Escritorio Modular Bambú",
            "categoria": "Hogar",
            "precio_origen_usd": 11.0,
            "precio_ml_usd": 85,
            "ventas_mensuales": 5600,
            "tendencia": "media",
            "link": "https://www.aliexpress.com/item/bamboo-desk-organizer-modular.html",
            "demanda": "Media",
            "estacionalidad": "Pico mudanzas y oficina",
        },
        {
            "nombre": "Masajeador Facial Rodillo Jade + LED",
            "categoria": "Belleza",
            "precio_origen_usd": 9.5,
            "precio_ml_usd": 78,
            "ventas_mensuales": 12400,
            "tendencia": "muy alta",
            "link": "https://www.aliexpress.com/item/jade-roller-led-facial-massager.html",
            "demanda": "Muy Alta",
            "estacionalidad": "Todo el año",
        },
        {
            "nombre": "Bolsa Térmica Almuerzo Impermeable",
            "categoria": "Hogar",
            "precio_origen_usd": 7.0,
            "precio_ml_usd": 52,
            "ventas_mensuales": 9200,
            "tendencia": "alta",
            "link": "https://www.aliexpress.com/item/waterproof-lunch-bag-thermal.html",
            "demanda": "Alta",
            "estacionalidad": "Pico vuelta al trabajo/escuela",
        },
    ],
}

# ─────────────────────────────────────────────
#  FUNCIONES DE NEGOCIO
# ─────────────────────────────────────────────

def calcular_landed_cost(precio_usd: float, dolar_mep: float, imp_aduaneros_pct: float, costo_envio_usd: float) -> dict:
    """
    Calcula el costo total 'landed' de un producto importado a Argentina.

    Fórmula:
        precio_con_envio = precio_usd + costo_envio_usd
        impuestos = precio_con_envio * (imp_aduaneros_pct / 100)
        costo_landed_usd = precio_con_envio + impuestos
        costo_landed_ars = costo_landed_usd * dolar_mep
    """
    precio_con_envio = precio_usd + costo_envio_usd
    impuestos = precio_con_envio * (imp_aduaneros_pct / 100)
    costo_landed_usd = precio_con_envio + impuestos
    costo_landed_ars = costo_landed_usd * dolar_mep
    return {
        "precio_con_envio_usd": precio_con_envio,
        "impuestos_usd": impuestos,
        "costo_landed_usd": costo_landed_usd,
        "costo_landed_ars": costo_landed_ars,
    }


def calcular_margen(precio_venta_ml_usd: float, dolar_mep: float, costo_landed_ars: float) -> dict:
    """
    Calcula el margen potencial de ganancia.

    El precio de ML se estima en base al precio USD de referencia * dolar_mep,
    con una variación de mercado simulada de ±15%.

    [API_INTEGRATION] → El campo precio_ml_ars debería obtenerse de:
        - MercadoLibre API oficial: https://developers.mercadolibre.com.ar/
        - Endpoint: GET https://api.mercadolibre.com/sites/MLA/search?q={producto}
        - Ejemplo:
            import requests
            def get_ml_price(query):
                r = requests.get(
                    "https://api.mercadolibre.com/sites/MLA/search",
                    params={"q": query, "limit": 5}
                )
                items = r.json().get("results", [])
                prices = [i["price"] for i in items if i.get("price")]
                return sum(prices) / len(prices) if prices else 0
    """
    # Simulación de precio de ML con variación de mercado
    variacion_mercado = random.uniform(0.90, 1.20)
    precio_ml_ars = precio_venta_ml_usd * dolar_mep * variacion_mercado

    ganancia_ars = precio_ml_ars - costo_landed_ars
    margen_pct = (ganancia_ars / precio_ml_ars * 100) if precio_ml_ars > 0 else 0

    return {
        "precio_ml_ars": precio_ml_ars,
        "ganancia_ars": ganancia_ars,
        "margen_pct": margen_pct,
    }


def generar_justificacion(producto: dict, margen_pct: float, ganancia_ars: float, dolar_mep: float) -> str:
    """
    Genera una justificación de por qué el producto es 'ganador'
    basada en datos de margen, demanda y estacionalidad.
    """
    partes = []

    # Análisis de brecha de precio
    ratio = producto["precio_ml_usd"] / producto["precio_origen_usd"]
    if ratio >= 6:
        partes.append(f"💰 **Brecha de precio extraordinaria**: el precio en ML es {ratio:.1f}x el costo de origen, generando una ganancia bruta de ${ganancia_ars:,.0f} ARS por unidad.")
    elif ratio >= 4:
        partes.append(f"💰 **Excelente brecha de precio**: relación {ratio:.1f}x entre precio ML y costo origen, con margen neto del {margen_pct:.0f}%.")
    else:
        partes.append(f"📊 **Margen sólido del {margen_pct:.0f}%** con una relación precio {ratio:.1f}x entre ML y el costo de origen.")

    # Análisis de demanda
    if producto["demanda"] == "Muy Alta":
        partes.append(f"🔥 **Demanda muy alta**: ~{producto['ventas_mensuales']:,} unidades vendidas mensualmente en la plataforma, lo que reduce el riesgo de stock inmovilizado.")
    elif producto["demanda"] == "Alta":
        partes.append(f"📈 **Demanda alta y sostenida**: {producto['ventas_mensuales']:,} ventas/mes, indicador de mercado maduro y predecible.")
    else:
        partes.append(f"📊 **Demanda media**: {producto['ventas_mensuales']:,} ventas/mes. Nicho con menor competencia y mayor diferenciación posible.")

    # Estacionalidad
    partes.append(f"📅 **Estacionalidad**: {producto['estacionalidad']}.")

    return " | ".join(partes)


def analizar_productos(fuente: str, dolar_mep: float, imp_aduaneros_pct: float, costo_envio_usd: float) -> pd.DataFrame:
    """
    Función principal de análisis. Toma los productos de la fuente seleccionada,
    calcula costos landed y márgenes, y retorna el Top 5 ordenado por margen.

    [API_INTEGRATION] → Aquí se deben reemplazar los datos de PRODUCTS_DB con
    llamadas reales a las APIs de Alibaba/AliExpress y MercadoLibre.
    El flujo sería:
        1. Llamar a SerpApi/ScraperApi para obtener productos trending de Alibaba/AliExpress
        2. Para cada producto, buscar su equivalente en ML con la API oficial
        3. Calcular los mismos KPIs con datos reales
    """
    productos_raw = PRODUCTS_DB.get(fuente, [])
    resultados = []

    for p in productos_raw:
        lc = calcular_landed_cost(p["precio_origen_usd"], dolar_mep, imp_aduaneros_pct, costo_envio_usd)
        mg = calcular_margen(p["precio_ml_usd"], dolar_mep, lc["costo_landed_ars"])

        resultados.append({
            "nombre": p["nombre"],
            "categoria": p["categoria"],
            "precio_origen_usd": p["precio_origen_usd"],
            "costo_landed_ars": lc["costo_landed_ars"],
            "precio_ml_ars": mg["precio_ml_ars"],
            "ganancia_ars": mg["ganancia_ars"],
            "margen_pct": mg["margen_pct"],
            "ventas_mensuales": p["ventas_mensuales"],
            "demanda": p["demanda"],
            "tendencia": p["tendencia"],
            "link": p["link"],
            "estacionalidad": p["estacionalidad"],
            "_raw": p,  # guardamos datos originales para justificación
        })

    df = pd.DataFrame(resultados)
    df = df[df["margen_pct"] > 0].sort_values("margen_pct", ascending=False).head(5).reset_index(drop=True)
    return df


def guardar_producto(producto_data: dict):
    """
    Guarda un producto en el archivo CSV local mis_productos.csv
    y en st.session_state para persistencia en sesión.
    """
    fila = {
        "fecha_guardado": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "nombre": producto_data["nombre"],
        "categoria": producto_data["categoria"],
        "precio_origen_usd": producto_data["precio_origen_usd"],
        "costo_landed_ars": round(producto_data["costo_landed_ars"], 2),
        "precio_ml_ars": round(producto_data["precio_ml_ars"], 2),
        "margen_pct": round(producto_data["margen_pct"], 1),
        "link": producto_data["link"],
    }

    # Persistencia en session_state (para UI)
    if "productos_guardados" not in st.session_state:
        st.session_state["productos_guardados"] = []

    nombres_guardados = [p["nombre"] for p in st.session_state["productos_guardados"]]
    if producto_data["nombre"] not in nombres_guardados:
        st.session_state["productos_guardados"].append(fila)

    # Persistencia en CSV local
    df_nuevo = pd.DataFrame([fila])
    if os.path.exists(CSV_PATH):
        df_existente = pd.read_csv(CSV_PATH)
        if producto_data["nombre"] not in df_existente["nombre"].values:
            df_resultado = pd.concat([df_existente, df_nuevo], ignore_index=True)
            df_resultado.to_csv(CSV_PATH, index=False)
    else:
        df_nuevo.to_csv(CSV_PATH, index=False)


def es_guardado(nombre: str) -> bool:
    """Verifica si un producto ya fue guardado en esta sesión."""
    if "productos_guardados" not in st.session_state:
        return False
    return any(p["nombre"] == nombre for p in st.session_state["productos_guardados"])


# ─────────────────────────────────────────────
#  INICIALIZACIÓN DE SESSION STATE
# ─────────────────────────────────────────────
if "productos_guardados" not in st.session_state:
    st.session_state["productos_guardados"] = []
if "resultados_df" not in st.session_state:
    st.session_state["resultados_df"] = None
if "analizado" not in st.session_state:
    st.session_state["analizado"] = False


# ─────────────────────────────────────────────
#  SIDEBAR
# ─────────────────────────────────────────────
with st.sidebar:
    st.markdown("## ⚙️ Configuración")
    st.markdown("---")

    st.markdown("### 🏪 Fuente de Productos")
    fuente = st.selectbox(
        "Plataforma de origen",
        options=["Alibaba", "AliExpress"],
        help="Alibaba: compras mayoristas B2B | AliExpress: compras minoristas, ideal para testear productos"
    )

    st.markdown("### 💱 Variables Económicas")
    dolar_mep = st.number_input(
        "💵 Dólar MEP (ARS/USD)",
        min_value=800.0,
        max_value=5000.0,
        value=1250.0,
        step=10.0,
        help="Tipo de cambio MEP (Bolsa). Consultá el valor actual en dolarito.ar o ambito.com"
    )

    imp_aduaneros_pct = st.number_input(
        "🏛️ Impuestos Aduaneros (%)",
        min_value=0.0,
        max_value=150.0,
        value=35.0,
        step=1.0,
        help="Incluye arancel externo + tasa estadística + IVA importación. Varía según posición arancelaria."
    )

    costo_envio_usd = st.number_input(
        "✈️ Costo de Envío por Producto (USD)",
        min_value=0.0,
        max_value=100.0,
        value=8.0,
        step=0.5,
        help="Costo estimado de flete internacional + última milla. Puede reducirse con volumen."
    )

    st.markdown("---")
    st.markdown("### 📂 Categoría (Próximamente)")
    st.selectbox(
        "Filtrar por categoría",
        ["Todas", "Electrónica", "Hogar", "Belleza", "Moda", "Deporte"],
        disabled=True,
    )

    st.markdown("---")
    # Botón principal de análisis
    analizar_btn = st.button("🚀 Analizar Oportunidades", use_container_width=True)

    st.markdown("""
    <div style='margin-top:1.5rem; font-size:0.75rem; color:rgba(255,255,255,0.3); text-align:center; font-family: Space Mono, monospace;'>
    ImportAR Pro v1.0<br>Datos simulados — integra tu API
    </div>
    """, unsafe_allow_html=True)


# ─────────────────────────────────────────────
#  CONTENIDO PRINCIPAL
# ─────────────────────────────────────────────
st.markdown("""
<div class="main-header">
    <span class="badge">Beta</span>
    <span class="badge">Datos Simulados</span>
    <h1>🚀 ImportAR Pro</h1>
    <p>Herramienta de investigación de productos para importación a Argentina · Calculá márgenes reales al instante</p>
</div>
""", unsafe_allow_html=True)

# Métricas de contexto rápidas
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("💵 Dólar MEP", f"${dolar_mep:,.0f}", help="Tipo de cambio configurado")
with col2:
    st.metric("🏛️ Impuestos Aduana", f"{imp_aduaneros_pct:.0f}%", help="% impuestos sobre costo + envío")
with col3:
    st.metric("✈️ Costo Envío", f"USD {costo_envio_usd:.1f}", help="Por unidad promedio")
with col4:
    st.metric("🏪 Fuente Activa", fuente)


# ─────────────────────────────────────────────
#  LÓGICA DE ANÁLISIS
# ─────────────────────────────────────────────
if analizar_btn:
    with st.spinner(f"Analizando productos en {fuente}..."):
        df = analizar_productos(fuente, dolar_mep, imp_aduaneros_pct, costo_envio_usd)
        st.session_state["resultados_df"] = df
        st.session_state["analizado"] = True
        st.session_state["fuente_analizada"] = fuente

# ─────────────────────────────────────────────
#  RESULTADOS
# ─────────────────────────────────────────────
if st.session_state["analizado"] and st.session_state["resultados_df"] is not None:
    df = st.session_state["resultados_df"]
    fuente_analizada = st.session_state.get("fuente_analizada", fuente)

    st.markdown(f"""
    <p class="section-title">🏆 Top 5 Productos Ganadores — {fuente_analizada}</p>
    """, unsafe_allow_html=True)

    # ── Tabla resumen interactiva
    with st.expander("📊 Ver tabla resumen completa", expanded=False):
        tabla = df[[
            "nombre", "categoria", "precio_origen_usd",
            "costo_landed_ars", "precio_ml_ars", "ganancia_ars",
            "margen_pct", "demanda"
        ]].copy()
        tabla.columns = [
            "Producto", "Categoría", "Precio Origen (USD)",
            "Costo Landed (ARS)", "Precio ML Est. (ARS)",
            "Ganancia Bruta (ARS)", "Margen (%)", "Demanda"
        ]
        tabla["Precio Origen (USD)"] = tabla["Precio Origen (USD)"].apply(lambda x: f"${x:.2f}")
        tabla["Costo Landed (ARS)"] = tabla["Costo Landed (ARS)"].apply(lambda x: f"${x:,.0f}")
        tabla["Precio ML Est. (ARS)"] = tabla["Precio ML Est. (ARS)"].apply(lambda x: f"${x:,.0f}")
        tabla["Ganancia Bruta (ARS)"] = tabla["Ganancia Bruta (ARS)"].apply(lambda x: f"${x:,.0f}")
        tabla["Margen (%)"] = tabla["Margen (%)"].apply(lambda x: f"{x:.1f}%")
        st.dataframe(tabla, use_container_width=True, hide_index=True)

    # ── Cards individuales con justificación y botón Guardar
    for idx, row in df.iterrows():
        rank = idx + 1
        guardado = es_guardado(row["nombre"])

        margen_color = "green" if row["margen_pct"] >= 40 else "yellow" if row["margen_pct"] >= 25 else "blue"

        st.markdown(f"""
        <div class="winner-card">
            <span class="rank-badge">#{rank}</span>
            <h3>{row['nombre']}</h3>
            <span style="font-size:0.8rem; color:rgba(255,255,255,0.4); font-family: Space Mono, monospace; text-transform:uppercase; letter-spacing:1px;">{row['categoria']}</span>

            <div class="metric-row">
                <div class="metric-box">
                    <div class="label">Precio Origen</div>
                    <div class="value blue">${row['precio_origen_usd']:.2f} USD</div>
                </div>
                <div class="metric-box">
                    <div class="label">Costo Landed</div>
                    <div class="value yellow">${row['costo_landed_ars']:,.0f} ARS</div>
                </div>
                <div class="metric-box">
                    <div class="label">Precio Est. ML</div>
                    <div class="value">${row['precio_ml_ars']:,.0f} ARS</div>
                </div>
                <div class="metric-box">
                    <div class="label">Ganancia Bruta</div>
                    <div class="value green">${row['ganancia_ars']:,.0f} ARS</div>
                </div>
                <div class="metric-box">
                    <div class="label">Margen Neto</div>
                    <div class="value {margen_color}">{row['margen_pct']:.1f}%</div>
                </div>
                <div class="metric-box">
                    <div class="label">Demanda</div>
                    <div class="value">{row['demanda']}</div>
                </div>
            </div>

            <div class="justification-box">
                <p>{generar_justificacion(row['_raw'], row['margen_pct'], row['ganancia_ars'], dolar_mep)}</p>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # Botones de acción (fuera del HTML para poder usar Streamlit)
        btn_col1, btn_col2, btn_col3 = st.columns([1, 1, 4])
        with btn_col1:
            if guardado:
                st.markdown('<span class="saved-badge">✓ GUARDADO</span>', unsafe_allow_html=True)
            else:
                if st.button(f"💾 Guardar Producto", key=f"guardar_{idx}"):
                    guardar_producto(row.to_dict())
                    st.success(f"✅ '{row['nombre']}' guardado en mis_productos.csv")
                    st.rerun()
        with btn_col2:
            st.link_button("🔗 Ver en origen", row["link"])


    # ─────────────────────────────────────────────
    #  SECCIÓN: PRODUCTOS GUARDADOS
    # ─────────────────────────────────────────────
    if st.session_state["productos_guardados"]:
        st.markdown("---")
        st.markdown('<p class="section-title">📂 Mis Productos Guardados</p>', unsafe_allow_html=True)

        df_guardados = pd.DataFrame(st.session_state["productos_guardados"])
        st.dataframe(df_guardados, use_container_width=True, hide_index=True)

        # Botón de descarga del CSV
        csv_data = df_guardados.to_csv(index=False).encode("utf-8")
        st.download_button(
            label="⬇️ Descargar mis_productos.csv",
            data=csv_data,
            file_name="mis_productos.csv",
            mime="text/csv",
        )

else:
    # Estado inicial — instrucciones
    st.markdown("---")
    col_a, col_b, col_c = st.columns(3)
    with col_a:
        st.markdown("""
        **1️⃣ Configurar variables**
        Ajustá el dólar MEP, impuestos y costo de envío en el panel lateral para reflejar tu situación real.
        """)
    with col_b:
        st.markdown("""
        **2️⃣ Seleccionar fuente**
        Elegí entre **Alibaba** (mayorista, grandes volúmenes) o **AliExpress** (minorista, ideal para testear).
        """)
    with col_c:
        st.markdown("""
        **3️⃣ Analizar oportunidades**
        Hacé click en **🚀 Analizar Oportunidades** para ver el Top 5 de productos con mayor margen potencial.
        """)

    st.info("""
    💡 **Tip para integrar datos reales**: Este MVP usa datos simulados. Para conectar fuentes reales, buscá los
    comentarios `[API_INTEGRATION]` en el código fuente. Podés usar **SerpApi**, **ScraperApi** o la
    **API oficial de MercadoLibre** para obtener precios en tiempo real.
    """)
