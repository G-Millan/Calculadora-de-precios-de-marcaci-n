"""
Data validation module.

Provides validation functions for user inputs and data integrity checks.
"""

from typing import Tuple

import pandas as pd

import config
from utils.logger import logger


def validate_quantity(quantity: int) -> Tuple[bool, str]:
    """
    Validate that quantity is within acceptable range.

    Args:
        quantity: Number of items to mark

    Returns:
        Tuple[bool, str]: (is_valid, error_message)
    """
    if quantity < config.MIN_QUANTITY:
        msg = f"La cantidad debe ser mayor a {config.MIN_QUANTITY}."
        logger.warning(f"Invalid quantity: {quantity}")
        return False, msg

    if quantity > config.MAX_QUANTITY:
        msg = f"La cantidad no puede exceder {config.MAX_QUANTITY}."
        logger.warning(f"Quantity exceeds maximum: {quantity}")
        return False, msg

    return True, ""


def validate_dataframe(df: pd.DataFrame) -> Tuple[bool, str]:
    """
    Validate that the loaded Excel file has required columns.

    Args:
        df: DataFrame from Excel file

    Returns:
        Tuple[bool, str]: (is_valid, error_message)
    """
    if df is None or df.empty:
        msg = "La base de datos está vacía."
        logger.error("DataFrame is empty or None")
        return False, msg

    required_columns = {
        config.COLUMN_PRODUCTO,
        config.COLUMN_TECNICA,
        config.COLUMN_RANGO_DESDE,
        config.COLUMN_RANGO_HASTA,
        config.COLUMN_PRECIO,
    }

    missing_columns = required_columns - set(df.columns)
    if missing_columns:
        msg = f"Columnas faltantes en Excel: {', '.join(missing_columns)}"
        logger.error(f"Missing columns: {missing_columns}")
        return False, msg

    return True, ""


def validate_filter_result(
    filter_result: pd.DataFrame,
) -> Tuple[bool, str]:
    """
    Validate that filter returned valid results.

    Args:
        filter_result: Filtered DataFrame

    Returns:
        Tuple[bool, str]: (is_valid, error_message)
    """
    if filter_result.empty:
        msg = config.MSG_NO_COMBINATION
        logger.info("No valid combination found for filters")
        return False, msg

    return True, ""
