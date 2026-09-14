# 00 - Ambiente e Escopo do Projeto

## Objetivo

Este documento apresenta o ambiente utilizado no projeto, define seu escopo e registra os cuidados adotados durante a análise de logs de autenticação SSH em Linux.

O projeto tem como objetivo praticar a leitura e interpretação de eventos de autenticação em um ambiente controlado, observando como tentativas de acesso via SSH são registradas pelo sistema e como esses registros podem ser utilizados em atividades de troubleshooting, infraestrutura e segurança defensiva.

Esta etapa também estabelece os limites do laboratório e serve como referência para as etapas seguintes do projeto.

## Ambiente utilizado

O laboratório foi criado em uma máquina virtual Linux executada no Oracle VirtualBox sobre um sistema Windows.

A configuração utilizada é:

- Sistema host: Windows
- Virtualizador: Oracle VirtualBox
- Sistema da VM: Ubuntu 24.04.3 LTS
- Kernel: Linux 6.14.0-27-generic
- Hostname da VM: `ubuntu-ssh-lab`
- Usuário utilizado no laboratório: `vboxuser`
- Serviço analisado: OpenSSH Server
- Linguagem utilizada na automação: Python
- Terminal utilizado: terminal Linux
- Rede: NAT + Host-only
- Fonte principal dos eventos: logs de autenticação do Linux

A VM possui duas interfaces de rede:

- `enp0s3`: interface NAT, com IP `10.0.2.15/24`
- `enp0s8`: interface Host-only, com IP `192.168.56.102/24`
- rota padrão: `10.0.2.2`, pela interface `enp0s3`

A interface NAT fornece acesso à internet para instalação de pacotes e atualizações do sistema.

A interface Host-only permite a comunicação entre o Windows host e a máquina virtual Ubuntu sem expor o serviço SSH diretamente à internet.

A conectividade externa da VM foi validada com sucesso por meio de teste de `ping`.

## Por que usar uma máquina virtual

A máquina virtual mantém o laboratório separado do sistema principal e permite realizar alterações, instalar serviços, gerar eventos de autenticação e consultar logs sem interferir diretamente no ambiente Windows.

Essa separação também facilita a repetição dos testes e a documentação das configurações utilizadas durante o projeto.

## Serviço analisado

O principal serviço analisado é o SSH, por meio do OpenSSH Server.

SSH é um protocolo amplamente utilizado para acesso remoto seguro a sistemas Linux e servidores de infraestrutura.

Neste projeto, seu uso tem finalidade exclusivamente educacional e defensiva. As conexões são realizadas apenas dentro do laboratório para observar como diferentes situações de autenticação aparecem nos logs do sistema.

Os principais eventos considerados são:

- login bem-sucedido;
- tentativa de login com senha incorreta;
- tentativa utilizando usuário inexistente;
- várias falhas de autenticação originadas do mesmo IP;
- várias falhas envolvendo o mesmo usuário;
- possível login bem-sucedido após tentativas anteriores com falha.

## Escopo

O projeto utiliza apenas eventos gerados em ambiente próprio e controlado.

As etapas incluem:

- configuração e documentação do ambiente Linux;
- instalação e verificação do OpenSSH Server;
- identificação das fontes de logs de autenticação;
- geração controlada de eventos SSH;
- leitura e análise manual dos registros;
- identificação de falhas de autenticação;
- identificação de usuários inexistentes;
- identificação de logins aceitos;
- análise de tentativas por endereço IP;
- análise de tentativas por usuário;
- análise temporal de eventos;
- definição de regras simples de detecção;
- automação da análise com Python;
- geração de relatório de investigação;
- recomendações básicas de hardening para SSH.

A proposta não é apenas desenvolver um script. Antes da automação, os eventos são observados e analisados manualmente para compreender sua estrutura, contexto e possíveis limitações.

Dessa forma, a lógica implementada posteriormente em Python é baseada no comportamento previamente observado nos logs.

## Fora do escopo

