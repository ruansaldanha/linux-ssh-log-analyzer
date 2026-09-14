# 03 - Geração de Eventos Controlados

## Objetivo

Nesta etapa foram gerados eventos de autenticação SSH de forma controlada para observar como diferentes situações são registradas no `/var/log/auth.log`.

As conexões foram iniciadas a partir do Windows e direcionadas à máquina virtual Ubuntu pela rede Host-only.

O objetivo foi produzir eventos conhecidos antes da análise manual, permitindo relacionar cada ação realizada ao respectivo registro gerado pelo `sshd`.

## Ambiente utilizado

- Cliente SSH: Windows
- Servidor SSH: Ubuntu
- Serviço: OpenSSH Server (`sshd`)
- Usuário válido: `vboxuser`
- Usuário inexistente utilizado no teste: `usuario_teste`
- IP do servidor Ubuntu: `192.168.56.102`
- IP de origem das conexões: `192.168.56.1`
- Rede utilizada: Host-only

Durante os testes, o arquivo de autenticação foi acompanhado em tempo real com:

```bash
sudo tail -f /var/log/auth.log
```

A opção `-f` mantém o acompanhamento do arquivo e exibe novas linhas à medida que os eventos são registrados.

## Cenário 1 — Autenticação bem-sucedida

No Windows PowerShell, foi iniciada uma conexão SSH utilizando o usuário válido:

```powershell
ssh vboxuser@192.168.56.102
```

Após informar a senha correta, a autenticação foi concluída com sucesso.

No `auth.log`, foi observado um evento semelhante a:

```text
Accepted password for vboxuser from 192.168.56.1 port 50795 ssh2
```

Também foram registrados eventos relacionados à abertura e ao encerramento da sessão.

Esse cenário permitiu identificar `Accepted password` como um dos principais padrões associados a uma autenticação SSH bem-sucedida.

### Evidência

```text
images/03-eventos-controlados/01-login-ssh-bem-sucedido.png
```

## Cenário 2 — Senha incorreta para usuário válido

Foi iniciada uma nova conexão utilizando o mesmo usuário:

```powershell
ssh vboxuser@192.168.56.102
```

Dessa vez, foi informada uma senha incorreta.

O `auth.log` registrou um evento semelhante a:

```text
Failed password for vboxuser from 192.168.56.1 port 64525 ssh2
```

Também foram observados registros do PAM relacionados à falha de autenticação.

Esse cenário mostrou o padrão utilizado pelo `sshd` quando uma tentativa falha para um usuário existente.

### Evidência

```text
images/03-eventos-controlados/02-senha-incorreta.png
```

## Cenário 3 — Tentativa com usuário inexistente

Foi realizada uma tentativa utilizando um usuário que não existe no sistema:

```powershell
ssh usuario_teste@192.168.56.102
```

Foram observadas linhas como:

```text
Invalid user usuario_teste from 192.168.56.1
```

e:

```text
Failed password for invalid user usuario_teste from 192.168.56.1
```

Esse cenário mostrou que uma única tentativa de autenticação pode produzir mais de uma linha relacionada no log.

Também foi possível observar que a estrutura do evento para um usuário inexistente é diferente da estrutura encontrada em uma falha de senha para um usuário válido.

Essa diferença será importante durante a análise e, posteriormente, na implementação do parser.

### Evidência

```text
images/03-eventos-controlados/03-usuario-inexistente.png
```

## Cenário 4 — Múltiplas falhas consecutivas

Foi iniciada outra conexão com o usuário válido:

```powershell
ssh vboxuser@192.168.56.102
```

Durante a mesma conexão, foram informadas três senhas incorretas consecutivas.

O `auth.log` registrou três eventos `Failed password` associados ao mesmo usuário, endereço IP de origem, porta e processo `sshd`.

Após as tentativas malsucedidas, a conexão foi encerrada e o cliente SSH apresentou:

```text
Permission denied (publickey,password)
```

Esse comportamento não representou um bloqueio permanente da conta.

Uma nova execução do comando `ssh` permitiu iniciar outra conexão normalmente.

As três falhas ocorreram dentro da mesma sessão de tentativa de autenticação e foram utilizadas posteriormente na análise temporal da Etapa 04.

### Evidência

```text
images/03-eventos-controlados/04-multiplas-tentativas-falhas.png
```

## Eventos observados

Os testes produziram os seguintes padrões principais:

```text
Accepted password
Failed password
Invalid user
Failed password for invalid user
```

Esses eventos permitem diferenciar:

- autenticação bem-sucedida;
- falha de autenticação para usuário válido;
- tentativa envolvendo usuário inexistente.

É importante observar que nem toda linha registrada representa uma tentativa independente de autenticação.

Uma tentativa com usuário inexistente, por exemplo, pode produzir tanto `Invalid user` quanto `Failed password for invalid user`.

## Aprendizados

A geração controlada dos eventos permitiu relacionar diretamente comportamentos conhecidos aos registros produzidos pelo sistema.

Os principais aprendizados desta etapa foram:

- `Accepted password` indica uma autenticação SSH concluída com sucesso;
- `Failed password` registra uma falha de autenticação;
- tentativas envolvendo usuários inexistentes possuem uma estrutura diferente;
- uma única tentativa pode gerar várias linhas relacionadas no log;
- múltiplas falhas consecutivas podem ocorrer dentro da mesma conexão SSH;
- várias falhas em sequência não são suficientes, isoladamente, para confirmar comportamento malicioso.

A partir desses eventos, a etapa seguinte realiza a análise manual dos registros para extrair informações como usuário, endereço IP, resultado da autenticação e relação temporal entre as tentativas.