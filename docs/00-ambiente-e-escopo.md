# 00 - Ambiente e Escopo do Projeto

## Objetivo

Este documento apresenta o ambiente utilizado, o escopo do projeto e os cuidados adotados durante a análise de logs SSH em Linux.

A ideia deste projeto é praticar a leitura de logs de autenticação em um ambiente controlado, observando como tentativas de login SSH aparecem no sistema e como esses registros podem ser usados para entender eventos de acesso.

Este arquivo serve como ponto de partida para deixar claro onde os testes serão feitos, quais limites foram definidos e quais cuidados serão seguidos ao longo do projeto.

## Ambiente utilizado

O ambiente principal será uma máquina virtual Linux criada no Oracle VirtualBox.

A configuração prevista para o laboratório é:

- Sistema host: Windows
- Virtualizador: Oracle VirtualBox
- Máquina virtual: Ubuntu 64 bits
- Serviço analisado: OpenSSH Server
- Linguagem usada na automação: Python
- Terminal utilizado: terminal Linux
- Rede utilizada: ambiente local controlado
- Logs analisados: logs de autenticação do Linux

As informações reais da máquina virtual serão registradas após a criação do ambiente, incluindo versão do Ubuntu, hostname, usuário utilizado, interfaces de rede e endereço IP usado nos testes.

## Ambiente utilizado

O ambiente principal utilizado neste projeto é uma máquina virtual Linux criada no Oracle VirtualBox.

A configuração inicial do laboratório é:

- Sistema host: Windows
- Virtualizador: Oracle VirtualBox
- Máquina virtual: Ubuntu 64 bits
- Sistema da VM: Ubuntu 24.04.3 LTS
- Versão base: Ubuntu 24.04
- Codinome da versão: Noble Numbat
- Kernel: Linux 6.14.0-27-generic
- Hostname da VM: ubuntu-ssh-lab
- Usuário utilizado no laboratório: vboxuser
- Serviço analisado: OpenSSH Server
- Linguagem usada na automação: Python
- Terminal utilizado: terminal Linux
- Rede utilizada: NAT + Host-only
- Logs analisados: logs de autenticação do Linux

A VM foi configurada com duas interfaces de rede:

- Interface NAT: `enp0s3`
- IP da interface NAT: `10.0.2.15/24`
- Interface Host-only: `enp0s8`
- IP da interface Host-only: `192.168.56.102/24`
- Rota padrão: via `10.0.2.2` pela interface `enp0s3`

A interface NAT será usada para acesso à internet a partir da VM, permitindo instalação de pacotes e atualizações do sistema.

A interface Host-only será usada para comunicação entre o Windows e a máquina virtual Ubuntu, mantendo o laboratório em um ambiente local controlado.

A conectividade com a internet foi testada usando `ping google.com`, com resposta bem-sucedida e 0% de perda de pacotes.

## Por que usar uma máquina virtual

A máquina virtual será usada para manter o laboratório separado do sistema principal.

Isso permite instalar serviços, alterar configurações, gerar eventos de autenticação e consultar logs sem impactar diretamente o Windows.

Também facilita a organização do projeto, porque o ambiente fica dedicado aos testes e pode ser documentado com mais clareza.

## Serviço analisado

O serviço principal analisado será o SSH.

O SSH é usado para acessar sistemas remotamente de forma segura, sendo bastante comum em servidores Linux e ambientes de infraestrutura.

Neste projeto, o foco não será usar o SSH de forma ofensiva, mas entender como eventos de autenticação aparecem nos logs do sistema.

Os principais eventos observados serão:

- tentativa de login com senha incorreta;
- tentativa de login com usuário inexistente;
- login bem-sucedido;
- várias falhas de autenticação vindas do mesmo IP;
- várias falhas envolvendo o mesmo usuário;
- possível login aceito após tentativas anteriores com falha.

## Escopo

Este projeto analisará eventos gerados em ambiente próprio, com foco educacional e defensivo.

As análises terão como foco:

