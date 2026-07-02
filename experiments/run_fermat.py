from __future__ import annotations

import time

from attacks.fermat import attack as fermat_attack
from experiments.common import append_result
from utils.rsa_utils import generate_fermat_vulnerable_key


def main() -> None:
    prime_bits = 128
    max_iterations = 1_000_000
    gap_bits_values = [16, 32, 48, 56, 64, 70, 72, 74]

    print("\n=== Experimento: Fermat ===")
    for gap_bits in gap_bits_values:
        key = generate_fermat_vulnerable_key(
            prime_bits=prime_bits,
            gap_bits=gap_bits,
        )

        start = time.perf_counter()
        result = fermat_attack(key.n, max_iterations=max_iterations)
        elapsed = time.perf_counter() - start

        recovered_ok = result.success and {result.p, result.q} == {key.p, key.q}
        print(
            f"gap_bits={gap_bits:>2} | sucesso={result.success} | "
            f"confere={recovered_ok} | tempo={elapsed:.6f}s | iterações={result.iterations}"
        )

        append_result(
            {
                "ataque": "fermat",
                "bits_modulo": key.n.bit_length(),
                "parametro_variado": f"gap_bits={gap_bits}",
                "sucesso": result.success,
                "tempo_execucao_s": f"{elapsed:.8f}",
                "iteracoes": result.iterations,
                "valor_recuperado_confere": recovered_ok,
            }
        )


if __name__ == "__main__":
    main()
