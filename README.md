# Linux SSH Log Analyzer: Análise de Logs SSH em Linux

## Sobre o projeto

Este repositório reúne uma análise prática de logs de autenticação SSH em ambiente Linux.

A proposta é observar como tentativas de login aparecem nos registros do sistema, interpretar eventos de autenticação e, depois da análise manual, criar uma automação simples em Python para identificar padrões suspeitos.

O projeto faz parte dos meus estudos em Linux, redes, suporte à infraestrutura, troubleshooting e segurança defensiva.

## Status

Projeto em andamento.

A estrutura inicial do repositório já foi criada, o ambiente Linux foi montado em máquina virtual e o OpenSSH Server foi instalado e verificado.
Até o momento, foram documentadas as etapas de ambiente inicial e fundamentos de SSH.

## Objetivos

- Configurar um ambiente Linux em máquina virtual para testes controlados.
- Entender o funcionamento básico do SSH em um servidor Linux.
- Identificar onde ficam os logs de autenticação no Ubuntu.
- Gerar tentativas controladas de login SSH.
- Observar falhas de autenticação, usuários inexistentes e logins bem-sucedidos.
- Analisar manualmente os registros antes de automatizar a leitura.
- Criar um script em Python para processar logs SSH.
- Identificar padrões simples, como várias falhas vindas do mesmo IP ou para o mesmo usuário.
- Gerar um relatório com os principais eventos encontrados.
- Registrar recomendações básicas de hardening para SSH.

## Estudos documentados

| Parte | Tema | Status |
|---|---|---|
| 00 | Ambiente e escopo do projeto | Concluído |
| 01 | Fundamentos de SSH | Concluído |
| 02 | Logs de autenticação no Linux | Concluído |
| 03 | Geração de eventos controlados | Pendente |
| 04 | Análise manual dos logs | Pendente |
| 05 | Lógica de detecção | Pendente |
| 06 | Automação com Python | Pendente |
| 07 | Relatório de investigação | Pendente |
| 08 | Hardening e recomendações | Pendente |
| 09 | Conclusão geral | Pendente |

## Metodologia

Em cada etapa, procuro seguir uma estrutura simples:

1. Definir o objetivo da etapa.
2. Preparar ou revisar o ambiente.
3. Gerar eventos de forma controlada.
4. Observar os registros produzidos no Linux.
5. Identificar informações importantes nos logs.
6. Registrar evidências com prints.
7. Analisar o comportamento observado.
8. Relacionar a análise com suporte, infraestrutura e segurança defensiva.
9. Automatizar partes repetitivas quando fizer sentido.
10. Registrar aprendizados, limitações e recomendações.

A ideia não é começar pelo script, mas entender primeiro o que está acontecendo nos logs. A automação será feita depois da análise manual, para que o código seja baseado em eventos reais observados no laboratório.

## Ambiente utilizado

O ambiente principal utilizado neste projeto é:

- Sistema host: Windows
- Virtualizador: Oracle VirtualBox
- Máquina virtual: Ubuntu 24.04.3 LTS
- Hostname da VM: ubuntu-ssh-lab
- Usuário utilizado no laboratório: vboxuser
- Serviço analisado: OpenSSH Server
- Linguagem da automação: Python
- Terminal: terminal Linux e Windows PowerShell
- Rede: NAT + Host-only

## Ferramentas utilizadas

- Ubuntu Linux
- Oracle VirtualBox
- OpenSSH Server
- Terminal Linux
- Python

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
│   └── conclusao.md
├── images/
│   ├── 00-ambiente/
│   ├── 01-ssh/
│   ├── 02-logs/
│   ├── 03-eventos-controlados/
│   ├── 04-analise-manual/
│   ├── 05-script-python/
│   ├── 06-relatorio/
│   └── 07-hardening/
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

A pasta `logs-local/` será usada apenas localmente para armazenar logs reais gerados na máquina virtual. Esses arquivos não serão publicados no GitHub.

A pasta `data/` será usada para armazenar um log de exemplo anonimizado ou fictício, que poderá ser usado para testar o script sem expor informações do ambiente real.

## Cuidados de privacidade

Logs reais de autenticação podem conter informações do ambiente local, como nome de usuário, hostname, endereços IP internos e horários de acesso.

Por isso, esses arquivos ficarão apenas na pasta `logs-local/`, configurada no `.gitignore`.

Nos documentos publicados, serão usados apenas prints selecionados e exemplos anonimizados, mantendo o valor técnico da análise sem expor dados sensíveis do laboratório.

## Cuidados éticos

Este projeto será realizado apenas em ambiente próprio e controlado.

O objetivo é estudar logs, autenticação SSH, análise defensiva e automação. Não serão realizados testes contra terceiros, varreduras em redes públicas ou tentativas de acesso a sistemas sem autorização.

As tentativas de login usadas no projeto serão geradas manualmente dentro do laboratório, apenas para produzir eventos suficientes para análise.

## Relação com segurança defensiva

A análise de logs é uma habilidade importante para áreas como suporte técnico, infraestrutura, NOC, Blue Team e SOC.

Mesmo em eventos simples de autenticação SSH, já é possível praticar perguntas importantes:

```text
Quem tentou acessar?
Qual usuário foi usado?
A tentativa falhou ou teve sucesso?
O usuário existe no sistema?
Qual IP originou a tentativa?
Houve várias falhas em sequência?
Houve login aceito depois de várias falhas?
O comportamento observado parece normal ou suspeito?
```

Essas perguntas ajudam a transformar registros do sistema em uma investigação. Esse tipo de raciocínio é útil para troubleshooting, análise de alertas, resposta a incidentes e monitoramento de ambientes Linux.

## Resultado esperado

Ao final do projeto, espero ter uma documentação clara mostrando como o ambiente foi montado, como os eventos SSH foram gerados, como os logs foram analisados e como a automação em Python foi construída.

O objetivo final é demonstrar raciocínio investigativo, organização de evidências, noções de Linux e uma base prática em segurança defensiva.

