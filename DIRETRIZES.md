# Diretrizes do fluxo de publicação @direitobinario

## Identidade visual vigente — a partir de 26/10/2026

Preferência expressa pelo usuário em 26/10/2026, com base nos três prints do próprio perfil enviados na conversa. Aplica-se às novas artes de feed, carrossel, Stories e Reels produzidas a partir desta data.

- Fundo preto ou azul-marinho muito escuro, com azul elétrico e ciano luminoso nos destaques. Branco de alto contraste nos textos. Essa direção substitui a orientação anterior de azul-marinho e dourado para novas artes.
- Aparência tecnológica: linhas de circuito, molduras finas, pontos luminosos, redes digitais e imagens de tecnologia relacionadas ao tema. Usar esses elementos com equilíbrio, preservando áreas de leitura.
- Títulos grandes, fortes e preferencialmente com tipografia condensada; composição com hierarquia clara, como nas referências enviadas.
- Texto visível das artes em CAIXA ALTA, inclusive chamadas e textos de apoio. Preservar acentos e grafia correta. Não converter URLs nem o identificador @direitobinario, para não alterar referências funcionais.
- Frases curtas, poucas palavras por tela, espaçamento adequado e margens seguras. Não reduzir a fonte para encaixar parágrafos: resumir ou dividir o conteúdo. Em Reels, manter tempo suficiente de leitura.
- Assinatura @direitobinario e identidade de Direito & Tecnologia consistentes. Manter as fontes verificáveis nas peças ou na legenda, conforme o formato.
- Legendas das publicações continuam com escrita natural em português brasileiro; o pedido de caixa alta refere-se à apresentação visual das artes.
- Paleta técnica de referência aproximada: fundo #030915 ou #071426; azul #167BD1; ciano #00C8EF; branco #FFFFFF. As referências visuais enviadas prevalecem sobre estes valores aproximados.
- Na revisão visual, conferir aderência às referências, CAIXA ALTA, contraste, ortografia, tamanho da fonte, margens e tempo de leitura.
- Esta atualização modifica o padrão das novas peças; não implica editar, excluir ou republicar conteúdo já publicado.

## Fluxo obrigatório para cada post

1. Pesquisar um tema jurídico ou de IA relevante e confirmar a fonte oficial e a data (ex.: Câmara dos Deputados, Senado, DOU, tribunais).
2. Escrever o JSON do post em `posts/<slug>.json` (título, seções, rodapé com fonte e identificação).
3. Renderizar a arte **sempre por código**: `scripts/make_post_image.py` gera o JPEG 1080x1350 a partir do JSON. Nunca enviar binários de imagem pela API nem usar gerador manual.
4. Commitar o JSON na `main`. O workflow `render-post-images` gera `posts/<slug>.jpg` e commita no repositório.
5. Usar a URL pública `https://raw.githubusercontent.com/taap1995-jpg/direitobinario-media/main/posts/<slug>.jpg` como `image_url` no container do Instagram.
6. Publicar somente na conta `direitobinario`. Confirmar a identidade com GET_USER_INFO e usar o user_id de publicação retornado (17841424809505687 na última verificação); não confundir com o id scoped 39241822288794396.
7. Confirmar o resultado: ID do container, ID da mídia publicada e permalink. Só considerar concluído após essa confirmação.
8. Registrar data, horário, tema, IDs e permalink.

## Regras

- Repositório público: nunca commitar tokens, segredos ou dados operacionais sensíveis.
- Tokens ficam apenas em Settings > Secrets and variables > Actions.
- Nunca publicar na conta @oabcomtaap (ID 28715383948125805).
- Textos jurídicos: diferenciar fato confirmado, projeto de lei, opinião e previsão. Projeto de lei não é lei.
- Se faltar fonte, data ou arte válida, não publicar: registrar o motivo.

## Agendamento

O fluxo vigente está em `editorial/PUBLICACAO.md`: relatório às 08h todos os dias, aprovação exclusivamente no chat, publicações aprovadas às 09h/12h/19h de segunda a sexta e após aprovação a qualquer hora nos fins de semana. A fila ativa é `editorial/queue.json`; não usar a fila legada como publicador paralelo.

## Hashtags nas publicações — preferência de 24/10/2026

- Incluir hashtags relevantes ao assunto nas legendas de todos os próximos posts de feed, carrosséis e Reels do @direitobinario, além de hashtags da marca quando pertinentes.
- Selecionar poucas hashtags específicas e coerentes com o conteúdo; não prometer aumento de alcance ou engajamento.
- Enviar o caractere literal `#` e conferir a legenda publicada para evitar o erro de exibir `%23`.
- Nos Stories, quando houver hashtags, integrá-las de modo discreto à arte, preservando a legibilidade; não depender de legenda não exibida nesse formato.
- Esta preferência se aplica às novas publicações. Não editar ou republicar posts antigos sem solicitação.


## Skill editorial guion-reel — uso em todas as próximas publicações

Antes de escrever novos posts, carregar `.agents/skills/guion-reel/SKILL.md`, adaptação em português brasileiro da skill confirmada pelo usuário em 24/10/2026. Aplicar abertura clara, desenvolvimento e chamada para ação ao formato escolhido: Reels, carrossel, imagem de feed ou Story. Preservar fontes atuais, rigor jurídico, identidade visual, produção por código, hashtags por assunto e QA.

A adaptação não incorpora alegações sem fonte da versão original sobre algoritmo, duração obrigatória, porcentagens de alcance ou limite universal de hashtags. Instalar uma skill não ativa agendamento. Não alterar ou republicar mídias antigas automaticamente.
