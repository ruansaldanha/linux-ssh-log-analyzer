# Relatorio de Investigacao - SSH

## Informacoes da analise

- Arquivo analisado: `teste-multiplos-ips.log`
- Data da analise: 2026-10-30T16:21:49-03:00
- Eventos SSH reconhecidos: 8
- Falhas contabilizadas: 7
- IPs com falhas: 3
- Alertas identificados: 0

## Regra de deteccao

Cinco ou mais falhas de autenticacao do mesmo IP em uma janela de ate 60 segundos.

## Contagem de falhas por IP

| IP de origem | Total de falhas |
|---|---:|
| 192.0.2.40 | 3 |
| 192.0.2.50 | 3 |
| 192.0.2.60 | 1 |

## Alertas identificados

Nenhum comportamento suspeito identificado pela regra atual.

## Observacoes e limitacoes

- Os alertas indicam comportamentos que merecem investigacao, nao ataques confirmados.
- Mensagens agrupadas sao contabilizadas usando o horario do respectivo registro.
- A implementacao gera somente o primeiro alerta por IP.
- Os resultados dependem dos formatos de log reconhecidos pelo analisador.

## Conclusao automatica

Nenhum endereco IP atingiu o criterio de deteccao nos registros analisados. Isso nao garante a ausencia de atividade maliciosa.
