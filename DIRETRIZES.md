# Diretrizes do fluxo de publicação @direitobinario

## Fluxo obrigatório para cada post

1. Pesquisar um tema jurídico ou de IA relevante e confirmar a fonte oficial e a data (ex.: Câmara dos Deputados, Senado, DOU, tribunais).
2. Escrever o JSON do post em `posts/<slug>.json` (título, seções, rodapé com fonte e identificação).
3. Renderizar a arte **sempre por código**: `scripts/make_post_image.py` gera o JPEG 1080x1350 a partir do JSON. Nunca enviar binários de imagem pela API nem usar gerador manual.
4. Commitar o JSON na `main`. O workflow `render-post-images` gera `posts/<slug>.jpg` e commita no repositório.
5. Usar a URL pública `https://raw.githubusercontent.com/taap1995-jpg/direitobinario-media/main/posts/<slug>.jpg` como `image_url` no container do Instagram.
6. Publicar somente na conta `direitobinario` (ID 39241822288794396). Confirmar a identidade antes de qualquer publicação.
7. Confirmar o resultado: ID do container, ID da mídia publicada e permalink. Só considerar concluído após essa confirmação.
8. Registrar data, horário, tema, IDs e permalink.

## Regras

- Repositório público: nunca commitar tokens, segredos ou dados operacionais sensíveis.
- Tokens ficam apenas em Settings > Secrets and variables > Actions.
- Nunca publicar na conta @oabcomtaap (ID 28715383948125805).
- Textos jurídicos: diferenciar fato confirmado, projeto de lei, opinião e previsão. Projeto de lei não é lei.
- Se faltar fonte, data ou arte válida, não publicar: registrar o motivo.

## Agendamento

Horários em America/Sao_Paulo: 08h revisão, 09h, 12h e 19h publicação. Em UTC (Brasil sem horário de verão): 11:00, 12:00, 15:00 e 22:00.
O workflow `publish.yml` publica um post com `status: approved` da `queue/posts.json`. Requer os secrets `IG_USER_ID` e `IG_ACCESS_TOKEN`.
