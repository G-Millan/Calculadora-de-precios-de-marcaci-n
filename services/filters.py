"""
Data filtering module.

Provides functions to filter pricing data based on user selections.
"""

from typing import List, Optional, Tuple

import pandas as pd

import config
from utils.helpers import clean_text
from utils.logger import logger


def filter_by_product(
    df: pd.DataFrame,
    product: str,
) -> pd.DataFrame:
    """
    Filter DataFrame by product type.

    Args:
        df: Complete pricing DataFrame
        product: Selected product name

    Returns:
        Filtered DataFrame containing only selected product
    """
    if df is None or df.empty:
        return pd.DataFrame()
    return df[df[config.COLUMN_PRODUCTO] == product]


def filter_by_technique(
    df: pd.DataFrame,
    technique: str,
) -> pd.DataFrame:
    """
    Filter DataFrame by marking technique.

    Args:
        df: Filtered DataFrame
        technique: Selected technique name

    Returns:
        Further filtered DataFrame
    """
    if df is None or df.empty:
        return pd.DataFrame()
    return df[df[config.COLUMN_TECNICA] == technique]


def filter_by_inks(
    df: pd.DataFrame,
    num_inks: Optional[int],
) -> pd.DataFrame:
    """
    Filter DataFrame by number of inks (if applicable).

    Args:
        df: Filtered DataFrame
        num_inks: Number of inks (None if not applicable)

    Returns:
        Further filtered DataFrame
    """
    if num_inks is None or df is None or df.empty:
        return df
    return df[df[config.COLUMN_TINTAS] == num_inks]


def filter_by_size(
    df: pd.DataFrame,
    size_from: Optional[float],
    size_to: Optional[float],
) -> pd.DataFrame:
    """
    Filter DataFrame by product size range.

    Args:
        df: Filtered DataFrame
        size_from: Size range start (cm)
        size_to: Size range end (cm)

    Returns:
        Further filtered DataFrame
    """
    if (
        size_from is None
        or size_to is None
        or df is None
        or df.empty
    ):
        return df

    return df[
        (df[config.COLUMN_TAMANO_DESDE] == size_from)
        & (df[config.COLUMN_TAMANO_HASTA] == size_to)
    ]


def apply_all_filters(
    df: pd.DataFrame,
    product: str,
    technique: str,
    num_inks: Optional[int] = None,
    size_from: Optional[float] = None,
    size_to: Optional[float] = None,
) -> pd.DataFrame:
    """
    Apply all filters sequentially to the DataFrame.

    This is the main filtering function that coordinates all individual filters.

    Args:
        df: Complete pricing DataFrame
        product: Selected product
        technique: Selected technique
        num_inks: Selected number of inks (optional)
        size_from: Size range start (optional)
        size_to: Size range end (optional)

    Returns:
        Filtered DataFrame with all conditions applied
    """
    logger.debug(
        f"Applying filters: product={product}, technique={technique}, "
        f"inks={num_inks}, size={size_from}-{size_to}"
    )

    result = df.copy()
    result = filter_by_product(result, product)
    result = filter_by_technique(result, technique)
    result = filter_by_inks(result, num_inks)
    result = filter_by_size(result, size_from, size_to)

    logger.debug(f"Filter result: {len(result)} rows")
    return result


def get_ink_options(
    df: pd.DataFrame,
    product: str,
    technique: str,
) -> List[int]:
    """
    Get available ink options for a product and technique combination.

    Args:
        df: Complete pricing DataFrame
        product: Selected product
        technique: Selected technique

    Returns:
        List of available ink counts
    """
    filtered = filter_by_product(df, product)
    filtered = filter_by_technique(filtered, technique)

    inks = (
        filtered[config.COLUMN_TINTAS]
        .dropna()
        .unique()
    )
    return sorted(inks)


def get_size_options(
    df: pd.DataFrame,
    product: str,
    technique: str,
) -> List[Tuple[float, float]]:
    """
    Get available size ranges for a product and technique combination.

    Args:
        df: Complete pricing DataFrame
        product: Selected product
        technique: Selected technique

    Returns:
        List of tuples (size_from, size_to)
    """
    filtered = filter_by_product(df, product)
    filtered = filter_by_technique(filtered, technique)

    sizes = filtered[
        [config.COLUMN_TAMANO_DESDE, config.COLUMN_TAMANO_HASTA]
    ].dropna().drop_duplicates()

    return [
        tuple(row)
        for row in sizes.itertuples(index=False)
    ]
