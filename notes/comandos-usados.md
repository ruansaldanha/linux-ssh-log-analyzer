## 00 - Ambiente e escopo

### Objetivo

Coletar informações iniciais da máquina virtual Ubuntu utilizada no laboratório.

### Comandos utilizados

```bash
cat /etc/os-release
hostname
whoami
uname -a
ip a
ip route
ping -c 4 google.com
```

### Evidências salvas

```text
images/00-ambiente/01-versao-hostname-usuario-kernel.png
images/00-ambiente/02-interfaces-de-rede.png
images/00-ambiente/03-rota-e-teste-internet.png
```

### Observação

A máquina virtual foi configurada com duas interfaces de rede: uma interface NAT para acesso à internet e uma interface Host-only para comunicação local entre o Windows e o Ubuntu.

A interface NAT identificada foi `enp0s3`, com IP `10.0.2.15/24`.

A interface Host-only identificada foi `enp0s8`, com IP `192.168.56.102/24`.

O teste de conectividade com `ping google.com` retornou resposta com 0% de perda de pacotes, confirmando que a VM estava com acesso à internet.

---

## 01 - Fundamentos de SSH

### Objetivo

Instalar e verificar o funcionamento do OpenSSH Server na máquina virtual Ubuntu.

Nesta etapa, o objetivo foi confirmar que o serviço SSH estava instalado, ativo, escutando na porta padrão 22 e acessível tanto localmente quanto a partir do Windows pela interface Host-only.

### Comandos utilizados

```bash
sudo apt update
sudo apt install openssh-server -y
apt list --installed openssh-server
systemctl status ssh
sudo ss -tulnp 'sport = :22'
ssh vboxuser@localhost
```

No Windows PowerShell, foi utilizado:

```powershell
ssh vboxuser@192.168.56.102
```

### Evidências salvas

```text
images/01-ssh/01-openssh-server-instalado.png
images/01-ssh/02-status-servico-ssh.png
images/01-ssh/03-porta-22-escutando.png
images/01-ssh/04-teste-ssh-localhost.png
images/01-ssh/05-teste-ssh-windows-host-only.png
```

### Observação

O OpenSSH Server foi instalado na VM Ubuntu e o serviço `ssh.service` foi confirmado como ativo.

A porta 22 foi verificada com o comando `ss`, indicando que havia um serviço escutando conexões TCP na porta padrão do SSH.

Também foram realizados dois testes de conexão:

- conexão local usando `ssh vboxuser@localhost`;
- conexão remota a partir do Windows usando o IP Host-only da VM: `192.168.56.102`.

Na primeira conexão feita pelo Windows, foi exibido o aviso de autenticidade do host. Esse comportamento é esperado em conexões SSH iniciais, pois o cliente ainda não conhece a chave do servidor.

---

## 02 - Logs de autenticação no Linux

### Objetivo

Localizar os logs de autenticação do Ubuntu e observar como eventos relacionados ao SSH aparecem nos registros do sistema.

Nesta etapa, foram comparados o arquivo `/var/log/auth.log` e os registros do serviço SSH utilizando `journalctl`.

### Comandos utilizados

Verificar se o arquivo de autenticação existe:

```bash
ls -lh /var/log/auth.log
```

Consultar as últimas 30 linhas do `auth.log`:

```bash
sudo tail -n 30 /var/log/auth.log
```

Consultar os últimos registros do serviço SSH:

```bash
sudo journalctl -u ssh --no-pager -n 30
```

Consultar todos os registros disponíveis do serviço SSH:

```bash
sudo journalctl -u ssh --no-pager
```

Buscar registros contendo `sshd` no `auth.log`:

```bash
sudo grep "sshd" /var/log/auth.log
```

Buscar registros contendo `Accepted` no `auth.log`:

```bash
sudo grep "Accepted" /var/log/auth.log
```

Buscar registros contendo `Failed` no `auth.log`:

```bash
sudo grep "Failed" /var/log/auth.log
```

Filtrar eventos de autenticação aceita diretamente no journal do SSH:

```bash
sudo journalctl -u ssh --no-pager | grep "Accepted"
```

### Evidências salvas

```text
images/02-logs/01-localizacao-auth-log.png
images/02-logs/02-ultimas-linhas-auth-log.png
images/02-logs/03-logs-ssh-journalctl.png
```

### Observação

O arquivo `/var/log/auth.log` contém eventos relacionados a diferentes componentes do sistema, e não apenas ao SSH.

Durante a análise, foram encontrados registros de componentes como `gdm-password`, `sudo`, `cron`, `pkexec`, `systemd` e `sshd`.

Isso mostrou que buscas simples por palavras como `Failed` ou `Accepted` podem gerar resultados que não correspondem a eventos de autenticação SSH.

Um exemplo foi a busca por `Failed`, que retornou uma mensagem do `dbus-daemon` relacionada à inicialização de um serviço. Também apareceram registros do próprio `sudo` utilizados para executar os comandos de análise.

Já o comando `journalctl -u ssh` permitiu consultar diretamente os registros do serviço SSH.

