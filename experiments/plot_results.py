from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[1]
RESULTS_PATH = PROJECT_ROOT / "results" / "resultados.csv"
PLOTS_DIR = PROJECT_ROOT / "results" / "plots"


def main() -> None:
    if not RESULTS_PATH.exists():
        raise FileNotFoundError("Execute primeiro: python experiments/run_all.py")

    PLOTS_DIR.mkdir(parents=True, exist_ok=True)
    df = pd.read_csv(RESULTS_PATH)

    # Gráfico 1: tempo por ataque/configuração.
    labels = df["ataque"] + "\n" + df["parametro_variado"].astype(str)
    plt.figure(figsize=(12, 6))
    plt.bar(labels, df["tempo_execucao_s"])
    plt.ylabel("Tempo de execução (s)")
    plt.xlabel("Ataque e parâmetro")
    plt.title("Tempo de execução por experimento")
    plt.xticks(rotation=60, ha="right")
    plt.tight_layout()
    plt.savefig(PLOTS_DIR / "tempo_por_experimento.png", dpi=200)
    plt.close()

    # Gráfico 2: iterações do Fermat por gap_bits.
    fermat = df[df["ataque"] == "fermat"].copy()
    if not fermat.empty:
        fermat["gap_bits"] = fermat["parametro_variado"].str.extract(r"gap_bits=(\d+)").astype(int)
        plt.figure(figsize=(8, 5))
        plt.plot(fermat["gap_bits"], fermat["iteracoes"], marker="o")
        plt.ylabel("Iterações")
        plt.xlabel("gap_bits, distância aproximada entre p e q")
        plt.title("Ataque de Fermat: iterações conforme p e q se afastam")
        plt.tight_layout()
        plt.savefig(PLOTS_DIR / "fermat_iteracoes.png", dpi=200)
        plt.close()

    print(f"Gráficos salvos em: {PLOTS_DIR}")


if __name__ == "__main__":
    main()