- configuração básica do ambiente Linux;
- instalação ou verificação do OpenSSH Server;
- localização dos logs de autenticação no Ubuntu;
- geração controlada de eventos SSH;
- leitura manual dos registros;
- identificação de falhas de login;
- identificação de usuários inválidos;
- identificação de logins aceitos;
- contagem de tentativas por IP;
- contagem de tentativas por usuário;
- criação de regras simples de detecção;
- automação da análise com Python;
- geração de um relatório de investigação;
- recomendações básicas de hardening para SSH.

O foco não é apenas criar um script, mas entender primeiro o comportamento registrado nos logs. A automação será feita depois da análise manual, para que o código tenha relação direta com os eventos observados no laboratório.

## Fora do escopo

Este projeto não tem como objetivo:

- realizar ataques contra terceiros;
- executar brute force real;
- testar credenciais em sistemas públicos;
- expor o SSH da máquina virtual para a internet;
- fazer varreduras em redes externas;
- tentar acessar máquinas sem autorização;
- publicar logs reais contendo dados sensíveis;
- criar uma ferramenta ofensiva de autenticação.

Todas as tentativas de login serão feitas apenas dentro do laboratório local, com o objetivo de gerar registros suficientes para análise.

## Cuidados de privacidade

Logs reais de autenticação podem conter informações do ambiente local, como nome de usuário, hostname, endereços IP internos e horários de acesso.

Por esse motivo, os logs reais ficarão apenas na pasta `logs-local/`, que não será publicada no GitHub.

Para testes públicos do script, será usado um arquivo em `data/sample-auth.log`, contendo dados fictícios ou anonimizados.

Nos documentos publicados, serão usados apenas prints selecionados e exemplos que não exponham informações sensíveis do laboratório.

## Padrão de análise

Cada etapa seguirá, sempre que possível, o seguinte padrão:

1. Objetivo da etapa.
2. Ambiente ou configuração utilizada.
3. Comando ou ação executada.
4. Evidências salvas.
5. Eventos observados nos logs.
6. Análise do comportamento.
7. Relação com suporte, infraestrutura e segurança defensiva.
8. Observações importantes.
9. Aprendizados.
10. Conclusão.

Esse padrão ajuda a manter o projeto organizado e evita que a documentação seja apenas uma lista de comandos.

## Perguntas-guia

Durante a análise dos logs, o foco será responder perguntas como:

```text
Quem tentou acessar o sistema?
Qual usuário foi utilizado?
O usuário existe no sistema?
A autenticação falhou ou teve sucesso?
Qual IP originou a tentativa?
Houve muitas falhas em sequência?
Houve tentativa com usuários diferentes?
Houve login aceito depois de falhas anteriores?
O comportamento observado parece normal ou suspeito?
Que ação defensiva poderia reduzir esse risco?
```

Essas perguntas ajudam a transformar registros do sistema em uma investigação.

## Relação com segurança defensiva

A análise de logs é uma habilidade importante para áreas como suporte técnico, infraestrutura, NOC, Blue Team e SOC.

Em um ambiente real, logs de autenticação podem ajudar a identificar falhas de acesso, erro de configuração, tentativa de uso de usuários inválidos, repetição de senhas incorretas e possíveis comportamentos suspeitos.

Neste projeto, o objetivo é praticar esse raciocínio em um laboratório simples, começando pela observação manual dos eventos e avançando depois para a automação com Python.

## Evidências previstas

Durante o projeto, serão registradas evidências como:

- versão do Ubuntu utilizado;
- configuração de rede da máquina virtual;
- status do serviço SSH;
- localização dos logs de autenticação;
- exemplos de falhas de login;
- exemplos de usuários inexistentes;
- exemplos de login bem-sucedido;
- resultado da análise manual;
- execução do script em Python;
- relatório final gerado.

As evidências serão salvas na pasta `images/`, separadas de acordo com a etapa correspondente.

## Resultado esperado

Ao final desta etapa inicial, espero ter um laboratório Linux documentado, com escopo claro, limites definidos e pronto para gerar eventos controlados de autenticação SSH.

Esse ambiente servirá como base para as próximas etapas do projeto: entender o SSH, localizar os logs, gerar eventos, analisar registros manualmente e construir a automação em Python.