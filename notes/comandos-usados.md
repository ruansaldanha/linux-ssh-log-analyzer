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
sudo grep sshd /var/log/auth.log
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