Entre os eventos observados estavam:

```text
Server listening on 0.0.0.0 port 22.
Server listening on :: port 22.
Accepted password for vboxuser from ::1 port 36392 ssh2
Accepted password for vboxuser from 192.168.56.1 port 53486 ssh2
```

Os dois eventos de autenticação bem-sucedida puderam ser relacionados aos testes realizados anteriormente:

```text
ssh vboxuser@localhost
```

e:

```powershell
ssh vboxuser@192.168.56.102
```

O endereço `::1` corresponde ao loopback IPv6 da própria máquina. Já o endereço `192.168.56.1` corresponde à origem da conexão do Windows pela rede Host-only.

Essas observações mostraram que o contexto do evento é importante para diferenciar registros relevantes de possíveis falsos positivos.

---

## 03 - Geração de eventos controlados

### Objetivo

Gerar eventos de autenticação SSH conhecidos em um ambiente controlado para observar como diferentes situações são registradas no `/var/log/auth.log`.

Foram testados quatro cenários: autenticação bem-sucedida, senha incorreta para um usuário válido, tentativa com usuário inexistente e múltiplas falhas consecutivas de autenticação.

### Comandos utilizados

Acompanhar o arquivo de autenticação em tempo real no Ubuntu:

```bash
sudo tail -f /var/log/auth.log
```

Realizar uma conexão SSH a partir do Windows com o usuário válido:

```powershell
ssh vboxuser@192.168.56.102
```

Esse comando foi utilizado tanto para o login bem-sucedido quanto para os testes com senha incorreta e múltiplas falhas consecutivas.

Encerrar uma sessão SSH autenticada:

```bash
exit
```

Realizar uma tentativa de autenticação utilizando um usuário inexistente:

```powershell
ssh usuario_teste@192.168.56.102
```

### Evidências salvas

```text
images/03-eventos-controlados/01-login-ssh-bem-sucedido.png
images/03-eventos-controlados/02-senha-incorreta.png
images/03-eventos-controlados/03-usuario-inexistente.png
images/03-eventos-controlados/04-multiplas-tentativas-falhas.png
```

### Observação

No cenário de autenticação bem-sucedida, o `sshd` registrou um evento `Accepted password`, seguido pela abertura da sessão do usuário.

No cenário de senha incorreta para o usuário válido `vboxuser`, foi registrado o evento `Failed password for vboxuser`.

No cenário com o usuário inexistente `usuario_teste`, foram observados registros como `Invalid user usuario_teste` e `Failed password for invalid user usuario_teste`.

Durante o teste de múltiplas falhas consecutivas, três senhas incorretas foram informadas dentro da mesma conexão SSH. Após o limite de tentativas daquela conexão, o cliente exibiu `Permission denied (publickey,password)` e retornou ao PowerShell. Esse comportamento não significou bloqueio permanente do usuário; uma nova execução do comando `ssh` poderia iniciar outra conexão.

Os eventos gerados nesta etapa serviram como base conhecida para a análise manual realizada na etapa seguinte.

---

## 04 - Análise manual dos logs

### Objetivo

Analisar manualmente os eventos de autenticação SSH gerados anteriormente, identificando padrões, informações relevantes e diferenças entre os tipos de evento antes da implementação da análise automatizada em Python.

### Filtrar eventos relevantes do SSH

Exibe eventos relacionados ao `sshd` contendo autenticação bem-sucedida, falha de senha ou tentativa com usuário inválido.

```bash
sudo grep "sshd" /var/log/auth.log | grep -E "Accepted password|Failed password|Invalid user"
```

### Contar autenticações bem-sucedidas

```bash
sudo grep "sshd" /var/log/auth.log | grep "Accepted password" | wc -l
```

Resultado observado no laboratório:

```text
1
```

### Contar todas as falhas de senha

```bash
sudo grep "sshd" /var/log/auth.log | grep "Failed password" | wc -l
```

Resultado observado no laboratório:

```text
5
```

### Contar falhas envolvendo usuário inexistente

```bash
sudo grep "sshd" /var/log/auth.log | grep "Failed password for invalid user" | wc -l
```

Resultado observado no laboratório:

```text
1
```

### Contar falhas para o usuário válido `vboxuser`

```bash
sudo grep "sshd" /var/log/auth.log | grep "Failed password for vboxuser" | wc -l
```

Resultado observado no laboratório:

```text
4
```

### Extrair os endereços IP de origem dos eventos de autenticação

O comando procura o campo `from` e imprime o valor imediatamente seguinte, que corresponde ao endereço IP de origem.

```bash
sudo grep "sshd" /var/log/auth.log | grep -E "Accepted password|Failed password" | awk '{for(i=1;i<=NF;i++) if($i=="from") print $(i+1)}'
```

Resultado observado:

```text
192.168.56.1
192.168.56.1
192.168.56.1
192.168.56.1
192.168.56.1
192.168.56.1
```

### Agrupar e contar eventos por endereço IP

```bash
sudo grep "sshd" /var/log/auth.log | grep -E "Accepted password|Failed password" | awk '{for(i=1;i<=NF;i++) if($i=="from") print $(i+1)}' | sort | uniq -c
```

