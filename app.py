"""
Calculadora de Precios de Marcación - Aplicación Principal

Una herramienta de Streamlit para calcular automáticamente el costo de marcación
de productos basada en una base de datos de reglas de precios en Excel.

Author: Germán Millán
Version: 2.0.0
"""

import streamlit as st

import config
from services.calculator import create_calculator
from services.data_loader import load_pricing_data
from services.filters import (
    apply_all_filters,
    get_ink_options,
    get_size_options,
    get_techniques_for_product,
)
from utils.helpers import format_currency
from utils.logger import logger
from utils.validators import validate_quantity


# ============================================================================
# PAGE CONFIGURATION
# ============================================================================


def setup_page_config():
    """Configure Streamlit page settings."""
    st.set_page_config(**config.STREAMLIT_CONFIG)


# ============================================================================
# UI COMPONENTS
# ============================================================================


def render_header():
    """Render application header with title and description."""
    col1, col2 = st.columns([1, 5])

    with col1:
        st.markdown(
            f"<div style='font-size: 48px; text-align: center;'>"
            f"{config.APP_ICON}</div>",
            unsafe_allow_html=True,
        )

    with col2:
        st.title(config.APP_NAME)
        st.markdown(
            """
            Calcula automáticamente el costo de marcación de productos
            basado en nuestras reglas de precios.
            """
        )


def render_product_examples():
    """Render expandable section with product categories and examples."""
    with st.expander("📘 Ver ejemplos y descripciones de productos"):
        st.markdown(
            """
            | **Categoría** | **Descripción / Ejemplos de artículos** |
            | -------------- | --------------------------------------- |
            | **Bolígrafos plásticos** | Esferos o bolígrafos elaborados en plástico, con o sin clip metálico. |
            | **Bolígrafos sin tratamiento** | Bolígrafos básicos sin acabados especiales. |
            | **Variedades** | Artículos pequeños sin forma definida. Ejemplo: llaveros, broches, identificadores. |
            | **Variedades con tratamiento** | Artículos con superficie especial. Ejemplo: pelotas antiestrés, figuras blandas. |
            | **Variedades metálicas** | Productos metálicos pequeños. Ejemplo: llaveros metálicos, destapadores. |
            | **Cerámicas y siliconas** | Cerámica, vidrio o silicona flexible. Ejemplo: tazas, mugs, fundas de silicona. |
            | **Paraguas** | Paraguas de diferentes tamaños y pliegues. |
            | **Bolsas ecológicas** | Bolsas reutilizables de materiales ecológicos. |
            | **Productos cilíndricos** | Botellas, termos, cilindros deportivos. |
            | **Productos planos** | Superficies lisas para impresión. Ejemplo: libretas, portadocumentos. |
            | **Láser fibra** | Artículos metálicos para grabado con láser fibra. |
            | **Láser CO₂** | Artículos de madera, cuero, acrílico para láser CO₂. |
            | **Textiles** | Camisetas, tulas, gorras, mochilas. |
            """
        )


def render_filters_form(df):
    """
    Render the input form for selecting product, technique, and quantity.

    Args:
        df: Pricing DataFrame

    Returns:
        dict with user selections
    """
    selections = {}

    # Product selection
    products = sorted(df[config.COLUMN_PRODUCTO].dropna().unique())
    selections["product"] = st.selectbox(
        "📦 Seleccione el producto:",
        options=products,
        key="product_select",
    )

    # Technique selection
    techniques = get_techniques_for_product(df, selections["product"])
    selections["technique"] = st.selectbox(
        "🎨 Seleccione la técnica:",
        options=techniques,
        key="technique_select",
    )

    # Inks selection (optional)
    inks = get_ink_options(df, selections["product"], selections["technique"])
    selections["inks"] = None
    if inks:
        selections["inks"] = st.selectbox(
            "🖨️ Seleccione el número de tintas:",
            options=inks,
            key="inks_select",
        )

    # Size selection (optional)
    sizes = get_size_options(df, selections["product"], selections["technique"])
    selections["size_from"] = None
    selections["size_to"] = None

    if sizes:
        size_options = [
            f"Desde {s[0]:.1f} cm hasta {s[1]:.1f} cm" for s in sizes
        ]
        size_index = st.selectbox(
            "📐 Seleccione el tamaño:",
            options=range(len(size_options)),
            format_func=lambda i: size_options[i],
            key="size_select",
        )
        selections["size_from"], selections["size_to"] = sizes[size_index]

    # Quantity input
    selections["quantity"] = st.number_input(
        "📊 Ingrese la cantidad de artículos a marcar:",
        min_value=config.MIN_QUANTITY,
        max_value=config.MAX_QUANTITY,
        step=1,
        value=config.MIN_QUANTITY,
        key="quantity_input",
    )

    return selections


