from __future__ import annotations

from dataclasses import dataclass
from math import isqrt
from typing import Optional

from utils.math_utils import continued_fraction, convergents_from_cf, is_square


@dataclass
class WienerResult:
    success: bool
    d: Optional[int] = None
    p: Optional[int] = None
    q: Optional[int] = None
    iterations: int = 0


def attack(n: int, e: int) -> WienerResult:
    """
    Ataque de Wiener contra RSA com expoente privado pequeno.
    Entrada: chave pública (n, e).
    Saída: d e fatores p, q, se recuperados.
    """
    cf = continued_fraction(e, n)

    for iteration, (k, d_candidate) in enumerate(convergents_from_cf(cf), start=1):
        if k == 0:
            continue

        ed_minus_1 = e * d_candidate - 1
        if ed_minus_1 % k != 0:
            continue

        phi_candidate = ed_minus_1 // k
        s = n - phi_candidate + 1  # s = p + q
        delta = s * s - 4 * n

        if delta < 0 or not is_square(delta):
            continue

        sqrt_delta = isqrt(delta)
        if (s + sqrt_delta) % 2 != 0 or (s - sqrt_delta) % 2 != 0:
            continue

        p = (s + sqrt_delta) // 2
        q = (s - sqrt_delta) // 2

        if p > 1 and q > 1 and p * q == n:
            return WienerResult(
                success=True,
                d=d_candidate,
                p=p,
                q=q,
                iterations=iteration,
            )

    return WienerResult(success=False, iterations=len(cf))
