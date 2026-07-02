from __future__ import annotations

import sys
from pathlib import Path

# Permite executar este arquivo diretamente com:
# python experiments/run_all.py
PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from experiments.common import RESULTS_PATH, reset_results
from experiments.run_fermat import main as run_fermat
from experiments.run_hastad import main as run_hastad
from experiments.run_wiener import main as run_wiener


def main() -> None:
    reset_results()
    run_wiener()
    run_fermat()
    run_hastad()
    print(f"\nResultados salvos em: {RESULTS_PATH}")


if __name__ == "__main__":
    main()
