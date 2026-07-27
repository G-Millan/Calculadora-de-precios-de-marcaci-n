"""
Unit tests for calculator module.

Tests pricing calculation logic.
"""

import pandas as pd
import pytest

import config
from services.calculator import PricingCalculator


@pytest.fixture
def sample_pricing_data():
    """Create sample pricing data for testing."""
    return pd.DataFrame({
        config.COLUMN_RANGO_DESDE: [1, 100, 1000],
        config.COLUMN_RANGO_HASTA: [99, 999, 10000],
        config.COLUMN_PRECIO: [100, 80, 50],
        config.COLUMN_OBSERVACIONES: ["", "", ""],
    })


@pytest.fixture
def sample_pricing_data_with_minimum():
    """Create sample data with minimum price rule."""
    return pd.DataFrame({
        config.COLUMN_RANGO_DESDE: [1, 100],
        config.COLUMN_RANGO_HASTA: [99, 1000],
        config.COLUMN_PRECIO: [100, 80],
        config.COLUMN_OBSERVACIONES: ["minima", ""],
    })


class TestPricingCalculator:
    """Tests for PricingCalculator class."""

    def test_calculate_price_normal(self, sample_pricing_data):
        """Test normal price calculation (quantity × unit price)."""
        calculator = PricingCalculator(sample_pricing_data)
        price, price_type, msg = calculator.calculate_price(
            sample_pricing_data,
            quantity=50,
        )

        assert price == 5000  # 50 × 100
        assert price_type == "normal"
        assert msg == ""

    def test_calculate_price_minimum(self, sample_pricing_data_with_minimum):
        """Test minimum price calculation (unit price only)."""
        calculator = PricingCalculator(sample_pricing_data_with_minimum)
        price, price_type, msg = calculator.calculate_price(
            sample_pricing_data_with_minimum,
            quantity=10,
        )

        assert price == 100  # Minimum price rule
        assert price_type == config.MSG_MINIMUM_PRICE
        assert msg == ""

    def test_calculate_price_empty_filter(self, sample_pricing_data):
        """Test with empty filter results."""
        calculator = PricingCalculator(sample_pricing_data)
        empty_df = pd.DataFrame()

        price, price_type, msg = calculator.calculate_price(
            empty_df,
            quantity=50,
        )

        assert price is None
        assert msg == config.MSG_NO_COMBINATION

    def test_calculate_price_out_of_range(self, sample_pricing_data):
        """Test with quantity outside all ranges."""
        calculator = PricingCalculator(sample_pricing_data)

        price, price_type, msg = calculator.calculate_price(
            sample_pricing_data,
            quantity=50000,  # Out of range
        )

        assert price is None
        assert msg == config.MSG_NO_RANGE

    def test_get_unit_price(self, sample_pricing_data):
        """Test unit price calculation."""
        calculator = PricingCalculator(sample_pricing_data)

        unit_price = calculator.get_unit_price(
            total_price=5000,
            quantity=50,
        )

        assert unit_price == 100.0

    def test_get_unit_price_zero_quantity(self, sample_pricing_data):
        """Test unit price with zero quantity."""
        calculator = PricingCalculator(sample_pricing_data)

        unit_price = calculator.get_unit_price(
            total_price=1000,
            quantity=0,
        )

        assert unit_price == 0.0
