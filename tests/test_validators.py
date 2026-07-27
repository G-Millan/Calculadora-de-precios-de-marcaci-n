"""
Unit tests for validators module.

Tests validation functions for inputs and data integrity.
"""

import pytest

from utils.validators import validate_quantity


class TestQuantityValidation:
    """Tests for quantity validation."""

    def test_valid_quantity_minimum(self):
        """Test that minimum valid quantity passes."""
        is_valid, msg = validate_quantity(1)
        assert is_valid is True
        assert msg == ""

    def test_valid_quantity_normal(self):
        """Test that normal quantity passes."""
        is_valid, msg = validate_quantity(100)
        assert is_valid is True
        assert msg == ""

    def test_valid_quantity_large(self):
        """Test that large quantity passes."""
        is_valid, msg = validate_quantity(999999)
        assert is_valid is True
        assert msg == ""

    def test_invalid_quantity_zero(self):
        """Test that zero quantity fails."""
        is_valid, msg = validate_quantity(0)
        assert is_valid is False
        assert "mayor a" in msg

    def test_invalid_quantity_negative(self):
        """Test that negative quantity fails."""
        is_valid, msg = validate_quantity(-5)
        assert is_valid is False
        assert "mayor a" in msg

    def test_invalid_quantity_too_large(self):
        """Test that quantity exceeding maximum fails."""
        is_valid, msg = validate_quantity(1_000_001)
        assert is_valid is False
        assert "no puede exceder" in msg