def render_price_result(price, price_type, unit_price):
    """
    Render the price calculation results with formatting.

    Args:
        price: Total calculated price
        price_type: Type of price ('minima' or 'normal')
        unit_price: Unit price
    """
    # Format prices
    price_str = format_currency(price)
    unit_price_str = format_currency(unit_price)

    # Display results in columns
    col1, col2 = st.columns(2)

    with col1:
        if price_type == config.MSG_MINIMUM_PRICE:
            st.success(
                f"💰 **Valor de la marcación (MÍNIMA):** {price_str}"
            )
        else:
            st.success(f"💰 **Valor total de la marcación:** {price_str}")

    with col2:
        st.info(f"🔹 **Valor unitario:** {unit_price_str}")

    # Display disclaimer
    st.warning(config.MSG_PRICE_NET)


def render_footer():
    """Render application footer."""
    st.divider()
    col1, col2, col3 = st.columns(3)

    with col1:
        st.caption(f"**v{config.APP_VERSION}**")
    with col2:
        st.caption("Made with ❤️ by Germán Millán")
    with col3:
        st.caption(f"📧 {config.AUTHOR_EMAIL}")


# ============================================================================
# MAIN APPLICATION LOGIC
# ============================================================================


def main():
    """Main application entry point."""
    # Setup page configuration
    setup_page_config()

    try:
        # Load pricing data
        logger.info("Starting application")
        df = load_pricing_data()

        if df is None or df.empty:
            st.error(
                "❌ Error al cargar la base de datos de precios. "
                "Por favor, intente más tarde."
            )
            logger.error("Failed to load pricing data")
            return

        # Render header
        render_header()

        # Create tabs for organization
        tab1, tab2 = st.tabs(["🧮 Calculadora", "📚 Información"])

        with tab1:
            st.markdown("---")

            # Render product examples
            render_product_examples()

            st.markdown("---")

            # Create form
            st.subheader("⚙️ Configura tu búsqueda")

            with st.form(key="pricing_form", clear_on_submit=False):
                selections = render_filters_form(df)

                # Submit button
                submit_button = st.form_submit_button(
                    "🔍 Calcular precio",
                    use_container_width=True,
                    type="primary",
                )

            # Process form submission
            if submit_button:
                # Validate quantity
                is_valid, error_msg = validate_quantity(selections["quantity"])
                if not is_valid:
                    st.error(f"❌ {error_msg}")
                    return

                # Apply filters
                filtered_df = apply_all_filters(
                    df,
                    product=selections["product"],
                    technique=selections["technique"],
                    num_inks=selections["inks"],
                    size_from=selections["size_from"],
                    size_to=selections["size_to"],
                )

                # Calculate price
                calculator = create_calculator(df)
                price, price_type, message = calculator.calculate_price(
                    filtered_df,
                    selections["quantity"],
                )

                st.markdown("---")

                # Display results or error
                if price is None:
                    st.error(f"❌ {message}")
                else:
                    unit_price = calculator.get_unit_price(
                        price,
                        selections["quantity"],
                    )
                    st.markdown("### 📊 Resultados")
                    render_price_result(price, price_type, unit_price)

                    # Log successful calculation
                    logger.info(
                        f"Calculation completed: product={selections['product']}, "
                        f"technique={selections['technique']}, "
                        f"quantity={selections['quantity']}, "
                        f"price={price}"
                    )

        with tab2:
            st.markdown("## 📖 Acerca de esta aplicación")
            st.markdown(
                """
                ### 🎯 Propósito
                Esta aplicación automatiza el cálculo de precios de marcación,
                reemplazando la búsqueda manual en hojas de cálculo.

                ### 📊 Características
                - **Búsqueda Rápida**: Obtén precios en segundos
                - **Filtros Inteligentes**: Selecciona producto, técnica, tintas y tamaño
                - **Precios Actualizados**: Basado en la base de datos oficial
                - **Reglas de Negocio**: Considera precios mínimos y rangos de cantidad

                ### 💡 ¿Cómo usar?
                1. Selecciona el **tipo de producto** que deseas marcar
                2. Elige la **técnica** de marcación
                3. Especifica **tintas** y **tamaño** (si aplica)
                4. Ingresa la **cantidad** de artículos
                5. Haz clic en **Calcular precio**

                ### ⚠️ Nota importante
                Los precios mostrados son **NETO** y no incluyen IVA.
                Los valores pueden variar según negociación directa.

                ### 👨‍💼 Contacto
                Para consultas o reportar problemas:  
                📧 {config.AUTHOR_EMAIL}
                """
            )

        # Render footer
        render_footer()

    except Exception as e:
        logger.error(f"Unexpected application error: {type(e).__name__}: {e}")
        st.error(
            "❌ Ha ocurrido un error inesperado. "
            "Por favor, intente nuevamente."
        )


if __name__ == "__main__":
    main()
