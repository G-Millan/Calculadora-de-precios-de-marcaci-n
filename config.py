"""
Configuration module for the Pricing Calculator application.

This module centralizes all configuration settings including file paths,
logging configuration, and application constants.
"""

import os
from pathlib import Path
from typing import Final

# ============================================================================
# PATHS
# ============================================================================

PROJECT_ROOT: Final[Path] = Path(__file__).parent
DATA_DIR: Final[Path] = PROJECT_ROOT / "data"
LOGS_DIR: Final[Path] = PROJECT_ROOT / "logs"
EXCEL_FILE: Final[Path] = DATA_DIR / "base_sima_precios.xlsx"

# Ensure directories exist
LOGS_DIR.mkdir(exist_ok=True)

# ============================================================================
# LOGGING CONFIGURATION
# ============================================================================

LOG_FILE: Final[Path] = LOGS_DIR / "app.log"
LOG_LEVEL: Final[str] = "INFO"
LOG_FORMAT: Final[str] = (
    "%(asctime)s - %(name)s - %(levelname)s - "
    "%(funcName)s:%(lineno)d - %(message)s"
)
LOG_DATE_FORMAT: Final[str] = "%Y-%m-%d %H:%M:%S"

# ============================================================================
# APPLICATION CONSTANTS
# ============================================================================

APP_NAME: Final[str] = "Calculadora de Precios de Marcación"
APP_ICON: Final[str] = "📦"
APP_VERSION: Final[str] = "2.0.0"
PAGE_TITLE: Final[str] = f"{APP_NAME} v{APP_VERSION}"

# Streamlit page configuration
STREAMLIT_CONFIG = {
    "page_title": PAGE_TITLE,
    "page_icon": APP_ICON,
    "layout": "wide",
    "initial_sidebar_state": "expanded",
}

# ============================================================================
# BUSINESS RULES
# ============================================================================

MIN_QUANTITY: Final[int] = 1
MAX_QUANTITY: Final[int] = 1_000_000
OBSERVACION_MINIMA: Final[str] = "minima"

# Excel column names (lowercase)
COLUMN_PRODUCTO: Final[str] = "producto"
COLUMN_TECNICA: Final[str] = "tecnica"
COLUMN_TINTAS: Final[str] = "numero de tintas"
COLUMN_TAMANO_DESDE: Final[str] = "tamaño producto desde cm"
COLUMN_TAMANO_HASTA: Final[str] = "tamaño producto hasta cm"
COLUMN_RANGO_DESDE: Final[str] = "rango cantidad desde"
COLUMN_RANGO_HASTA: Final[str] = "rango cantidad hasta"
COLUMN_PRECIO: Final[str] = "precio unitario"
COLUMN_OBSERVACIONES: Final[str] = "observaciones"

# ============================================================================
# UI CONSTANTS
# ============================================================================

# Colors (Streamlit color scheme)
COLOR_SUCCESS: Final[str] = "#0f8419"
COLOR_ERROR: Final[str] = "#ff2b2b"
COLOR_WARNING: Final[str] = "#ff9400"
COLOR_INFO: Final[str] = "#0099ff"

# Messages
MSG_NO_COMBINATION = "⚠️ No se encontró combinación válida."
MSG_NO_RANGE = "⚠️ No se encontró rango válido para esa cantidad."
MSG_QUANTITY_ERROR = "⚠️ Cantidad no válida."
MSG_PRICE_NET = "⚠️ Este precio es NETO, no incluye IVA y puede variar según negociación."
MSG_MINIMUM_PRICE = "mínima"

# Author
AUTHOR: Final[str] = "Germán Millán"
AUTHOR_EMAIL: Final[str] = "produccion@almadelascosas.com"
