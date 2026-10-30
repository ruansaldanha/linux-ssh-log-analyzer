# Relatorio de Investigacao - SSH

## Informacoes da analise

- Arquivo analisado: `sample-auth.log`
- Data da analise: 2026-10-30T16:19:05-03:00
- Eventos SSH reconhecidos: 7
- Falhas contabilizadas: 7
- IPs com falhas: 2
- Alertas identificados: 1

## Regra de deteccao

Cinco ou mais falhas de autenticacao do mesmo IP em uma janela de ate 60 segundos.

## Contagem de falhas por IP

| IP de origem | Total de falhas |
|---|---:|
| 192.0.2.10 | 6 |
| 192.0.2.20 | 1 |

## Alertas identificados

| IP | Falhas na janela | Intervalo (s) | Classificacao |
|---|---:|---:|---|
| 192.0.2.10 | 6 | 30.00 | Potencialmente suspeito |

## Observacoes e limitacoes

- Os alertas indicam comportamentos que merecem investigacao, nao ataques confirmados.
- Mensagens agrupadas sao contabilizadas usando o horario do respectivo registro.
- A implementacao gera somente o primeiro alerta por IP.
- Os resultados dependem dos formatos de log reconhecidos pelo analisador.

## Conclusao automatica

Foram identificados 1 endereco(s) IP que atingiram o criterio de deteccao. Recomenda-se examinar os registros correspondentes e considerar o contexto das autenticacoes.
