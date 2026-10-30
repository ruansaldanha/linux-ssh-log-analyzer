# Exemplo de análise humana — registros SSH fictícios

> Este é um **exercício de investigação** baseado em `data/sample-auth.log`, não o registro de um incidente real. Os dados são sintéticos.

## Contexto e fonte

- Fonte: `data/sample-auth.log`, timestamps em UTC (`+00:00`).
- Regra de laboratório: cinco ou mais falhas de autenticação do mesmo IPv4 em até 60 segundos.
- Saída automatizada correspondente: `reports/relatorio-com-alerta.md` e `reports/resultado-com-alerta.csv`.

## Fatos observados

| Horário (UTC) | IP | Evento interpretado |
|---|---|---|
| 16:32:03 | `192.0.2.10` | Uma falha de senha para `vboxuser` |
| 16:32:12 | `192.0.2.10` | Duas mensagens de falha repetidas |
| 16:32:22 | `192.0.2.10` | Uma falha de senha para `vboxuser` |
| 16:32:33 | `192.0.2.10` | Duas mensagens de falha repetidas |
| 16:34:10 | `192.0.2.10` | Autenticação por senha aceita para `vboxuser` |
| 16:35:01 | `192.0.2.20` | Usuário inexistente (`usuario_teste`) |
| 16:35:05 | `192.0.2.20` | Falha de senha do usuário inexistente |

A linha posterior de auditoria do `sudo` não é uma autenticação SSH e não participa da contagem. Foram reconhecidos sete eventos SSH; a contagem total foi de sete falhas.

## Resultado automatizado

O IP `192.0.2.10` atingiu a regra com seis falhas distribuídas em registros separados por 30 segundos. O IP `192.0.2.20` apresentou apenas uma falha. Foi produzido um alerta de **comportamento potencialmente suspeito**, e não uma confirmação de comprometimento.

## Hipóteses a verificar em um ambiente real

- Um usuário legítimo pode ter digitado credenciais incorretas antes de autenticar com sucesso.
- Um script ou ferramenta de automação pode ter utilizado uma senha desatualizada.
- Pode ter ocorrido tentativa de adivinhação de credenciais; a autenticação posterior aumenta a necessidade de contexto, mas não comprova esse cenário.

## Lacunas e limitações

- Não há identificação do responsável pelo IP nem do contexto operacional.
- Não foram correlacionadas outras fontes, como registros de rede, inventário ou histórico de autenticação.
- As repetições agregadas não expõem seus timestamps individuais; a janela de 30 segundos é baseada nos horários visíveis no arquivo.
- A regra automatizada atual não associa explicitamente o sucesso posterior às falhas anteriores.

## Próximos passos recomendados (hipotéticos)

Em uma investigação autorizada, confirmar titularidade do IP, legitimidade do usuário, horário esperado, finalidade do acesso e existência de outros eventos relacionados. Preservar os logs originais e registrar as evidências antes de concluir qualquer comprometimento.

**Conclusão:** o conjunto sintético alcança o limiar definido para investigação. O resultado demonstra detecção e documentação de um indicador, não prova de ataque.