Resultado observado:

```text
6 192.168.56.1
```

### Extrair os usuários envolvidos nos eventos

O comando trata separadamente o formato utilizado para usuários válidos e o formato `invalid user`, evitando interpretar a palavra `invalid` como nome de usuário.

```bash
sudo grep "sshd" /var/log/auth.log | grep -E "Accepted password|Failed password" | awk '{for(i=1;i<=NF;i++) {if($i=="for") {if($(i+1)=="invalid" && $(i+2)=="user") print $(i+3); else print $(i+1);}}}'
```

Resultado observado:

```text
vboxuser
vboxuser
usuario_teste
vboxuser
vboxuser
vboxuser
```

### Agrupar e contar eventos por usuário

```bash
sudo grep "sshd" /var/log/auth.log | grep -E "Accepted password|Failed password" | awk '{for(i=1;i<=NF;i++) {if($i=="for") {if($(i+1)=="invalid" && $(i+2)=="user") print $(i+3); else print $(i+1);}}}' | sort | uniq -c
```

Resultado observado:

```text
1 usuario_teste
5 vboxuser
```

Os cinco eventos associados a `vboxuser` correspondem a uma autenticação bem-sucedida e quatro falhas de autenticação. O evento associado a `usuario_teste` corresponde a uma tentativa utilizando um usuário inexistente.

### Exibir as três últimas falhas consecutivas do usuário `vboxuser`

```bash
sudo grep "sshd" /var/log/auth.log | grep "Failed password for vboxuser" | tail -n 3
```

Esse comando foi utilizado para analisar as três falhas consecutivas geradas durante o cenário controlado.

### Extrair somente os timestamps das três últimas falhas

```bash
sudo grep "sshd" /var/log/auth.log | grep "Failed password for vboxuser" | tail -n 3 | awk '{print $1}'
```

Timestamps observados:

```text
2026-09-06T14:09:08.771769+00:00
2026-09-06T14:09:22.289644+00:00
2026-09-06T14:09:30.816198+00:00
```

Entre a primeira e a terceira falha decorreram aproximadamente 22 segundos.

### Evidências salvas

```text
images/04-analise-manual/01-eventos-ssh-filtrados.png
images/04-analise-manual/02-contagem-eventos.png
images/04-analise-manual/03-contagem-por-ip.png
images/04-analise-manual/04-usuarios-extraidos.png
images/04-analise-manual/05-contagem-por-usuario.png
images/04-analise-manual/06-analise-temporal-falhas.png
```

### Comandos e operadores utilizados nesta etapa

- `grep`: localiza linhas que correspondem a determinado texto ou padrão.
- `grep -E`: permite utilizar expressões com alternativas, como `Accepted password|Failed password`.
- `wc -l`: conta a quantidade de linhas recebidas.
- `awk`: processa os campos de cada linha e permite extrair informações específicas, como endereço IP, usuário ou timestamp.
- `sort`: ordena os resultados, fazendo com que valores iguais fiquem agrupados.
- `uniq -c`: conta quantas vezes cada valor agrupado aparece.
- `tail -n 3`: exibe somente as três últimas linhas do resultado.
- `|`: envia a saída de um comando para a entrada do comando seguinte.
- `NF`: no `awk`, representa a quantidade total de campos da linha.
- `$i`: representa o campo atualmente analisado pelo `awk`.
- `$(i+1)`: representa o campo imediatamente posterior ao campo atual.

### Observações da análise

O arquivo `/var/log/auth.log` contém registros de autenticação de diferentes serviços, por isso o filtro por `sshd` foi utilizado para restringir a análise aos eventos relacionados ao SSH.

Uma única tentativa de autenticação pode gerar mais de uma linha no log. Uma tentativa utilizando um usuário inexistente, por exemplo, pode gerar tanto um evento `Invalid user` quanto um evento `Failed password for invalid user`.

Por esse motivo, a quantidade de linhas encontradas no log não deve ser interpretada automaticamente como a quantidade de tentativas de autenticação.

Também foi observado que diferentes tipos de evento possuem formatos diferentes. Em uma falha envolvendo um usuário existente, o padrão pode ser:

```text
Failed password for vboxuser from 192.168.56.1
```

Enquanto uma tentativa envolvendo um usuário inexistente pode aparecer como:

```text
Failed password for invalid user usuario_teste from 192.168.56.1
```

Essa diferença deverá ser considerada posteriormente durante a implementação do parser em Python.

A análise temporal mostrou três falhas consecutivas para `vboxuser`, originadas de `192.168.56.1`, dentro da mesma conexão SSH e em aproximadamente 22 segundos. Esse comportamento, isoladamente, não é suficiente para concluir que houve um ataque de força bruta, pois um usuário legítimo também pode gerar várias falhas consecutivas ao informar uma senha incorreta.

Os principais campos identificados como úteis para a automação posterior são: timestamp, tipo de evento, usuário, endereço IP de origem, porta de origem, resultado da autenticação e indicação de usuário válido ou inexistente.
