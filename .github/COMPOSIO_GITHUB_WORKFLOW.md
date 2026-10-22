# Protocolo de trabalho integrado: Composio + GitHub

## Propósito
Composio coordena e executa ferramentas de aplicativos; GitHub mantém código, configuração, documentação e histórico versionado. Este documento é um procedimento operacional, não um agendador nem um agente persistente.

## Ciclo padrão
1. **Contexto:** carregue a Skill de domínio relevante e **Orquestração Composio + GitHub**; carregue **Automação Confiável e Melhoria Contínua** para tarefas de automação.
2. **Descoberta:** pesquise ferramentas para cada app citado no Composio. Use somente slugs retornados pela pesquisa, leia schemas completos e confirme conexões ativas. Se houver mais de uma conta, selecione o alias explicitamente.
3. **Inspeção:** confirme usuário, repositório, branch padrão, caminhos, estado dos arquivos, workflows, permissões e resultados recentes. Leia antes de editar.
4. **Plano:** separe ações independentes das dependentes. Não execute uma etapa antes de obter IDs, URLs, conteúdo ou estados necessários da anterior.
5. **Mudança:** para alterações relacionadas em múltiplos arquivos, prefira um commit atômico. Use branch/PR quando necessário. Nunca force sobrescrita de trabalho, exponha tokens ou amplie permissões sem motivo.
6. **Validação:** valide esquema dos dados transferidos entre ferramentas, sintaxe/configuração, formatos de mídia, URLs e fuso horário. Use timeouts e retries limitados; para efeitos externos, confirme o estado antes de repetir após timeout.
7. **Execução:** dispare o workflow apenas quando as pré-condições estiverem satisfeitas. Verifique o run específico e aguarde o resultado final; em falha, examine logs, corrija a causa e teste novamente.
8. **Reconciliação:** para ações como publicar conteúdo, confirme o resultado na plataforma de destino. Um arquivo de workflow ou resposta intermediária não prova publicação nem agendamento ativo.
9. **Memória:** atualize `.github/PROJECT_MEMORY.md` e/ou `.github/AGENT_ORCHESTRATION.md` quando houver decisões operacionais duráveis, sem guardar valores secretos.
10. **Relato:** entregue links diretos para arquivos, commit e execução; diferencie alteração feita, teste aprovado, tarefa executada e automação ativa. Declare apenas o que foi verificado.

## Regras de resiliência
- IDs de tarefa e chaves de idempotência quando suportados.
- Retries limitados com backoff para falhas transitórias; sem repetição cega de ações com efeitos colaterais.
- Logs úteis, sem tokens, credenciais ou dados pessoais desnecessários.
- Permissões mínimas em GitHub Actions e uso de GitHub Secrets para valores secretos.
- Interromper o ramo dependente em caso de falha de autenticação, permissão, quota ou artefato inválido; registrar o bloqueio e continuar apenas tarefas independentes.

## Checklist antes de concluir
- [ ] Conta/alias e repositório confirmados.
- [ ] Schemas e entradas validados.
- [ ] Arquivos e diff conferidos.
- [ ] Commit e caminhos alterados confirmados.
- [ ] Workflow/teste com resultado terminal verificado.
- [ ] Resultado externo confirmado, se aplicável.
- [ ] Memória atualizada quando necessário.
- [ ] Links e limitações reais informados.
