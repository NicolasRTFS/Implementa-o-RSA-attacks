from __future__ import annotations

import time

from attacks.wiener import attack as wiener_attack
from experiments.common import append_result
from utils.rsa_utils import generate_wiener_vulnerable_key


def main() -> None:
    modulus_bits = 512
    factors = [0.05, 0.10, 0.20, 0.30, 1.00, 2.00, 5.00]

    print("\n=== Experimento: Wiener ===")
    for factor in factors:
        key = generate_wiener_vulnerable_key(
            modulus_bits=modulus_bits,
            d_factor=factor,
        )

        start = time.perf_counter()
        result = wiener_attack(key.n, key.e)
        elapsed = time.perf_counter() - start

        recovered_ok = result.success and result.d == key.d
        print(
            f"d_factor={factor:.2f} | sucesso={result.success} | "
            f"confere={recovered_ok} | tempo={elapsed:.6f}s | iterações={result.iterations}"
        )

        append_result(
            {
                "ataque": "wiener",
                "bits_modulo": modulus_bits,
                "parametro_variado": f"d_factor={factor:.2f}",
                "sucesso": result.success,
                "tempo_execucao_s": f"{elapsed:.8f}",
                "iteracoes": result.iterations,
                "valor_recuperado_confere": recovered_ok,
            }
        )


if __name__ == "__main__":
    main()
