# Orquestração multiagente — @direitobinario

## Preferência permanente e obrigatória de produção de artes
- Criar todas as artes por programação no GitHub, gerando SVG (e outros formatos quando necessários) por código versionado.
- **Não usar Canva** para criar as artes do @direitobinario, salvo pedido explícito do usuário para mudar esse método.
- Guardar os arquivos no repositório de mídia do projeto, com nomes claros e versão rastreável.
- Fornecer um link verificável para cada arquivo gerado. Distinguir link do arquivo no GitHub (que pode exigir login se o repositório for privado) de uma URL pública de mídia que o Instagram consiga buscar.
- Para publicar pelo Instagram API/Composio, preparar uma URL de mídia publicamente acessível e estável, validar que ela responde com o tipo de arquivo correto e só então enviar. Nunca fingir que um link GitHub privado é publicamente acessível ao Instagram.
- Preferência visual vigente a partir de 26/10/2026: seguir os prints do próprio perfil enviados pelo usuário; fundo preto/azul-marinho escuro, azul elétrico e ciano luminoso, texto branco forte e elementos tecnológicos. Texto das artes em CAIXA ALTA, com frases curtas e leitura confortável no celular; preservar URLs e @direitobinario. A direção anterior em dourado foi substituída para novas peças. Consultar a seção de identidade visual vigente em DIRETRIZES.md. Para temas atuais, verificar fontes primárias; inspiração explicativa sem copiar outros perfis.

## Estado
- Padrão de coordenação documentado: supervisor + estado compartilhado + revisão cruzada.
- Execuções piloto do VLM Run concluídas; são execuções avulsas, não agentes persistentes.
- Publicação real permanece bloqueada até haver mídia válida, URL acessível ao Instagram e aprovação técnica de qualidade.
- Não declarar automação recorrente ativa até existir gatilho agendado, permissões verificadas e execução observada.

## Fluxo obrigatório
1. **Supervisor** recebe tema, formato, prazo e restrições; cria um identificador único de tarefa e pacote de contexto.
2. **Pesquisa** busca fontes primárias atuais e registra URL, data, afirmação suportada e evidência.
3. **Revisor jurídico** confere a redação legal vigente, jurisdição, status de projetos e riscos de aconselhamento individual.
4. **Redação** produz conteúdo em português brasileiro, com tom educativo e objetivo.
5. **Gerador programático** cria SVG por código no repositório GitHub; se o destino exigir raster, renderiza PNG/JPEG a partir do arquivo-fonte versionado.
6. **QA independente** confere precisão factual, ortografia, legibilidade, proporção, áudio quando aplicável, direitos de uso e legenda.
7. **Supervisor** resolve divergências, devolve itens reprovados para revisão e monta um pacote único: fontes, mídia, legenda, checklist e evidências dos testes.
8. **Hospedagem/publicador** torna a mídia acessível por URL pública apropriada e só publica quando todos os gates estiverem aprovados.
9. **Verificação pós-publicação** confirma o objeto publicado e guarda permalink, ID, horário e estado.

## Gates de liberação
- Pesquisa e revisão jurídica: PASS com fontes rastreáveis.
- Arte: PASS; SVG válido, arquivo não vazio, texto legível e, quando necessário, rasterização validada.
- URL de publicação: PASS; acesso externo verificado e MIME type correto.
- Conteúdo: português brasileiro; identidade de marca consistente.
- Auditoria: nota mínima 8/10; erro jurídico/factual crítico implica BLOCK.
- Publicação: conta correta, mídia válida, limite de publicação verificado e nenhum resultado ambíguo de publicação anterior.
- Pós-publicação: permalink confirmado antes de declarar sucesso.

## Estado compartilhado recomendado
`task_id`, `topic`, `format`, `sources[]`, `legal_review`, `draft_caption`, `svg_source_path`, `rendered_media_path`, `public_media_url`, `qa_score`, `blocking_issues[]`, `approval_status`, `publish_container_id`, `published_media_id`, `permalink`, `published_at`.

## Política de falha
- Se uma ferramenta retornar erro de permissão, quota ou mídia inacessível, interromper o ramo dependente; não simular sucesso.
- Em timeout durante publicação, consultar as mídias recentes antes de tentar novamente para evitar duplicação.
- Manter registro de evidências e comunicar PASS/FAIL/BLOCK com links verificáveis.
- Este documento descreve o contrato operacional; não é, por si só, um agendador ou workflow executável.
