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