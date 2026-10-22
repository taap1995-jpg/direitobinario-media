# Gates do fluxo de publicação — Composio + GitHub

O fluxo de publicação aplica o protocolo operacional antes de qualquer efeito externo. GitHub Actions executa a fila agendada; Composio permanece a camada de orquestração para inspeção, validação de conta/limites e reconciliação do resultado no Instagram. Este arquivo não cria credenciais nem substitui a conexão ativa do Composio.

## Ordem obrigatória
1. Carregar Skills de domínio, automação confiável e orquestração Composio + GitHub.
2. Confirmar repositório, branch, workflows, conta Instagram e estado atual da fila.
3. Validar estrutura da fila, data/hora com fuso, legenda, fontes e score de QA.
4. Exigir `status: "approved"`, `approval_status: "ready"`, `qa_score >= 8`, `sources` não vazio e URL pública direta HTTPS em `raw.githubusercontent.com`.
5. Fazer HEAD da URL de mídia e aceitar apenas JPG/PNG com resposta HTTP válida e tamanho maior que zero.
6. Conferir que `IG_USER_ID` corresponde a `EXPECTED_IG_USER_ID` da conta @direitobinario.
7. Publicar no máximo o item aprovado mais antigo; gravar o ID do container antes da publicação para facilitar reconciliação.
8. Só registrar `published` quando houver ID da mídia e permalink. Em erro ou timeout, não repetir automaticamente; consultar o Instagram primeiro.
9. Persistir o estado da fila mesmo quando a etapa de publicação falhar.
10. Depois da execução, consultar o run do GitHub Actions e, se houve publicação, confirmar a mídia no Instagram pelo ID/permalink.

## Campos exigidos para um item autoaprovado
- `id`, `status: "approved"`, `scheduled_for` em ISO 8601 com fuso explícito.
- `image_url`, `caption`, `sources` (lista de fontes verificáveis).
- `qa_score` (inteiro de 0 a 10, mínimo 8).
- `approval_status: "ready"` após as revisões jurídica/factual, editorial e visual.

A aprovação individual manual não é exigida: o estado `ready` deve representar que as verificações automatizadas e editoriais foram concluídas. Não atribuir esse estado por padrão a conteúdo que ainda não foi revisado.

## Bloqueios conhecidos a resolver antes da primeira publicação
- O item piloto atual está `error` e aponta para uma URL `.png` que não corresponde à arte JPEG renderizada existente.
- Uma execução anterior retornou erro OAuth 190 (token inválido). O secret `IG_ACCESS_TOKEN` deve ser atualizado no GitHub Actions; seu valor nunca deve ser incluído no repositório nem nos logs.
- Uma conexão Composio ativa não atualiza automaticamente os secrets do GitHub Actions.
- Um workflow com `schedule` configurado não prova, sozinho, que a publicação ocorreu; confirmar cada run e o estado final no Instagram.

## Links canônicos
- Diretrizes: [DIRETRIZES.md](../DIRETRIZES.md)
- Orquestração: [AGENT_ORCHESTRATION.md](AGENT_ORCHESTRATION.md)
- Integração: [COMPOSIO_GITHUB_WORKFLOW.md](COMPOSIO_GITHUB_WORKFLOW.md)
- Publicador: [scripts/publish.py](../scripts/publish.py)
- Workflow: [publish.yml](workflows/publish.yml)
