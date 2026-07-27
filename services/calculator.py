"""
Pricing calculation module.

Core business logic for calculating marking prices based on quantity and rules.
"""

from typing import Optional, Tuple

import pandas as pd

import config
from utils.helpers import clean_text, format_currency, safe_float
from utils.logger import logger


class PricingCalculator:
    """
    Calculates marking prices based on quantity and pricing rules.

    This class encapsulates the core business logic for determining
    the correct price based on quantity ranges and business rules.
    """

    def __init__(self, pricing_data: pd.DataFrame):
        """
        Initialize the calculator with pricing data.

        Args:
            pricing_data: DataFrame with pricing rules
        """
        self.pricing_data = pricing_data

    def calculate_price(
        self,
        filtered_data: pd.DataFrame,
        quantity: int,
    ) -> Tuple[Optional[float], str, str]:
        """
        Calculate the price for a given quantity and filtered pricing rules.

        This method implements the core business rule: if the quantity falls
        within a range marked as "mínima" (minimum), return the unit price;
        otherwise return the total price (unit price × quantity).

        Args:
            filtered_data: Pre-filtered DataFrame matching user selections
            quantity: Number of items to mark

        Returns:
            Tuple[price, price_type, message]:
                - price: Calculated price (None if no valid rule found)
                - price_type: Either "minima" or "normal"
                - message: Descriptive message for display
        """
        if filtered_data is None or filtered_data.empty:
            logger.warning(
                f"Attempt to calculate with empty filter. "
                f"Quantity: {quantity}"
            )
            return None, "", config.MSG_NO_COMBINATION

        try:
            # Iterate through each pricing rule row
            for _, row in filtered_data.iterrows():
                range_from = safe_float(row[config.COLUMN_RANGO_DESDE])
                range_to = safe_float(row[config.COLUMN_RANGO_HASTA])
                unit_price = safe_float(row[config.COLUMN_PRECIO])

                # Get and clean observation text
                observation = clean_text(
                    row.get(config.COLUMN_OBSERVACIONES, "")
                )

                # Check if quantity falls within this range
                if not (range_from <= quantity <= range_to):
                    continue

                # If marked as "mínima", return unit price
                if config.OBSERVACION_MINIMA in observation:
                    logger.info(
                        f"Minimum price rule applied: quantity={quantity}, "
                        f"unit_price={unit_price}"
                    )
                    return unit_price, config.MSG_MINIMUM_PRICE, ""

                # Otherwise, return total price (unit price × quantity)
                total_price = quantity * unit_price
                logger.info(
                    f"Normal calculation: quantity={quantity}, "
                    f"unit_price={unit_price}, total={total_price}"
                )
                return total_price, "normal", ""

            # No matching range found
            logger.warning(
                f"No valid range found for quantity: {quantity}"
            )
            return None, "", config.MSG_NO_RANGE

        except Exception as e:
            logger.error(
                f"Error calculating price: {type(e).__name__}: {e}"
            )
            return None, "", config.MSG_QUANTITY_ERROR

    def get_unit_price(self, total_price: float, quantity: int) -> float:
        """
        Calculate unit price from total price.

        Args:
            total_price: Total price for all items
            quantity: Number of items

        Returns:
            Unit price (total_price / quantity)
        """
        if quantity <= 0:
            return 0.0
        return total_price / quantity


def create_calculator(df: pd.DataFrame) -> PricingCalculator:
    """
    Factory function to create a PricingCalculator instance.

    Args:
        df: Pricing data DataFrame

    Returns:
        Initialized PricingCalculator instance
    """
    return PricingCalculator(df)
