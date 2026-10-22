# Orquestração multiagente — @direitobinario

## Estado
- Padrão de coordenação documentado: supervisor + estado compartilhado + revisão cruzada.
- Execuções piloto do VLM Run concluídas; são execuções avulsas, não agentes persistentes.
- Publicação real permanece bloqueada até o pipeline ter uma mídia válida e aprovação técnica de qualidade.
- Não declarar automação recorrente ativa até existir gatilho agendado, permissões verificadas e execução observada.

## Fluxo obrigatório
1. **Supervisor** recebe tema, formato, prazo e restrições; cria um identificador único de tarefa e um pacote de contexto.
2. **Pesquisa** busca fontes primárias atuais e registra URL, data, afirmação suportada e trecho de evidência.
3. **Revisor jurídico** confere a redação legal vigente, jurisdição, status de projetos e riscos de aconselhamento individual.
4. **Redação** produz conteúdo em português brasileiro, com tom educativo e objetivo.
5. **Direção de arte** cria mídia com identidade azul-marinho (#0A1628) e dourado (#C9A84C), legível em celular.
6. **QA independente** confere precisão factual, ortografia, legibilidade, proporção, áudio quando aplicável, direitos de uso e legenda.
7. **Supervisor** resolve divergências, devolve itens reprovados para revisão e monta um pacote único: mídia, legenda, fontes, checklist e resultado dos testes.
8. **Publicador** só pode publicar quando todos os gates estiverem aprovados e a mídia estiver acessível ao Instagram.
9. **Verificação pós-publicação** consulta o objeto publicado e guarda permalink, ID, horário e estado em um registro.

## Gates de liberação
- Pesquisa e revisão jurídica: PASS com fontes rastreáveis.
- Arte/áudio: PASS; nenhum arquivo em branco, corrompido ou ilegível.
- Conteúdo: português brasileiro; identidade de marca consistente.
- Auditoria: nota mínima 8/10; erro jurídico/factual crítico implica BLOCK.
- Publicação: conta correta, mídia válida, limite de publicação verificado e nenhum resultado ambíguo de publicação anterior.
- Pós-publicação: permalink confirmado antes de declarar sucesso.

## Estado compartilhado recomendado
`task_id`, `topic`, `format`, `sources[]`, `legal_review`, `draft_caption`, `media_asset`, `qa_score`, `blocking_issues[]`, `approval_status`, `publish_container_id`, `published_media_id`, `permalink`, `published_at`.

## Política de falha
- Se uma ferramenta retornar erro de permissão, quota ou mídia inacessível, interromper o ramo dependente; não simular sucesso.
- Em timeout durante publicação, consultar as mídias recentes antes de tentar novamente para evitar duplicação.
- Manter registro de evidências e comunicar PASS/FAIL/BLOCK com links verificáveis.
- Este documento descreve o contrato operacional; não é, por si só, um agendador ou workflow executável.
