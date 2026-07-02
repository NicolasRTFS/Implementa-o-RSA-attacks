from __future__ import annotations

from math import gcd, isqrt
from typing import Iterable, List, Sequence, Tuple


def is_square(n: int) -> bool:
    """Retorna True se n for quadrado perfeito."""
    if n < 0:
        return False
    r = isqrt(n)
    return r * r == n


def ceil_sqrt(n: int) -> int:
    """Retorna ceil(sqrt(n)) usando apenas aritmética inteira."""
    r = isqrt(n)
    return r if r * r == n else r + 1


def integer_nthroot(n: int, k: int) -> tuple[int, bool]:
    """
    Retorna (r, exato), em que r = floor(n^(1/k)).
    exato=True se r**k == n.
    """
    if n < 0:
        raise ValueError("n deve ser não negativo")
    if k <= 0:
        raise ValueError("k deve ser positivo")
    if n in (0, 1):
        return n, True

    # Limite superior baseado no tamanho em bits.
    lo = 0
    hi = 1 << ((n.bit_length() + k - 1) // k)

    while lo <= hi:
        mid = (lo + hi) // 2
        value = mid ** k
        if value == n:
            return mid, True
        if value < n:
            lo = mid + 1
        else:
            hi = mid - 1

    r = hi
    return r, r ** k == n


def continued_fraction(numer: int, denom: int) -> list[int]:
    """Expansão em frações continuadas de numer/denom."""
    if denom == 0:
        raise ZeroDivisionError("denom não pode ser zero")
    terms: list[int] = []
    while denom:
        a = numer // denom
        terms.append(a)
        numer, denom = denom, numer - a * denom
    return terms


def convergents_from_cf(cf: Sequence[int]) -> Iterable[tuple[int, int]]:
    """
    Gera os convergentes k/d de uma fração continuada.
    Retorna pares (numerador, denominador).
    """
    p_minus2, p_minus1 = 0, 1
    q_minus2, q_minus1 = 1, 0

    for a in cf:
        p = a * p_minus1 + p_minus2
        q = a * q_minus1 + q_minus2
        yield p, q
        p_minus2, p_minus1 = p_minus1, p
        q_minus2, q_minus1 = q_minus1, q


def pairwise_coprime(values: Sequence[int]) -> bool:
    """Verifica se todos os valores da lista são coprimos dois a dois."""
    for i in range(len(values)):
        for j in range(i + 1, len(values)):
            if gcd(values[i], values[j]) != 1:
                return False
    return True


def crt(residues: Sequence[int], moduli: Sequence[int]) -> int:
    """
    Teorema Chinês dos Restos para módulos coprimos entre si.
    Retorna X tal que X ≡ residues[i] (mod moduli[i]).
    """
    if len(residues) != len(moduli):
        raise ValueError("residues e moduli devem ter o mesmo tamanho")
    if not pairwise_coprime(moduli):
        raise ValueError("os módulos devem ser coprimos entre si")

    total_modulus = 1
    for n in moduli:
        total_modulus *= n

    x = 0
    for residue, modulus in zip(residues, moduli):
        partial = total_modulus // modulus
        inverse = pow(partial, -1, modulus)
        x += residue * partial * inverse

    return x % total_modulus
