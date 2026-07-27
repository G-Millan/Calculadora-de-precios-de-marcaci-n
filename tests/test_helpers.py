"""
Unit tests for helpers module.

Tests text processing and formatting functions.
"""

import pytest

from utils.helpers import (
    clean_text,
    format_currency,
    safe_float,
)


class TestCleanText:
    """Tests for text cleaning function."""

    def test_clean_text_with_accents(self):
        """Test that accents are removed."""
        result = clean_text("Número, técnica")
        assert result == "numero, tecnica"

    def test_clean_text_uppercase(self):
        """Test that uppercase is converted to lowercase."""
        result = clean_text("TECNICA")
        assert result == "tecnica"

    def test_clean_text_mixed(self):
        """Test with mixed accents and uppercase."""
        result = clean_text("TÉCNICA")
        assert result == "tecnica"

    def test_clean_text_none(self):
        """Test that None returns empty string."""
        result = clean_text(None)
        assert result == ""

    def test_clean_text_not_string(self):
        """Test that non-strings return empty string."""
        result = clean_text(123)
        assert result == ""


class TestFormatCurrency:
    """Tests for currency formatting."""

    def test_format_currency_basic(self):
        """Test basic currency formatting."""
        result = format_currency(85000)
        assert result == "$85,000"

    def test_format_currency_with_symbol(self):
        """Test with custom symbol."""
        result = format_currency(100, symbol="COP ")
        assert result == "COP 100"

    def test_format_currency_small(self):
        """Test with small amount."""
        result = format_currency(100.5)
        assert result == "$100" or result == "$101"  # Rounding


class TestSafeFloat:
    """Tests for safe float conversion."""

    def test_safe_float_valid_int(self):
        """Test converting valid integer."""
        result = safe_float(42)
        assert result == 42.0

    def test_safe_float_valid_string(self):
        """Test converting valid string."""
        result = safe_float("3.14")
        assert result == 3.14

    def test_safe_float_invalid_string(self):
        """Test that invalid string returns default."""
        result = safe_float("not a number")
        assert result == 0.0

    def test_safe_float_none(self):
        """Test that None returns default."""
        result = safe_float(None)
        assert result == 0.0

    def test_safe_float_custom_default(self):
        """Test with custom default value."""
        result = safe_float("invalid", default=-1.0)
        assert result == -1.0
