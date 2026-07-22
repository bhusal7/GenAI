"""
Basic Calculator Module
Provides fundamental arithmetic operations for the AI Code Assistant project.
"""

def add(a: float, b: float) -> float:
    """Returns the sum of two numbers."""
    return a + b

def subtract(a: float, b: float) -> float:
    """Returns the difference of two numbers."""
    return a - b

def multiply(a: float, b: float) -> float:
    """Returns the product of two numbers."""
    return a * b

def divide(a: float, b: float) -> float:
    """
    Returns the quotient of two numbers.
    Raises ValueError if division by zero is attempted.
    """
    if b == 0:
        raise ValueError("Cannot divide by zero.")
    return a / b

if __name__ == "__main__":
    print("Testing calculator module:")
    print(f"10 + 5 = {add(10, 5)}")
    print(f"10 / 2 = {divide(10, 2)}")