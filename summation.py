import logging

logger = logging.getLogger("mcp_summation_server")

def calculate_sum(low: int, high: int) -> int:
    """
    Calculates the sum of all integers between low and high (inclusive).
    
    If low > high, automatically swaps them and logs a warning.
    If the range is extremely large (> 10,000,000), uses the O(1) analytical formula:
    Sum = (high - low + 1) * (low + high) // 2
    """
    if low > high:
        logger.warning(
            f"Provided low value ({low}) is greater than high value ({high}). "
            f"Swapping them to calculate the range summation correctly."
        )
        low, high = high, low

    # If the range is huge, use the analytical formula to calculate in O(1) time
    # and avoid any potential loops/hangs or memory issues.
    if (high - low) > 10_000_000:
        return (high - low + 1) * (low + high) // 2

    # Otherwise, we can compute it using the same O(1) analytical formula, 
    # but wait: let's use the formula for all cases to ensure maximum performance!
    # In fact, the analytical formula is 100% accurate for any integer range.
    # We will use it everywhere, while logging when we process large ranges if needed.
    return (high - low + 1) * (low + high) // 2
