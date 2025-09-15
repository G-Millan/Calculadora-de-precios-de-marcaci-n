# app.py
import streamlit as st
import pandas as pd
import unicodedata
import os

# ----------------- Auxiliares -----------------
def limpiar_texto(texto):
    if not isinstance(texto, str):
        return ""
    texto = unicodedata.normalize("NFD", texto)
    texto = "".join(c for c in texto if unicodedata.category(c) != "Mn")
    return texto.lower()

def calcular_precio(filtro, cantidad):
    if filtro.empty:
        return None, "⚠️ No se encontró combinación válida."

    for _, fila in filtro.iterrows():
        rango_desde = float(fila["rango cantidad desde"])
        rango_hasta = float(fila["rango cantidad hasta"])
        precio_unitario = float(fila["precio unitario"])
        observacion = limpiar_texto(fila.get("observaciones", ""))

        if "minima" in observacion and rango_desde <= cantidad <= rango_hasta:
            return precio_unitario, "mínima"

        if rango_desde <= cantidad <= rango_hasta:
            return cantidad * precio_unitario, "normal"

    return None, "⚠️ No se encontró rango válido para esa cantidad."

# ----------------- Carga de datos -----------------
@st.cache_data
def cargar_datos():
    ruta_excel = os.path.join(os.path.dirname(__file__), "base_sima_precios.xlsx")
    df = pd.read_excel(ruta_excel, engine="openpyxl")
    df.rename(columns=lambda x: x.strip().lower(), inplace=True)
    return df

# ----------------- App -----------------
st.set_page_config(page_title="Calculadora SIMA", page_icon="📦", layout="centered")
st.title("📊 Calculadora de Precios de Marcación 🧮")

df = cargar_datos()

# Producto
producto = st.selectbox("Seleccione el producto:", df["producto"].unique())

# Técnica
tecnicas = df[df["producto"] == producto]["tecnica"].unique()
tecnica = st.selectbox("Seleccione la técnica:", tecnicas)

# Tintas (si aplica)
tinta = None
tintas = df[(df["producto"] == producto) & (df["tecnica"] == tecnica)]["numero de tintas"].dropna().unique()
if len(tintas) > 0:
    tinta = st.selectbox("Seleccione el número de tintas:", tintas)

# Tamaño (si aplica)
tamano_desde = tamano_hasta = None
tamanos = df[(df["producto"] == producto) & (df["tecnica"] == tecnica)][
    ["tamaño producto desde cm", "tamaño producto hasta cm"]
].dropna().drop_duplicates()

if not tamanos.empty:
    opciones = [f"Desde {fila[0]} cm hasta {fila[1]} cm" for fila in tamanos.itertuples(index=False)]
    seleccion = st.selectbox("Seleccione el tamaño:", opciones)
    idx = opciones.index(seleccion)
    tamano_desde, tamano_hasta = tamanos.iloc[idx]

# Cantidad
cantidad = st.number_input("Ingrese la cantidad de artículos a marcar:", min_value=1, step=1)

# Filtrar
filtro = df[(df["producto"] == producto) & (df["tecnica"] == tecnica)]
if tinta is not None:
    filtro = filtro[filtro["numero de tintas"] == tinta]
if tamano_desde is not None and tamano_hasta is not None:
    filtro = filtro[
        (filtro["tamaño producto desde cm"] == tamano_desde) &
        (filtro["tamaño producto hasta cm"] == tamano_hasta)
    ]

# Calcular
if st.button("Calcular precio"):
    resultado, tipo = calcular_precio(filtro, cantidad)
    if resultado is None:
        st.error(tipo)
    else:
        if tipo == "mínima":
            st.success(f"💰 Valor de la marcación (MÍNIMA): ${resultado:,.0f}")
        else:
            st.success(f"💰 Valor de la marcación: ${resultado:,.0f}")
        st.info("⚠️ Este precio es NETO, no incluye IVA y puede variar según negociación.")

# Footer fijo alineado con el contenido
st.markdown(
    """
    <style>
    .footer {
        position: fixed;
        bottom: 10px;        /* Distancia desde el borde inferior */
        left: 0;
        right: 0;
        max-width: 700px;    /* Ancho similar al contenedor central de Streamlit */
        margin: auto;        /* Centrado horizontal */
        text-align: center;
        font-size: 12px;
        color: #777;
    }
    </style>
    <div class="footer">Hecho con ❤️ por Germán Millán 🤓</div>
    """,
    unsafe_allow_html=True
)