Este projeto não tem como objetivo:

- realizar ataques contra terceiros;
- executar brute force contra sistemas externos;
- testar credenciais em serviços públicos;
- expor o SSH da máquina virtual à internet;
- realizar varreduras em redes externas;
- acessar sistemas sem autorização;
- publicar logs reais contendo informações sensíveis;
- desenvolver uma ferramenta ofensiva de autenticação.

Todas as tentativas de login são realizadas exclusivamente dentro do laboratório local para gerar eventos destinados à análise.

## Privacidade e tratamento dos dados

Logs de autenticação podem conter informações do ambiente, como nomes de usuário, hostname, endereços IP e horários de acesso.

Por esse motivo, os logs originais do laboratório permanecem na pasta:

`logs-local/`

Essa pasta não é publicada no GitHub.

Para testes públicos do script, é utilizado o arquivo:

`data/sample-auth.log`

Esse arquivo contém dados fictícios ou previamente anonimizados.

As imagens utilizadas na documentação apresentam apenas informações adequadas ao contexto público do laboratório.

## Metodologia de análise

Sempre que aplicável, cada etapa do projeto segue uma sequência semelhante:

1. definir o objetivo;
2. executar a configuração, comando ou teste necessário;
3. registrar as evidências;
4. observar os eventos gerados;
5. interpretar os registros;
6. relacionar o resultado com situações de infraestrutura, suporte ou segurança defensiva;
7. registrar limitações e observações;
8. documentar os principais aprendizados.

Esse formato evita que a documentação seja apenas uma sequência de comandos e mantém o foco no raciocínio utilizado durante a análise.

## Perguntas-guia

Durante a análise dos eventos, algumas perguntas orientam a investigação:

```text
Quem tentou acessar o sistema?
Qual usuário foi utilizado?
Esse usuário existe?
A autenticação falhou ou teve sucesso?
Qual endereço IP originou a tentativa?
Houve várias falhas em um curto intervalo?
Foram utilizados usuários diferentes?
Houve um login aceito após várias falhas?
Os eventos pertencem à mesma conexão?
O comportamento observado parece normal ou potencialmente suspeito?
Que medida defensiva poderia reduzir o risco?
```

Essas perguntas ajudam a transformar registros isolados em informações úteis para investigação.

## Relação com infraestrutura e segurança defensiva

Logs de autenticação são úteis em diferentes áreas de TI, incluindo suporte, infraestrutura, NOC, Blue Team e SOC.

Eles podem ajudar a investigar:

- falhas de acesso;
- erros de configuração;
- utilização de usuários inválidos;
- repetição de senhas incorretas;
- comportamento anormal de autenticação;
- possíveis tentativas de acesso indevido.

O projeto utiliza um cenário simples de SSH para praticar esse raciocínio de forma progressiva, começando pela observação manual dos eventos e avançando posteriormente para sua automação.

## Evidências

As evidências produzidas ao longo do projeto são armazenadas na pasta `images/`, organizadas de acordo com cada etapa.

Entre elas estão:

- informações do sistema e da máquina virtual;
- configuração das interfaces de rede;
- conectividade do laboratório;
- status do serviço SSH;
- registros de autenticação;
- falhas de login;
- tentativas com usuários inexistentes;
- logins bem-sucedidos;
- resultados da análise manual;
- validação das regras de detecção;
- execução da automação em Python;
- resultados e relatórios gerados.

## Resultado desta etapa

Ao final desta etapa, o laboratório Linux encontra-se configurado e documentado, com:

- máquina virtual Ubuntu funcional;
- conectividade externa por NAT;
- comunicação local entre Windows e Ubuntu por Host-only;
- limites de segurança e privacidade definidos;
- escopo do projeto documentado;
- estrutura preparada para geração e análise controlada de eventos SSH.

Esse ambiente serve como base para as próximas etapas do projeto, que aprofundam o funcionamento do SSH, os logs de autenticação, a análise manual dos eventos, a lógica de detecção e sua posterior automação com Python.