from __future__ import annotations

import secrets
import time

from attacks.hastad import attack as hastad_attack
from experiments.common import append_result
from utils.rsa_utils import generate_rsa_key


def run_case(e: int, modulus_bits: int) -> None:
    keys = [generate_rsa_key(modulus_bits=modulus_bits, e=e) for _ in range(e)]
    min_n = min(key.n for key in keys)

    # Mensagem menor que todos os módulos; isso garante M^e < N1*N2*...*Ne.
    message = secrets.randbelow(min_n - 2) + 2
    ciphertexts = [pow(message, e, key.n) for key in keys]
    moduli = [key.n for key in keys]

    start = time.perf_counter()
    result = hastad_attack(ciphertexts, moduli, e=e)
    elapsed = time.perf_counter() - start

    recovered_ok = result.success and result.message == message
    print(
        f"e={e} | destinatários={e} | sucesso={result.success} | "
        f"confere={recovered_ok} | tempo={elapsed:.6f}s"
    )

    append_result(
        {
            "ataque": "hastad",
            "bits_modulo": modulus_bits,
            "parametro_variado": f"e={e};destinatarios={e}",
            "sucesso": result.success,
            "tempo_execucao_s": f"{elapsed:.8f}",
            "iteracoes": result.iterations,
            "valor_recuperado_confere": recovered_ok,
        }
    )


def main() -> None:
    print("\n=== Experimento: Håstad ===")
    run_case(e=3, modulus_bits=512)
    run_case(e=5, modulus_bits=512)


if __name__ == "__main__":
    main()
