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

# Expander con ejemplos
with st.expander("📘 Ver ejemplos y descripciones de productos"):
    st.markdown("""
    | **Categoría** | **Descripción / Ejemplos de artículos** |
    | -------------- | --------------------------------------- |
    | **Bolígrafos plásticos** | Esferos o bolígrafos elaborados en plástico, con o sin clip metálico. Ejemplo: bolígrafo promocional básico, esfero retráctil. |
    | **Variedades** | Artículos pequeños o de uso variado, sin forma definida ni material predominante. Ejemplo: llaveros plásticos, broches, identificadores, destapadores simples, porta tapabocas, mini accesorios. |
    | **Variedades con tratamiento y antiestrés** | Artículos con superficie especial o textura, que se deforman o tienen mecanismos de presión. Ejemplo: pelotas antiestrés, figuras blandas, masajeadores, juguetes sensoriales. |
    | **Variedades metálicas** | Productos metálicos pequeños o medianos, con acabados en aluminio, acero o zamac. Ejemplo: llaveros metálicos, navajas, destapadores metálicos, herramientas mini, portanombres. |
    | **Cerámicas y siliconas** | Artículos de cerámica, vidrio grueso o silicona flexible. Ejemplo: tazas, mugs, portavasos, tapas de silicona, fundas, bandas o tapones reutilizables. |
    | **Paraguas / 1 casco** | Paraguas pequeños de un solo pliegue o tipo bastón corto. Ejemplo: paraguas compacto básico. |
    | **Paraguas / 2 casco** | Paraguas medianos con doble pliegue. Ejemplo: paraguas semi plegable de tamaño intermedio. |
    | **Paraguas / 4 casco** | Paraguas grandes de cuatro pliegues o tipo golf. Ejemplo: paraguas de gran cobertura o estructura reforzada. |
    | **Bolsas ecológicas plegables** | Bolsas reutilizables que se pueden doblar o guardar en un bolsillo interno. Ejemplo: bolsas de tela delgada tipo poliéster que se pliegan. |
    | **Bolsas ecológicas no plegables hasta 8 cm × 8 cm (media carta)** | Bolsas pequeñas de materiales ecológicos o rígidos. Ejemplo: bolsas de yute o algodón de tamaño reducido. |
    | **No plegables desde 8 cm × 8 cm (carta)** | Bolsas medianas o grandes no plegables. Ejemplo: bolsas de yute o algodón tamaño carta o superior. |
    | **Algodón, yute, metalizado media carta** | Bolsas o productos textiles de materiales naturales o brillantes, tamaño pequeño. Ejemplo: bolsas o estuches de algodón, yute o material metalizado pequeños. |
    | **Material poliéster** | Productos textiles sintéticos de poliéster. Ejemplo: estuches, portacosméticos, tulas o accesorios en tela sintética. |
    | **Algodón, yute, metalizado carta** | Bolsas o artículos textiles naturales o metalizados de tamaño estándar. Ejemplo: bolsas de algodón tamaño carta, empaques ecológicos medianos. |
    | **Producto cilíndrico** | Artículos con forma tubular o redonda, generalmente plásticos. Ejemplo: botellas plásticas, termos, cilindros deportivos. |
    | **Producto cilíndrico metálico** | Cilindros metálicos de acero o aluminio. Ejemplo: termos metálicos, botellas de aluminio, vasos térmicos. |
    | **Producto cilíndrico vidrio uniformado** | Botellas o vasos de vidrio con superficie lisa, sin relieves. Ejemplo: botellas de vidrio transparente, cilindros de vidrio esmerilado. |
    | **Productos planos** | Superficies lisas y planas, ideales para impresión directa o tampografía. Ejemplo: libretas, portadocumentos, tapas, cajas o estuches rectangulares. |
    | **Silicona sin accesorios plásticos mayor a 3 cm** | Artículos de silicona pura (sin piezas plásticas), de tamaño medio o grande. Ejemplo: pulseras de silicona, bandas, tapas o bases de silicona. |
    | **Silicona desensamble y ensamble** | Artículos que deben desarmarse para su marcación y luego volver a ensamblarse. Ejemplo: fundas de silicona con accesorios, productos compuestos. |
    | **Láser fibra artículo pequeño** | Artículos metálicos pequeños adecuados para marcación con láser fibra. Ejemplo: llaveros, bolígrafos metálicos, chapas pequeñas. |
    | **Láser fibra artículo grande** | Artículos metálicos grandes o de superficie amplia. Ejemplo: termos, placas, portanombres, herramientas. |
    | **Láser CO₂** | Artículos de madera, cuero, acrílico o vidrio que requieren grabado con láser CO₂. Ejemplo: cajas de madera, tapas acrílicas, trofeos, bases de vidrio. |
    | **Memorias, tarjetas, USB blancas** | Dispositivos electrónicos con superficies lisas o plásticas. Ejemplo: memorias USB, tarjetas USB, pendrives. |
    | **Pop socket** | Soportes plegables para celulares tipo “pop socket”. Ejemplo: pop socket plástico, metálico o con impresión UV. |
    | **Gorras** | Gorras de tela o poliéster, con o sin malla. Ejemplo: gorras tipo trucker, deportivas o promocionales. |
    | **Maletas** | Artículos de carga o transporte grandes. Ejemplo: mochilas, maletines, morrales, estuches grandes. |
    | **Camisetas y tulas media carta** | Textiles medianos o pequeños. Ejemplo: camisetas infantiles o tulas pequeñas. |
    | **Camisetas y tulas carta** | Textiles estándar o grandes. Ejemplo: camisetas para adultos, tulas deportivas. |
    | **Plásticos, vidrios, metal, etc. (7×7)** | Artículos pequeños de superficie plana (7 × 7 cm aprox.). Ejemplo: placas pequeñas, portanombres, bases cuadradas. |
    | **Plásticos, vidrios, metal, etc. (20×7)** | Artículos medianos o alargados de superficie plana. Ejemplo: placas rectangulares, tapas, portarretratos. |
    | **Marca en cristalería** | Artículos de vidrio fino o decorativo. Ejemplo: copas, vasos, jarras, trofeos de cristal. |
    """, unsafe_allow_html=True)

# Cargar base
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

# Calcular al presionar botón
if st.button("Calcular precio"):
    resultado, tipo = calcular_precio(filtro, cantidad)
    if resultado is None:
        st.error(tipo)
    else:
        valor_total = resultado
        valor_unitario = valor_total / cantidad
        if tipo == "mínima":
            st.success(f"💰 Valor de la marcación (MÍNIMA): ${valor_total:,.0f}")
        else:
            st.success(f"💰 Valor total de la marcación: ${valor_total:,.0f}")
        st.markdown(f"🔹 **Valor unitario:** ${valor_unitario:,.0f}")
        st.info("⚠️ Este precio es NETO, no incluye IVA y puede variar según negociación.")


# Footer fijo alineado con el contenido
st.markdown(
    """
    <style>
    .footer {
        position: fixed;
        bottom: 10px;
        left: 0;
        right: 0;
        max-width: 700px;
        margin: auto;
        text-align: center;
        font-size: 12px;
        color: #777;
    }
    </style>
    <div class="footer">Hecho con ❤️ por Germán Millán 🤓</div>
    """,
    unsafe_allow_html=True
)






