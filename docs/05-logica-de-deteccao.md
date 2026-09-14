# 05 - Lógica de Detecção

## Objetivo

Nesta etapa é definida uma lógica simples para identificar padrões de autenticação SSH que possam merecer investigação.

A proposta é transformar os eventos observados nas etapas anteriores em critérios objetivos que posteriormente possam ser implementados em Python.

O objetivo não é afirmar automaticamente que determinada sequência representa um ataque. A lógica busca apenas destacar comportamentos potencialmente suspeitos com base em fatores como quantidade de falhas, endereço IP de origem, usuário e intervalo de tempo.

## Eventos considerados

A análise utiliza principalmente três tipos de evento encontrados nos logs do OpenSSH:

```text
Accepted password
Failed password
Failed password for invalid user
```

- `Accepted password`: autenticação realizada com sucesso.
- `Failed password`: tentativa de autenticação malsucedida para um usuário existente.
- `Failed password for invalid user`: tentativa de autenticação utilizando um usuário inexistente.

O evento `Invalid user` também pode aparecer separadamente no log.

Quando ele pertence à mesma tentativa já registrada como `Failed password for invalid user`, não será contabilizado como uma nova tentativa de autenticação.

Isso evita contar duas vezes o mesmo evento.

## Campos relevantes

A análise manual mostrou que os seguintes campos são úteis para interpretar eventos de autenticação:

- timestamp;
- tipo do evento;
- usuário;
- endereço IP de origem;
- porta de origem;
- resultado da autenticação;
- indicação de usuário válido ou inexistente.

Para a primeira versão da detecção, os principais campos serão:

```text
timestamp
IP de origem
usuário
resultado da autenticação
```

Essas informações permitem agrupar eventos relacionados e analisar se várias falhas ocorreram dentro de um intervalo curto de tempo.

## Princípio da detecção

Uma falha de autenticação isolada não representa necessariamente atividade maliciosa.

Um usuário legítimo pode informar uma senha incorreta por diferentes motivos, como erro de digitação, uso de uma senha antiga ou confusão entre credenciais.

Por esse motivo, a análise considera o comportamento de um conjunto de eventos, e não apenas uma linha isolada do log.

A lógica leva em consideração principalmente:

```text
quantidade de falhas
+
IP de origem
+
intervalo de tempo
+
usuários envolvidos
```

## Regra principal

Para a primeira versão do projeto, será utilizada a seguinte regra:

```text
5 ou mais falhas de autenticação
originadas do mesmo endereço IP
dentro de uma janela de 60 segundos
```

Em forma lógica:

```text
falhas >= 5
AND
mesmo IP de origem
AND
intervalo <= 60 segundos
```

Quando esse padrão for identificado, o comportamento será classificado como:

```text
Comportamento potencialmente suspeito
Motivo: múltiplas falhas de autenticação em curto intervalo
```

Essa classificação não significa que um ataque de força bruta foi confirmado.

Ela apenas indica que o comportamento ultrapassou o limite definido pelo projeto e merece investigação.

## Justificativa do limite

Durante a análise manual foram observadas três falhas consecutivas para o usuário `vboxuser`, originadas do mesmo endereço IP e ocorridas em aproximadamente 22 segundos.

Esse comportamento foi produzido manualmente dentro do laboratório e representa uma situação em que múltiplos erros podem ocorrer sem indicar necessariamente atividade maliciosa.

Por isso, para a primeira versão do detector, foi escolhido um limite de cinco falhas em até 60 segundos.

Esse valor é uma heurística criada especificamente para o laboratório.

Ele não representa um padrão universal de segurança e não deve ser interpretado como um limite ideal para ambientes reais.

O objetivo é possuir um critério simples que possa ser testado, compreendido e posteriormente implementado em Python.

## Comportamentos abaixo do limite

Eventos que não atingirem a regra principal continuarão sendo registrados, mas não gerarão alerta.

Exemplos:

```text
1 falha isolada

ou

3 falhas
mesmo IP
mesmo usuário
22 segundos
```

Nesses casos, a interpretação será semelhante a:

```text
Evento de autenticação malsucedida
Nenhum alerta pela regra principal
```

Isso não significa que o evento deve ser ignorado em qualquer contexto, apenas que ele não atende ao critério definido para esta versão do detector.

## Exemplo de comportamento acima do limite

Exemplo:

```text
IP: 192.168.56.1

14:10:01 - Failed password
14:10:09 - Failed password
14:10:18 - Failed password
14:10:26 - Failed password
14:10:35 - Failed password
```

Nesse cenário ocorreram cinco falhas em aproximadamente 34 segundos, todas originadas do mesmo endereço IP.

