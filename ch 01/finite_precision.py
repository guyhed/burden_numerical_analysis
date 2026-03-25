"""
FinitePrecision: A number class for exploring arithmetic with limited decimal precision.

This module provides the FinitePrecision class, which enforces finite decimal 
precision for all arithmetic operations. It is useful for studying numerical 
errors in computational mathematics, as demonstrated in Burden & Burden's 
Numerical Analysis textbook.
"""

import math
from decimal import Decimal, ROUND_HALF_UP


class FinitePrecision:
    """
    A number class that enforces finite decimal precision.

    All arithmetic operations (+, -, *, /) automatically round results
    to the specified number of significant (meaningful) digits.

    Parameters
    ----------
    value : float, int, or str
        The numeric value
    precision : int
        Number of significant digits to preserve

    Example
    -------
    >>> x = FinitePrecision(1.2345, precision=4)
    >>> print(x.value)
    1.234
    >>> y = FinitePrecision(12345.6, precision=4)
    >>> print(y.value)
    12350.0
    """

    def __init__(self, value, precision=4):
        self.precision = precision
        # Store as Decimal for precise control
        self._decimal = Decimal(str(value))
        self._round()

    def _round(self):
        """Round the internal decimal to the specified number of significant digits."""
        if self._decimal == 0:
            return
        magnitude = int(math.floor(math.log10(abs(float(self._decimal)))))
        decimal_places = self.precision - 1 - magnitude
        # Use string form so Decimal carries the correct exponent (e.g. '1E+2'
        # rounds to hundreds, whereas Decimal(100) rounds to ones).
        quantize_format = Decimal(f'1E{-decimal_places}')
        self._decimal = self._decimal.quantize(
            quantize_format, rounding=ROUND_HALF_UP)

    @property
    def value(self):
        """Return the rounded value as a float."""
        return float(self._decimal)

    def __repr__(self):
        return f"FinitePrecision({self.value}, precision={self.precision})"

    def __str__(self):
        return str(self.value)

    # Unary operators
    def __neg__(self):
        """Unary negation."""
        result = FinitePrecision(-self._decimal, precision=self.precision)
        return result

    def __pos__(self):
        """Unary positive (identity)."""
        result = FinitePrecision(self._decimal, precision=self.precision)
        return result

    # Arithmetic operations: return new FinitePrecision instances
    def __add__(self, other):
        if isinstance(other, FinitePrecision):
            result_value = self._decimal + other._decimal
            precision = self.precision
        else:
            result_value = self._decimal + Decimal(str(other))
            precision = self.precision
        result = FinitePrecision(float(result_value), precision=precision)
        return result

    def __radd__(self, other):
        return self.__add__(other)

    def __sub__(self, other):
        if isinstance(other, FinitePrecision):
            result_value = self._decimal - other._decimal
            precision = self.precision
        else:
            result_value = self._decimal - Decimal(str(other))
            precision = self.precision
        result = FinitePrecision(float(result_value), precision=precision)
        return result

    def __rsub__(self, other):
        if isinstance(other, FinitePrecision):
            result_value = other._decimal - self._decimal
            precision = other.precision
        else:
            result_value = Decimal(str(other)) - self._decimal
            precision = self.precision
        result = FinitePrecision(float(result_value), precision=precision)
        return result

    def __mul__(self, other):
        if isinstance(other, FinitePrecision):
            result_value = self._decimal * other._decimal
            precision = self.precision
        else:
            result_value = self._decimal * Decimal(str(other))
            precision = self.precision
        result = FinitePrecision(float(result_value), precision=precision)
        return result

    def __rmul__(self, other):
        return self.__mul__(other)

    def __truediv__(self, other):
        if isinstance(other, FinitePrecision):
            if other._decimal == 0:
                raise ZeroDivisionError("Cannot divide by FinitePrecision(0)")
            result_value = self._decimal / other._decimal
            precision = self.precision
        else:
            if other == 0:
                raise ZeroDivisionError("Cannot divide by 0")
            result_value = self._decimal / Decimal(str(other))
            precision = self.precision
        result = FinitePrecision(float(result_value), precision=precision)
        return result

    def __rtruediv__(self, other):
        if self._decimal == 0:
            raise ZeroDivisionError("Cannot divide by FinitePrecision(0)")
        result_value = Decimal(str(other)) / self._decimal
        result = FinitePrecision(float(result_value), precision=self.precision)
        return result

    def __pow__(self, exponent):
        """Raise to a power."""
        result_value = self._decimal ** exponent
        result = FinitePrecision(float(result_value), precision=self.precision)
        return result

    # Comparison operators
    def __eq__(self, other):
        if isinstance(other, FinitePrecision):
            return self._decimal == other._decimal
        return self._decimal == Decimal(str(other))

    def __lt__(self, other):
        if isinstance(other, FinitePrecision):
            return self._decimal < other._decimal
        return self._decimal < Decimal(str(other))

    def __le__(self, other):
        if isinstance(other, FinitePrecision):
            return self._decimal <= other._decimal
        return self._decimal <= Decimal(str(other))

    def __gt__(self, other):
        if isinstance(other, FinitePrecision):
            return self._decimal > other._decimal
        return self._decimal > Decimal(str(other))

    def __ge__(self, other):
        if isinstance(other, FinitePrecision):
            return self._decimal >= other._decimal
        return self._decimal >= Decimal(str(other))

    def __float__(self):
        return self.value

    def __int__(self):
        return int(self._decimal)
