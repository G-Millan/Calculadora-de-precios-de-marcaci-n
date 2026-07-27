"""
Data loading module.

Handles reading and preprocessing the Excel pricing database.
"""

from typing import Optional

import pandas as pd
import streamlit as st

import config
from utils.logger import logger
from utils.validators import validate_dataframe


@st.cache_data(show_spinner=False)
def load_pricing_data() -> Optional[pd.DataFrame]:
    """
    Load and preprocess the pricing database from Excel.

    The data is cached automatically by Streamlit to improve performance.

    Returns:
        DataFrame with normalized column names or None if loading fails

    Raises:
        FileNotFoundError: If Excel file is not found
        ValueError: If Excel file is invalid
    """
    try:
        if not config.EXCEL_FILE.exists():
            logger.error(f"Excel file not found: {config.EXCEL_FILE}")
            return None

        logger.info(f"Loading data from {config.EXCEL_FILE}")
        df = pd.read_excel(config.EXCEL_FILE, engine="openpyxl")

        # Normalize column names: strip whitespace and convert to lowercase
        df.rename(columns=lambda x: x.strip().lower(), inplace=True)

        # Validate the loaded data
        is_valid, error_msg = validate_dataframe(df)
        if not is_valid:
            logger.error(f"Data validation failed: {error_msg}")
            return None

        logger.info(
            f"Successfully loaded {len(df)} rows and {len(df.columns)} "
            "columns from pricing database"
        )
        return df

    except FileNotFoundError as e:
        logger.error(f"Excel file not found: {e}")
        return None
    except Exception as e:
        logger.error(f"Unexpected error loading data: {type(e).__name__}: {e}")
        return None


def get_unique_products(df: pd.DataFrame) -> list:
    """
    Extract unique product types from the pricing database.

    Args:
        df: Pricing DataFrame

    Returns:
        Sorted list of unique products
    """
    if df is None or df.empty:
        return []
    return sorted(df[config.COLUMN_PRODUCTO].dropna().unique())


def get_techniques_for_product(
    df: pd.DataFrame,
    product: str,
) -> list:
    """
    Extract techniques available for a specific product.

    Args:
        df: Pricing DataFrame
        product: Product name

    Returns:
        Sorted list of unique techniques
    """
    if df is None or df.empty:
        return []
    filtered = df[df[config.COLUMN_PRODUCTO] == product]
    return sorted(filtered[config.COLUMN_TECNICA].dropna().unique())