A lógica deverá identificar esse conjunto como:

```text
[ALERTA] Múltiplas falhas de autenticação SSH

IP de origem: 192.168.56.1
Quantidade de falhas: 5
Janela observada: 34 segundos
Usuários envolvidos: vboxuser
Classificação: comportamento potencialmente suspeito
```

A saída apresenta as evidências encontradas e deixa a interpretação final para a investigação.

## Possíveis evoluções da detecção

A primeira versão utilizará apenas a regra baseada em quantidade de falhas, endereço IP e intervalo de tempo.

Outros padrões poderão ser incorporados posteriormente.

### Tentativas contra múltiplos usuários

Um mesmo endereço IP tentando autenticar com diversos nomes de usuário pode indicar comportamento de descoberta de contas.

Exemplo:

```text
192.168.56.1 -> root
192.168.56.1 -> admin
192.168.56.1 -> suporte
192.168.56.1 -> ubuntu
```

Uma possível regra futura seria:

```text
3 ou mais usuários diferentes
testados pelo mesmo IP
dentro de 60 segundos
```

Esse comportamento continuaria sendo classificado como potencialmente suspeito, e não como ataque confirmado.

### Login bem-sucedido após múltiplas falhas

Também pode ser relevante correlacionar várias falhas com uma autenticação posteriormente aceita.

Exemplo:

```text
14:20:01 - Failed password
14:20:10 - Failed password
14:20:18 - Failed password
14:20:25 - Failed password
14:20:31 - Failed password
14:20:40 - Accepted password
```

Esse padrão não significa necessariamente comprometimento da conta.

Um usuário legítimo pode simplesmente ter informado a senha correta após algumas tentativas incorretas.

Entretanto, quando combinado com outros elementos, como grande quantidade de falhas, endereço IP inesperado ou tentativa contra vários usuários, esse comportamento pode aumentar a relevância da investigação.

## Limitações da regra

A lógica deste projeto é propositalmente simples e foi criada para aprendizado em laboratório.

Diversas situações legítimas podem gerar várias falhas de autenticação, como:

- usuário digitando a senha incorretamente;
- aplicações utilizando credenciais antigas;
- scripts mal configurados;
- alterações recentes de senha;
- problemas de sincronização de credenciais.

Isso pode gerar falsos positivos.

Da mesma forma, um comportamento malicioso pode ocorrer lentamente e permanecer abaixo do limite definido.

Por exemplo, poucas tentativas distribuídas ao longo de várias horas não seriam identificadas pela regra de cinco falhas em 60 segundos.

Isso pode gerar falsos negativos.

Em um ambiente real, a análise poderia considerar também:

- histórico do endereço IP;
- origem da conexão;
- reputação do IP;
- comportamento anterior do usuário;
- horário habitual de acesso;
- quantidade de usuários diferentes testados;
- autenticação bem-sucedida após várias falhas;
- eventos de rede;
- alertas de outras ferramentas;
- contexto e criticidade do ativo.

Por isso, a regra definida neste projeto deve ser entendida apenas como um ponto de partida para estudar correlação de eventos.

## Validação da regra

Antes da implementação em Python, a lógica será validada utilizando dois cenários controlados.

### Cenário abaixo do limite

Já foi observado no laboratório:

```text
3 falhas
mesmo IP
mesmo usuário
aproximadamente 22 segundos
```

Resultado esperado:

```text
Evento registrado
Nenhum alerta pela regra principal
```

### Cenário acima do limite

Será gerado um novo conjunto controlado contendo:

```text
5 ou mais falhas
mesmo IP
intervalo máximo de 60 segundos
```

Resultado esperado:

```text
Comportamento potencialmente suspeito
Alerta pela regra principal
```

A comparação entre os dois cenários permitirá verificar se o critério definido diferencia corretamente eventos abaixo e acima do limite estabelecido.

## Implementação futura

Após a validação da regra, a próxima etapa será automatizar a análise utilizando Python.

A primeira versão do script deverá:

1. ler as linhas do arquivo de log;
2. identificar eventos relevantes de autenticação SSH;
3. extrair timestamp, usuário e endereço IP;
4. diferenciar autenticação bem-sucedida, falha para usuário válido e falha para usuário inexistente;
5. agrupar falhas por endereço IP;
6. ordenar e correlacionar os eventos temporalmente;
7. verificar se cinco ou mais falhas ocorreram dentro de 60 segundos;
8. apresentar as evidências e a classificação encontrada.

A implementação será realizada somente após a validação manual da regra.

Essa sequência mantém a metodologia adotada no projeto: primeiro compreender os eventos, depois definir e testar a lógica e, por fim, automatizar a análise.