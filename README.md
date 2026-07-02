# Experimentos didáticos com ataques ao RSA

Este projeto implementa três ataques didáticos contra instâncias RSA propositalmente vulneráveis:

1. Wiener: expoente privado pequeno.
2. Fermat: primos `p` e `q` próximos.
3. Håstad: mesma mensagem enviada para múltiplos destinatários com expoente público baixo e sem padding.

## Instalação

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Executar todos os experimentos

```bash
python experiments/run_all.py
```

Os resultados serão salvos em:

```text
results/resultados.csv
```

## Gerar gráficos

```bash
python experiments/plot_results.py
```

Os gráficos serão salvos em:

```text
results/plots/
```

## Observação importante

Os códigos geram suas próprias chaves fracas e servem apenas para fins acadêmicos. Não use contra sistemas reais.
# Implementa-o-RSA-attacks
