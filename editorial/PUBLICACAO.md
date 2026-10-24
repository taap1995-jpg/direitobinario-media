# Fluxo editorial — Direito Binário

Atualizado em 24/10/2026. Fuso: America/Sao_Paulo. Canal do relatório, das escolhas, das aprovações e das confirmações: o chat “Publicar post sobre democracia”, ID 01a16eb3-e09e-7c21-a5ee-c326b1dbff89. Nenhuma aprovação por e-mail.

## Relatório diário às 08h

Entregar 10 pautas numeradas e identificadas por data. Pesquisar fatos preferencialmente das últimas 24h: tecnologia, IA, desenvolvimento do setor, segurança digital, vazamentos, falhas, fraudes e roubo de dados ou propriedade intelectual, com consequências jurídicas quando pertinentes. Separar fato confirmado, investigação, alegação e análise. Registrar data do evento e publicação, fontes com links, resumo, relevância, abordagem e ressalvas. Se faltarem dez fatos novos verificáveis, complementar com análise atual claramente identificada, sem inventar notícias.

Cada pauta deve permitir escolher Reel, Story, imagem de feed ou carrossel. Recomendar um formato, preservando a escolha do usuário. No chat, oferecer ações clicáveis de continuação quando suportadas; sempre aceitar texto, por exemplo: “Pautas de 26/10: 2 Reel às 9h; 4 carrossel às 12h; 7 feed às 19h”. Não simular botões.

## Aprovação humana única

Uma seleção clara de pauta e formato neste chat autoriza pesquisar, redigir, criar a arte, revisar e publicar essa escolha na data e horário indicados, sem nova aprovação. Seleções semanais mantêm sua validade para as datas definidas. Não selecionar tema em nome do usuário. Na ausência de horário, distribuir pela ordem da escolha nos próximos horários disponíveis e informar a agenda. Mais de três escolhas para o mesmo dia útil ou referências ambíguas exigem definir a distribuição, sem publicar por suposição. Se apenas o tema for escolhido, resolver o formato antes de agendar.

Uma mudança material no fato ou no conteúdo aprovado bloqueia aquela peça e deve ser comunicada. Ajustes de redação, pesquisa complementar, hashtags e criação dentro do tema/formato autorizado não exigem uma segunda aprovação.

## Segunda a sexta

Publicar as escolhas nos horários 09h, 12h e 19h. Horários já passados não autorizam publicação retroativa nem concentração de atrasados. Se não existir escolha para um horário, não publicar e não preencher com pauta escolhida pelo agente.

## Sábado e domingo

Relatório às 08h; aprovação pelo usuário a qualquer hora neste chat. Depois de aprovada, preparar e publicar a escolha durante o mesmo dia, assim que o QA e a mídia estiverem prontos; sem esperar um horário fixo e sem novo aceite. Respeitar horários ou intervalos específicos fornecidos pelo usuário.

## Produção e publicação

Ler .agents/skills/guion-reel/SKILL.md. Usar abertura clara, conteúdo útil e chamada para ação adequada a cada formato. Melhorar a apresentação com base em evidências disponíveis de desempenho; não prometer viralização, inventar métricas nem usar alegações de algoritmo sem fonte.

Português brasileiro, azul-marinho #0A1628 e dourado #C9A84C; arte por programação no GitHub, pouco texto, boa leitura em celular. Não usar Canva nem Cloudinary sem nova orientação. Incluir hashtags temáticas e da marca quando pertinentes; # literal, sem %23. Em Stories, hashtags discretas na arte. Revalidar fontes e fazer QA factual, jurídico e visual antes de publicar.

GitHub guarda fontes, roteiro, arte e estado; Composio/Instagram publica. Confirmar o perfil conectado @direitobinario e obter o identificador de publicação com GET_USER_INFO. Não confundir id scoped com user_id: na verificação de 24/10, user_id de publicação era 17841424809505687 e id scoped era 39241822288794396. Checar novamente se houver mudança de conexão. Conferir cota, mídia pública e posts recentes.

## Fila e estados

Usar exclusivamente editorial/queue.json para este fluxo. Não usar queue/posts.json nem acionar publish.yml como segundo publicador. O workflow legado fica disponível apenas para acionamento manual expressamente solicitado. A fila inicia vazia: esta reorganização não aprova nenhuma pauta.

Cada item contém:
- id único; report_date; topic_id e topic; format (reel, story, feed ou carousel).
- scheduled_for em ISO 8601 com fuso; no fim de semana, data/hora estimada após aprovação, com schedule_mode: after_approval.
- approval: status, approved_at e reference contendo apenas referência da escolha humana; nenhuma transcrição pessoal ou segredo.
- sources com URL, data do evento, data de publicação e checked_at; content_path; media_urls; caption com hashtags.
- qa: status e observações factuais/jurídicas/visuais.
- status: approved, preparing, ready, publishing, published, blocked, missed, cancelled ou verification_required.
- container_id; media_id; permalink; published_at; error, quando aplicáveis.

Somente uma seleção humana clara pode criar approval.status: approved. QA pronto não substitui aprovação. Persistir publishing antes de publicar; guardar container_id e media_id assim que retornados. Em timeout, resultado incerto ou falha após uma escrita, usar verification_required e reconciliar o Instagram antes de nova tentativa. Não repetir automaticamente uma publicação incerta.

Consultar a mídia publicada e confirmar ID, permalink, conta e formato; em carrossel, conferir quantidade e sequência. Atualizar a fila e confirmar neste chat. Falhas ou alterações materiais devem ser informadas com evidências. Nunca declarar concluído apenas porque renderizou a arte.

## Rotinas configuradas

- Automação 3-rascunhos-di-rios-para-direitobinario: relatório diário às 08h, agora com aprovação neste chat.
- Automação 09h-12h-e-19h-publicar-escolhas-aprovadas-direito-bin-rio: publicador de segunda a sexta às 09h, 12h e 19h.
- As respostas humanas neste chat iniciam a preparação e registram as escolhas. Aos fins de semana, também iniciam a publicação sem horário fixo.
- Os gatilhos locais dependem do computador e do aplicativo disponíveis, das conexões ativas e dos limites de execução. Agendamento salvo não prova uma execução futura nem garante pontualidade absoluta.
