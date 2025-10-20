#!/usr/bin/env python3
"""
Demo Python module to show how CLI agent templates work
"""


def fibonacci(n):
    """
    Calculate the nth fibonacci number.

    Args:
        n: Position in fibonacci sequence

    Returns:
        The nth fibonacci number

    Example:
        >>> fibonacci(5)
        5
        >>> fibonacci(10)
        55
    """
    if n <= 0:
        return 0
    elif n == 1:
        return 1
    else:
        a, b = 0, 1
        for _ in range(2, n + 1):
            a, b = b, a + b
        return b


def is_prime(n):
    """
    Check if a number is prime.

    Args:
        n: Number to check

    Returns:
        True if prime, False otherwise

    Example:
        >>> is_prime(7)
        True
        >>> is_prime(10)
        False
    """
    if n < 2:
        return False
    for i in range(2, int(n ** 0.5) + 1):
        if n % i == 0:
            return False
    return True


if __name__ == '__main__':
    # Demo usage
    print("Fibonacci sequence:")
    for i in range(10):
        print(f"  fib({i}) = {fibonacci(i)}")

    print("\nPrime numbers under 20:")
    primes = [n for n in range(20) if is_prime(n)]
    print(f"  {primes}")