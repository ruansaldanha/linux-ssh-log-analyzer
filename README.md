# Linux SSH Log Analyzer

## Sobre o projeto

Este repositório documenta uma análise prática de logs de autenticação SSH em Linux.

A proposta é entender como diferentes tentativas de autenticação aparecem nos registros do sistema, analisar esses eventos manualmente e, a partir do comportamento observado, construir uma automação em Python capaz de identificar padrões que mereçam investigação.

O projeto faz parte dos meus estudos em Linux, redes, infraestrutura, troubleshooting e segurança defensiva.

## Status

Projeto em andamento.

Até o momento foram concluídas as etapas de configuração do laboratório, fundamentos de SSH, estudo dos logs de autenticação, geração de eventos controlados e análise manual dos registros.

A lógica inicial de detecção também já foi definida e utiliza como regra principal:

```text
5 ou mais falhas de autenticação
originadas do mesmo endereço IP
dentro de uma janela de 60 segundos
```

Essa regra é uma heurística criada para o laboratório e não representa um padrão universal de segurança.

A etapa atual consiste em validar esse critério com eventos controlados antes de iniciar a implementação do analisador em Python.

## Objetivos

- Configurar um ambiente Linux para testes controlados.
- Entender o funcionamento básico do SSH.
- Identificar e consultar logs de autenticação no Ubuntu.
- Gerar diferentes eventos de autenticação SSH.
- Diferenciar logins bem-sucedidos, falhas de senha e usuários inexistentes.
- Analisar manualmente os registros antes de automatizá-los.
- Correlacionar eventos por usuário, endereço IP e intervalo de tempo.
- Definir uma lógica simples de detecção.
- Implementar a análise dos logs em Python.
- Gerar um relatório com os eventos identificados.
- Documentar recomendações básicas de hardening para SSH.

## Estudos documentados

| Parte | Tema | Status |
|---|---|---|
| 00 | Ambiente e escopo do projeto | Concluído |
| 01 | Fundamentos de SSH | Concluído |
| 02 | Logs de autenticação no Linux | Concluído |
| 03 | Geração de eventos controlados | Concluído |
| 04 | Análise manual dos logs | Concluído |
| 05 | Lógica de detecção | Condluído |
| 06 | Automação com Python | Pendente |
| 07 | Relatório de investigação | Pendente |
| 08 | Hardening e recomendações | Pendente |
| 09 | Conclusão geral | Pendente |

## Metodologia

O projeto segue uma abordagem progressiva:

1. preparar e documentar o ambiente;
2. compreender o funcionamento do serviço analisado;
3. localizar e interpretar suas fontes de log;
4. gerar eventos conhecidos de forma controlada;
5. analisar manualmente os registros;
6. identificar informações relevantes para correlação;
7. definir e validar critérios de detecção;
8. automatizar a análise em Python;
9. organizar os resultados em um relatório;
10. registrar limitações, aprendizados e recomendações.

A ideia é não começar pela automação.

Primeiro, os eventos são produzidos e analisados manualmente para entender sua estrutura e contexto. Somente depois desse processo a lógica é transformada em código.

## Ambiente utilizado

O laboratório utiliza:

- Sistema host: Windows
- Virtualizador: Oracle VirtualBox
- Sistema da VM: Ubuntu 24.04.3 LTS
- Hostname: `ubuntu-ssh-lab`
- Usuário do laboratório: `vboxuser`
- Serviço analisado: OpenSSH Server
- Rede: NAT + Host-only
- Automação: Python
- Terminais: Linux e Windows PowerShell

A interface NAT fornece acesso à internet para a máquina virtual.

A interface Host-only permite a comunicação entre o Windows e o Ubuntu sem expor o serviço SSH diretamente à internet.

## Tecnologias e ferramentas

- Linux / Ubuntu
- OpenSSH Server
- Oracle VirtualBox
- Bash e utilitários de linha de comando
- `grep`
- `awk`
- `journalctl`
- Python
- Windows PowerShell
- Git e GitHub

## Estrutura do repositório

