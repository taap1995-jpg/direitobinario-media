# direitobinario-media

Imagens e agendamento dos posts do Instagram @direitobinario.

## Como funciona
- `queue/posts.json`: fila de posts. Só posts com `"status": "approved"` são publicados.
- `.github/workflows/publish.yml`: roda às 09h, 12h e 19h (America/Sao_Paulo) e publica, no máximo, um post por execução.
- `scripts/publish.py`: cria o container, aguarda o processamento, publica e grava o resultado na fila.

## Configuração necessária
Adicione em Settings > Secrets and variables > Actions:
- `IG_USER_ID`: ID da conta Instagram Business
- `IG_ACCESS_TOKEN`: token de acesso da Meta com permissão de publicação de conteúdo

Sem esses segredos, o workflow não publica nada.

## Aprovação
Para liberar um post, troque `"pending_approval"` por `"approved"` no arquivo `queue/posts.json`.
