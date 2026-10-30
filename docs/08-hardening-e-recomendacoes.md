# 08 — Hardening e Recomendações de Segurança SSH

> **Status: preparação.** Nenhuma alteração de hardening foi comprovada neste documento até o momento. Os resultados serão preenchidos a partir dos testes reais na VM Ubuntu do laboratório.

## Objetivo

Avaliar as configurações efetivas do OpenSSH Server e demonstrar medidas proporcionais de redução de risco, preservando a capacidade de administração da VM.

## Escopo

- Ambiente próprio com Ubuntu e OpenSSH Server na VirtualBox.
- Rede local Host-only para conexão Windows → Ubuntu; sem exposição planejada à internet.
- Avaliação de autenticação por chave pública, acesso do root, métodos de autenticação e limites de tentativas.
- Validação de conectividade e registros antes e depois das mudanças.

## Preparação e cuidados

**Não desative autenticação por senha nem reinicie o SSH antes de comprovar um método alternativo de acesso.** Mantenha o console da VM disponível e uma sessão administrativa aberta durante as alterações. Evite publicar chaves privadas, credenciais ou conteúdo sensível de configuração.

A configuração efetiva pode incluir arquivos em `/etc/ssh/sshd_config.d/`. Por isso, consultar apenas `/etc/ssh/sshd_config` não demonstra necessariamente quais valores estão ativos.

## 1. Coleta da configuração inicial — pendente

Executar no terminal **da VM Ubuntu**, sem alterar as configurações:

```bash
sudo systemctl is-active ssh
sudo /usr/sbin/sshd -t
sudo /usr/sbin/sshd -T | grep -E '^(permitrootlogin|passwordauthentication|pubkeyauthentication|kbdinteractiveauthentication|maxauthtries|authenticationmethods) '
```

Registrar os valores retornados, a data e o estado do serviço. Saídas filtradas são preferíveis à publicação integral de arquivos de configuração.

## 2. Autenticação por chave — pendente

Gerar uma chave **no cliente Windows** (se ainda não existir), instalar somente a parte pública na conta de teste da VM e verificar uma nova conexão por chave. O procedimento exato e os comandos utilizados serão registrados após a execução.

## 3. Avaliação e aplicação das medidas — pendente

Avaliar, de acordo com o estado inicial: restrição de login direto de root, desativação de senha **somente após** comprovar autenticação por chave, ajustes de tentativas e redução de superfície de acesso. Validar a sintaxe com `sshd -t` antes de recarregar o serviço e testar uma nova sessão sem encerrar a antiga.

## 4. Evidências — pendentes

As capturas da etapa devem comprovar o **antes/depois** e os testes de conexão, sem expor material secreto.

## 5. Conclusão — pendente

Será preenchida depois de validar os resultados observados e eventuais limitações do laboratório.
