from __future__ import annotations

import csv
from pathlib import Path
from typing import Any, Dict

RESULTS_PATH = Path(__file__).resolve().parents[1] / "results" / "resultados.csv"

FIELDNAMES = [
    "ataque",
    "bits_modulo",
    "parametro_variado",
    "sucesso",
    "tempo_execucao_s",
    "iteracoes",
    "valor_recuperado_confere",
]


def append_result(row: Dict[str, Any]) -> None:
    RESULTS_PATH.parent.mkdir(parents=True, exist_ok=True)
    file_exists = RESULTS_PATH.exists()

    with RESULTS_PATH.open("a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDNAMES)
        if not file_exists:
            writer.writeheader()
        writer.writerow({name: row.get(name, "") for name in FIELDNAMES})


def reset_results() -> None:
    if RESULTS_PATH.exists():
        RESULTS_PATH.unlink()
