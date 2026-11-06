"""Shared validation for product measurements."""

import math


def non_negative_number(value, label):
    if type(value) not in (int, float):
        raise ValueError(f"{label} must be a finite, non-negative number.")
    try:
        value = float(value)
    except OverflowError:
        raise ValueError(f"{label} must be a finite, non-negative number.")
    if not math.isfinite(value) or value < 0:
        raise ValueError(f"{label} must be a finite, non-negative number.")
    return value
