"""
Helper functions for text processing and data manipulation.

Provides utility functions for cleaning and transforming text data.
"""

import unicodedata
from typing import Any

import pandas as pd

import config


def clean_text(text: Any) -> str:
    """
    Normalize and clean text by removing accents and converting to lowercase.

    This function is useful for standardizing text comparisons across
    different input formats (with/without accents).

    Args:
        text: Input text (can be any type)

    Returns:
        Cleaned text in lowercase without accents
    """
    if not isinstance(text, str):
        return ""

    # NFD: Decompose characters into base + combining marks
    text = unicodedata.normalize("NFD", text)
    # Remove combining marks (accents, diacritics)
    text = "".join(c for c in text if unicodedata.category(c) != "Mn")
    return text.lower()


def format_currency(value: float, symbol: str = "$") -> str:
    """
    Format a numeric value as currency with thousands separator.

    Args:
        value: Numeric value to format
        symbol: Currency symbol (default: "$")

    Returns:
        Formatted currency string

    Example:
        >>> format_currency(85000)
        '$85,000'
    """
    return f"{symbol}{value:,.0f}"


def get_unique_sorted(series: pd.Series) -> list:
    """
    Get unique values from a pandas Series, sorted and cleaned.

    Args:
        series: Pandas Series

    Returns:
        List of unique, non-null values
    """
    return sorted(series.dropna().unique())


def safe_float(value: Any, default: float = 0.0) -> float:
    """
    Safely convert a value to float with fallback default.

    Args:
        value: Value to convert
        default: Default value if conversion fails

    Returns:
        Converted float or default value
    """
    try:
        return float(value)
    except (ValueError, TypeError):
        return default