```text
linux-ssh-log-analyzer/
├── data/
│   ├── README.md
│   └── sample-auth.log
├── docs/
│   ├── 00-ambiente-e-escopo.md
│   ├── 01-fundamentos-ssh.md
│   ├── 02-logs-de-autenticacao-linux.md
│   ├── 03-geracao-de-eventos-controlados.md
│   ├── 04-analise-manual-dos-logs.md
│   ├── 05-logica-de-deteccao.md
│   ├── 06-automacao-com-python.md
│   ├── 07-relatorio-de-investigacao.md
│   ├── 08-hardening-e-recomendacoes.md
│   └── 09-conclusao-geral.md
├── images/
│   ├── 00-ambiente/
│   ├── 01-ssh/
│   ├── 02-logs/
│   ├── 03-eventos-controlados/
│   ├── 04-analise-manual/
│   ├── 05-logica-deteccao/
│   ├── 06-script-python/
│   ├── 07-relatorio/
│   └── 08-hardening/
├── logs-local/
├── notes/
│   ├── comandos-usados.md
│   ├── problemas-e-solucoes.md
│   └── regex-utilizadas.md
├── reports/
│   ├── relatorio-incidente-exemplo.md
│   └── resultado-analise.csv
├── src/
│   ├── README.md
│   └── ssh_log_analyzer.py
├── .gitignore
└── README.md
```

## Tratamento dos dados

Os logs originais gerados no laboratório permanecem em:

```text
logs-local/
```

Essa pasta é mantida fora do repositório por meio do `.gitignore`.

Para os testes públicos da automação será utilizado:

```text
data/sample-auth.log
```

Esse arquivo deverá conter apenas dados fictícios ou anonimizados.

As imagens utilizadas na documentação são selecionadas de forma a evitar a exposição desnecessária de informações do ambiente.

## Escopo e uso responsável

Todos os testes são realizados em ambiente próprio e controlado.

O projeto não envolve ataques contra terceiros, varreduras de redes externas, testes de credenciais em serviços públicos ou acesso a sistemas sem autorização.

As tentativas de autenticação SSH são produzidas manualmente dentro do laboratório apenas para gerar eventos que possam ser estudados.

## O que já foi observado

Os testes realizados até o momento permitiram identificar eventos como:

```text
Accepted password
Failed password
Invalid user
Failed password for invalid user
```

A análise manual também mostrou que uma única tentativa pode produzir mais de uma linha no log.

Por exemplo:

```text
Invalid user usuario_teste
Failed password for invalid user usuario_teste
```

Por isso, a quantidade de linhas encontradas não deve ser interpretada automaticamente como a quantidade de tentativas realizadas.

Também foram analisados:

- endereço IP de origem;
- usuário envolvido;
- resultado da autenticação;
- intervalo entre falhas;
- porta de origem;
- relação entre eventos da mesma conexão.

## Lógica inicial de detecção

A primeira regra definida pelo projeto considera potencialmente suspeito o seguinte comportamento:

```text
falhas >= 5
AND
mesmo IP de origem
AND
intervalo <= 60 segundos
```

Essa classificação não confirma um ataque de força bruta.

O objetivo é apenas destacar um conjunto de eventos que ultrapassou o limite definido para o laboratório e que merece análise.

O valor escolhido será validado antes da implementação em Python.

## Relação com infraestrutura e segurança defensiva

Mesmo em um laboratório simples de autenticação SSH, é possível praticar perguntas importantes:

```text
Quem tentou acessar?
Qual usuário foi utilizado?
A autenticação falhou ou teve sucesso?
O usuário existe no sistema?
Qual IP originou a conexão?
Quantas falhas ocorreram?
Em quanto tempo elas ocorreram?
Os eventos pertencem à mesma conexão?
O comportamento merece investigação?
```

Esse tipo de raciocínio pode ser aplicado em atividades de troubleshooting, administração de sistemas, monitoramento, Blue Team e SOC.

O objetivo do projeto não é apenas detectar falhas de autenticação, mas praticar a transformação de registros técnicos em informações úteis para investigação.

## Próximas etapas

A sequência planejada é:

1. validar a regra inicial de detecção;
2. preparar um log de exemplo para testes;
3. implementar o parser em Python;
4. aplicar a regra automaticamente;
5. organizar os resultados em um relatório;
6. documentar recomendações de hardening;
7. registrar as conclusões do projeto.

## Resultado esperado

Ao final do projeto, o repositório deverá demonstrar todo o processo utilizado:

```text
ambiente
    ↓
eventos SSH
    ↓
logs
    ↓
análise manual
    ↓
lógica de detecção
    ↓
automação em Python
    ↓
relatório
    ↓
hardening e conclusões
```

Mais do que apresentar um script pronto, o objetivo é demonstrar o raciocínio utilizado para compreender os registros, definir critérios, reconhecer limitações e automatizar uma análise baseada em evidências observadas no laboratório.