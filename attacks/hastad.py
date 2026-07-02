from __future__ import annotations

from dataclasses import dataclass
from typing import Optional, Sequence

from utils.math_utils import crt, integer_nthroot, pairwise_coprime


@dataclass
class HastadResult:
    success: bool
    message: Optional[int] = None
    iterations: int = 1


def attack(ciphertexts: Sequence[int], moduli: Sequence[int], e: int) -> HastadResult:
    """
    Ataque de Håstad/Broadcast.
    Recupera M quando a mesma mensagem foi cifrada para e destinatários,
    todos com o mesmo expoente público e e módulos coprimos entre si.
    """
    if len(ciphertexts) != len(moduli):
        raise ValueError("ciphertexts e moduli devem ter o mesmo tamanho")
    if len(ciphertexts) < e:
        raise ValueError("para Håstad, é necessário pelo menos e criptogramas")
    if not pairwise_coprime(moduli):
        raise ValueError("os módulos devem ser coprimos entre si")

    x = crt(ciphertexts, moduli)
    root, exact = integer_nthroot(x, e)

    if exact:
        return HastadResult(success=True, message=root, iterations=1)
    return HastadResult(success=False, iterations=1)
