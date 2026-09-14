# 04 - Análise Manual dos Logs

## Objetivo

Nesta etapa, os eventos de autenticação SSH gerados anteriormente foram analisados manualmente antes da criação de qualquer mecanismo automatizado de detecção.

O objetivo foi entender quais informações podem ser extraídas dos registros, como diferentes situações de autenticação aparecem no log e quais cuidados são necessários para interpretar corretamente esses eventos.

Essa análise servirá como base para a definição da lógica de detecção e para a implementação posterior do parser em Python.

## Seleção dos eventos relevantes

O arquivo `/var/log/auth.log` registra eventos de autenticação de diferentes componentes do sistema.

Por isso, a análise foi direcionada aos registros relacionados ao `sshd` e aos seguintes padrões:

```text
Accepted password
Failed password
Invalid user
Failed password for invalid user
```

Nos eventos gerados durante o laboratório foram identificadas:

- 1 autenticação bem-sucedida para `vboxuser`;
- 4 falhas de autenticação para `vboxuser`;
- 1 tentativa malsucedida utilizando o usuário inexistente `usuario_teste`.

Também foi encontrada a linha `Invalid user usuario_teste`, associada à mesma tentativa envolvendo o usuário inexistente.

## Linhas de log e tentativas de autenticação

Um dos principais cuidados identificados durante a análise foi não interpretar diretamente a quantidade de linhas do log como a quantidade de tentativas realizadas.

A tentativa utilizando `usuario_teste`, por exemplo, produziu registros como:

```text
Invalid user usuario_teste
```

e:

```text
Failed password for invalid user usuario_teste
```

As duas linhas descrevem informações relacionadas à mesma tentativa de autenticação.

Portanto, contabilizá-las como duas tentativas diferentes produziria uma contagem incorreta.

Essa distinção será importante posteriormente para evitar duplicidade durante o processamento automatizado dos logs.

## Análise por endereço IP

As tentativas de autenticação analisadas tiveram como origem:

```text
192.168.56.1
```

Esse endereço corresponde ao host Windows utilizado para realizar os testes pela rede Host-only.

Como todos os eventos foram produzidos intencionalmente a partir da mesma máquina, esse resultado era esperado no laboratório.

A análise por IP, entretanto, demonstra como esse campo pode ser utilizado para agrupar eventos provenientes de uma mesma origem.

## Análise por usuário

Foram identificados dois nomes de usuário durante os testes:

- `vboxuser`: 5 tentativas, sendo 1 bem-sucedida e 4 malsucedidas;
- `usuario_teste`: 1 tentativa malsucedida utilizando um usuário inexistente.

Também foi observada uma diferença importante na estrutura das linhas:

```text
Failed password for vboxuser
```

e:

```text
Failed password for invalid user usuario_teste
```

Em uma falha envolvendo usuário válido, o nome aparece imediatamente depois de `for`.

Quando o usuário é inexistente, aparecem primeiro os termos `invalid user`.

Essa diferença precisa ser considerada na extração automática do nome do usuário.

## Análise temporal

Três falhas consecutivas para `vboxuser` ocorreram nos seguintes horários:

```text
14:09:08
14:09:22
14:09:30
```

Entre a primeira e a última falha transcorreram aproximadamente 22 segundos.

Além da proximidade temporal, os três registros apresentaram:

- mesmo usuário;
- mesmo endereço IP de origem;
- mesma porta de origem;
- mesmo PID do processo `sshd`.

Essas informações indicam que as três falhas ocorreram dentro da mesma conexão SSH.

Apesar da concentração das tentativas em um curto intervalo, esse comportamento não é suficiente para concluir que ocorreu um ataque de força bruta.

No próprio laboratório, o padrão foi produzido manualmente por um usuário legítimo ao informar três senhas incorretas durante uma única conexão.

Esse resultado mostrou a importância de considerar contexto antes de classificar um conjunto de eventos como suspeito.

## Evidências

As evidências desta etapa foram armazenadas em:

```text
images/04-analise-manual/01-eventos-ssh-filtrados.png
images/04-analise-manual/02-contagem-eventos.png
images/04-analise-manual/03-contagem-por-ip.png
images/04-analise-manual/04-usuarios-extraidos.png
images/04-analise-manual/05-contagem-por-usuario.png
images/04-analise-manual/06-analise-temporal-falhas.png
```

Elas registram a filtragem dos eventos, as contagens realizadas, a extração de endereços IP e usuários e a análise temporal das falhas.

## Aprendizados

A análise manual mostrou que a interpretação de logs de autenticação exige mais contexto do que simplesmente contar ocorrências de `Failed password`.

Os principais elementos identificados para análise foram:

- tipo do evento;
- resultado da autenticação;
- usuário envolvido;
- existência ou não do usuário;
- endereço IP de origem;
- porta de origem;
- PID do processo `sshd`;
- quantidade de falhas;
- intervalo de tempo entre os eventos;
- relação entre diferentes linhas do log;
- repetição do comportamento em diferentes conexões.

Também ficou claro que múltiplas linhas podem representar uma única tentativa e que várias falhas em um intervalo curto não devem ser classificadas automaticamente como ataque.

Esses aprendizados servem de base para a Etapa 05, na qual será definida uma regra simples para destacar comportamentos que mereçam investigação.