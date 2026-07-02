from __future__ import annotations

from dataclasses import dataclass
from math import isqrt
from typing import Optional

from utils.math_utils import ceil_sqrt, is_square


@dataclass
class FermatResult:
    success: bool
    p: Optional[int] = None
    q: Optional[int] = None
    iterations: int = 0


def attack(n: int, max_iterations: int = 1_000_000) -> FermatResult:
    """
    Ataque de Fermat para fatorar n = p*q quando p e q são próximos.
    """
    a = ceil_sqrt(n)

    for iteration in range(max_iterations + 1):
        b2 = a * a - n
        if is_square(b2):
            b = isqrt(b2)
            p = a - b
            q = a + b
            if p > 1 and q > 1 and p * q == n:
                return FermatResult(
                    success=True,
                    p=min(p, q),
                    q=max(p, q),
                    iterations=iteration,
                )
        a += 1

    return FermatResult(success=False, iterations=max_iterations)
