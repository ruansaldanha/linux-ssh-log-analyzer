# Linux SSH Log Analyzer

Projeto prático de **análise defensiva de logs de autenticação SSH** em Linux. O laboratório foi construído de forma progressiva: preparação da VM Ubuntu, geração controlada de eventos, análise manual de registros, criação de uma regra de detecção e automação com Python.

> **Status:** etapas 00 a 07 concluídas. Etapa 08 (hardening SSH) em preparação; conclusão geral pendente.

## O que o analisador faz

- Lê arquivos de log com timestamps ISO 8601 nos formatos previstos pelo laboratório.
- Reconhece `Failed password`, `Accepted password`, `Invalid user` e registros `message repeated N times`.
- Extrai timestamp, usuário e IP IPv4; contabiliza falhas por endereço de origem.
- Aplica uma **janela deslizante de 60 segundos**: cinco ou mais falhas do mesmo IP geram um alerta de *comportamento potencialmente suspeito*.
- Exporta alertas em CSV e um resumo técnico em Markdown.

**Importante:** um alerta não confirma invasão ou força bruta. O limite é uma heurística didática; mensagens agrupadas não fornecem timestamps individuais, o que limita a precisão temporal.

## Executar

**Requisitos:** Python 3.10+; nenhuma dependência externa. No PowerShell, use `python` ou `python3`, conforme a instalação.

Na raiz do repositório:

```bash
python3 src/ssh_log_analyzer.py
python3 src/ssh_log_analyzer.py teste-multiplos-ips.log
```

O primeiro comando analisa `data/sample-auth.log`; o segundo analisa o arquivo informado, localizado em `data/`. O programa imprime os eventos reconhecidos e gera:

- `reports/resultado-analise.csv` — lista de alertas encontrados, com separador `;`.
- `reports/relatorio-investigacao.md` — resumo da análise, contagem por IP e limitações.

**Atenção:** os dois arquivos de saída acima são **sobrescritos** a cada execução. Exemplos preservados estão em `reports/resultado-com-alerta.csv`, `reports/resultado-sem-alerta.csv`, `reports/relatorio-com-alerta.md` e `reports/relatorio-sem-alerta.md`.

## Cenários e testes

| Arquivo em `data/` | Comportamento esperado |
|---|---|
| `sample-auth.log` | 6 falhas em 30 segundos para `192.0.2.10`: **alerta** |
| `teste-acima-60s.log` | 6 falhas distribuídas em grupos separados: **sem alerta** |
| `teste-limite-60s.log` | 5 falhas em exatamente 60 segundos: **alerta** |
| `teste-limite-61s.log` | 5 falhas em 61 segundos: **sem alerta** |
| `teste-multiplos-ips.log` | 7 falhas distribuídas entre 3 IPs: **sem alerta** |
| `teste-repeticoes-nao-falhas.log` | Repetições de sucesso/usuário inválido não contam como falhas |

Para executar os testes automatizados (biblioteca padrão `unittest`):

```bash
python3 -m unittest discover -s tests -v
```

Os testes cobrem cenários positivos, negativos, limites temporais, agrupamento por IP, mensagens repetidas e geração dos relatórios. As capturas dos testes manuais continuam disponíveis na documentação.

## Etapas do projeto

| Etapa | Documento | Situação |
|---|---|---|
| 00 | [Ambiente e escopo](docs/00-ambiente-e-escopo.md) | Concluída |
| 01 | [Fundamentos de SSH](docs/01-fundamentos-ssh.md) | Concluída |
| 02 | [Logs de autenticação Linux](docs/02-logs-de-autenticacao-linux.md) | Concluída |
| 03 | [Eventos controlados](docs/03-geracao-de-eventos-controlados.md) | Concluída |
| 04 | [Análise manual](docs/04-analise-manual-dos-logs.md) | Concluída |
| 05 | [Lógica de detecção](docs/05-logica-de-deteccao.md) | Concluída |
| 06 | [Automação em Python](docs/06-automacao-com-python.md) | Concluída |
| 07 | [Relatório de investigação](docs/07-relatorio-de-investigacao.md) | Concluída |
| 08 | [Hardening e recomendações](docs/08-hardening-e-recomendacoes.md) | Em preparação |
| 09 | [Conclusão](docs/conclusao.md) | Pendente |

## Evidências e relatórios

- [Teste controlado da regra](docs/05-logica-de-deteccao.md#validação-da-regra) e imagem em `images/05-logica-deteccao/`.
- [Sete evidências dos testes de Python](docs/06-automacao-com-python.md#evidências).
- [Três evidências dos relatórios](docs/07-relatorio-de-investigacao.md#8-evidências).
- [Exemplo de interpretação humana dos achados](reports/relatorio-incidente-exemplo.md).

## Estrutura principal

```text
data/       Logs sintéticos reproduzíveis (IPs reservados para documentação)
docs/       Etapas detalhadas, métodos, resultados e limitações
images/     Capturas de tela das evidências
notes/      Comandos e anotações do laboratório
reports/    Relatórios CSV e Markdown
src/        Código do analisador
tests/      Testes automatizados com unittest
logs-local/ Logs originais do laboratório, excluídos do Git
```

## Ambiente e uso responsável

O laboratório foi realizado com Windows, VirtualBox, Ubuntu 24.04.3 LTS, OpenSSH Server e rede NAT + Host-only. Os arquivos públicos em `data/` são **sintéticos**, com IPs de documentação `192.0.2.0/24`. Os registros reais permanecem em `logs-local/`, ignorado pelo Git.

Os testes de autenticação descritos neste projeto ocorreram em ambiente próprio e controlado. O analisador **não inicia conexões SSH nem realiza tentativas de login**: ele processa registros previamente coletados.

## Limitações e próximos passos

O parser foi projetado para o formato ISO e os padrões de autenticação por senha usados no laboratório; não inclui IPv6, todos os formatos de syslog, outros métodos SSH nem correlação avançada. Um alerta por IP é emitido por execução. O próximo trabalho prático é avaliar configurações efetivas do `sshd`, testar autenticação por chave e documentar medidas de hardening sem perder o acesso à VM.
