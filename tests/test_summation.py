import logging
import pytest
from summation import calculate_sum

def test_sum_positive_range():
    # Sum of 1 to 10 is 55
    assert calculate_sum(1, 10) == 55

def test_sum_negative_range():
    # Sum of -5 to -1 is -15 (-5 + -4 + -3 + -2 + -1)
    assert calculate_sum(-5, -1) == -15

def test_sum_mixed_range():
    # Sum of -2 to 2 is 0 (-2 + -1 + 0 + 1 + 2)
    assert calculate_sum(-2, 2) == 0

def test_sum_single_number():
    assert calculate_sum(5, 5) == 5

def test_sum_reversed_bounds(caplog):
    # If low > high, it should swap and calculate correctly, logging a warning.
    with caplog.at_level(logging.WARNING):
        result = calculate_sum(10, 1)
        assert result == 55
        assert any("swap" in record.message.lower() for record in caplog.records)

def test_sum_huge_range():
    # Sum of 1 to 10_000_000 should use the analytical formula
    # Formula: (10_000_000 * (1 + 10_000_000)) / 2 = 50,000,005,000,000
    assert calculate_sum(1, 10_000_000) == 50000005000000

def test_sum_even_huger_range():
    # Sum of 1 to 1,000,000_000 (1 billion) to test efficiency and safety
    # Formula: (1,000,000_000 * (1 + 1,000,000_000)) / 2 = 500,000,000,500,000,000
    assert calculate_sum(1, 1000000000) == 500000000500000000
