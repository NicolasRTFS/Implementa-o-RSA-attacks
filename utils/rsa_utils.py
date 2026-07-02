from __future__ import annotations

import secrets
from dataclasses import dataclass
from math import gcd, isqrt

from sympy import isprime, nextprime


@dataclass(frozen=True)
class RSAKey:
    p: int
    q: int
    n: int
    phi: int
    e: int
    d: int


def random_prime(bits: int) -> int:
    """Gera um primo com exatamente 'bits' bits."""
    if bits < 8:
        raise ValueError("use pelo menos 8 bits")

    lower = 1 << (bits - 1)
    upper = 1 << bits

    while True:
        candidate = secrets.randbits(bits) | lower | 1
        p = int(nextprime(candidate))
        if lower <= p < upper:
            return p


def generate_rsa_key(modulus_bits: int = 512, e: int = 65537) -> RSAKey:
    """
    Gera uma chave RSA didática. Para Håstad, use e=3 ou e=5.
    A função garante gcd(e, phi)=1.
    """
    if modulus_bits < 128:
        raise ValueError("use modulus_bits >= 128 para os experimentos")

    prime_bits = modulus_bits // 2
    while True:
        p = random_prime(prime_bits)
        q = random_prime(prime_bits)
        if p == q:
            continue
        phi = (p - 1) * (q - 1)
        if gcd(e, phi) == 1:
            n = p * q
            d = pow(e, -1, phi)
            return RSAKey(p=p, q=q, n=n, phi=phi, e=e, d=d)


def generate_wiener_vulnerable_key(
    modulus_bits: int = 512,
    d_factor: float = 0.20,
) -> RSAKey:
    """
    Gera RSA vulnerável a Wiener, escolhendo d aproximadamente:
        d = d_factor * N^(1/4)

    O ataque clássico tende a funcionar quando d < (1/3) * N^(1/4).
    Valores acima disso são úteis para demonstrar falha experimental.
    """
    if d_factor <= 0:
        raise ValueError("d_factor deve ser positivo")

    prime_bits = modulus_bits // 2

    while True:
        p = random_prime(prime_bits)
        q = random_prime(prime_bits)
        if p == q:
            continue

        n = p * q
        phi = (p - 1) * (q - 1)
        n_fourth_root = isqrt(isqrt(n))
        d = max(3, int(d_factor * n_fourth_root))

        # Ajusta d até ficar coprimo com phi.
        if d % 2 == 0:
            d += 1
        while d < phi and gcd(d, phi) != 1:
            d += 2

        if 1 < d < phi and gcd(d, phi) == 1:
            e = pow(d, -1, phi)
            if 1 < e < phi:
                return RSAKey(p=p, q=q, n=n, phi=phi, e=e, d=d)


def generate_fermat_vulnerable_key(
    prime_bits: int = 128,
    gap_bits: int = 70,
    e: int = 65537,
) -> RSAKey:
    """
    Gera p e q próximos para o ataque de Fermat.

    gap_bits controla aproximadamente a distância q-p.
    Para prime_bits=128, valores como 48, 56, 64 e 70 são bons para testes rápidos.
    """
    if gap_bits <= 0:
        raise ValueError("gap_bits deve ser positivo")
    if gap_bits >= prime_bits:
        raise ValueError("gap_bits deve ser menor que prime_bits")

    lower = 1 << (prime_bits - 1)
    upper = 1 << prime_bits

    while True:
        base = secrets.randbits(prime_bits) | lower | 1
        if base >= upper:
            continue

        p = int(nextprime(base))
        # Distância aproximada controlada por gap_bits.
        gap = (1 << gap_bits) + secrets.randbelow(1 << max(1, gap_bits - 4))
        q = int(nextprime(base + gap))

        if p == q or not (lower <= p < upper and lower <= q < upper):
            continue

        phi = (p - 1) * (q - 1)
        if gcd(e, phi) == 1:
            n = p * q
            d = pow(e, -1, phi)
            return RSAKey(p=p, q=q, n=n, phi=phi, e=e, d=d)


def encrypt_int(message: int, key: RSAKey) -> int:
    if not (0 <= message < key.n):
        raise ValueError("mensagem deve estar no intervalo 0 <= m < n")
    return pow(message, key.e, key.n)


def decrypt_int(ciphertext: int, key: RSAKey) -> int:
    return pow(ciphertext, key.d, key.n)
