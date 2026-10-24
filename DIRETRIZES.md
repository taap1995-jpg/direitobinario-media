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


## Hashtags nas publicações — preferência de 24/10/2026

- Incluir hashtags relevantes ao assunto nas legendas de todos os próximos posts de feed, carrosséis e Reels do @direitobinario, além de hashtags da marca quando pertinentes.
- Selecionar poucas hashtags específicas e coerentes com o conteúdo; não prometer aumento de alcance ou engajamento.
- Enviar o caractere literal `#` e conferir a legenda publicada para evitar o erro de exibir `%23`.
- Nos Stories, quando houver hashtags, integrá-las de modo discreto à arte, preservando a legibilidade; não depender de legenda não exibida nesse formato.
- Esta preferência se aplica às novas publicações. Não editar ou republicar posts antigos sem solicitação.


## Skill editorial guion-reel — uso em todas as próximas publicações

Antes de escrever novos posts, carregar `.agents/skills/guion-reel/SKILL.md`, adaptação em português brasileiro da skill confirmada pelo usuário em 24/10/2026. Aplicar abertura clara, desenvolvimento e chamada para ação ao formato escolhido: Reels, carrossel, imagem de feed ou Story. Preservar fontes atuais, rigor jurídico, identidade visual, produção por código, hashtags por assunto e QA.

A adaptação não incorpora alegações sem fonte da versão original sobre algoritmo, duração obrigatória, porcentagens de alcance ou limite universal de hashtags. Instalar uma skill não ativa agendamento. Não alterar ou republicar mídias antigas automaticamente.
