# Implementação em Python

O script principal é [`ssh_log_analyzer.py`](ssh_log_analyzer.py). Ele usa apenas bibliotecas da instalação padrão do Python.

## Executar

Na pasta raiz do repositório:

```bash
python3 src/ssh_log_analyzer.py
python3 src/ssh_log_analyzer.py teste-multiplos-ips.log
python3 -m unittest discover -s tests -v
```

O parâmetro opcional é o nome do arquivo dentro da pasta `data/`. Sem argumento, utiliza `sample-auth.log`.

## Organização das funções

| Função | Papel |
|---|---|
| `interpretar_linha` | Reconhece eventos SSH e extrai timestamp, usuário, IP e quantidade |
| `calcular_quantidade_falhas` | Diferencia falhas de sucessos e outras mensagens repetidas |
| `ler_eventos` | Lê registros reconhecidos do arquivo |
| `organizar_falhas` | Agrupa falhas e horários por IP |
| `detectar_alertas` | Aplica a janela deslizante de cinco falhas em até 60 segundos |
| `gerar_relatorio_csv` | Exporta alertas para CSV |
| `gerar_relatorio_markdown` | Exporta resumo técnico para Markdown |
| `exibir_resultados` / `main` | Exibe resultados e coordena a execução |

## Saídas e limitações

Os arquivos `reports/resultado-analise.csv` e `reports/relatorio-investigacao.md` são sobrescritos a cada execução. O CSV contém somente alertas; um arquivo com cabeçalho e sem linhas é um resultado válido.

O parser é voltado aos logs ISO/IPv4 dos exemplos. Registros `message repeated` são atribuídos ao horário da linha agregada, não aos horários reais de cada tentativa. A classificação automática **não confirma incidentes**.
