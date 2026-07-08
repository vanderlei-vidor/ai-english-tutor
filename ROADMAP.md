# Roadmap

Este roadmap organiza os proximos passos do projeto com foco em evoluir o
`Teacher Brain` sem regressao. A regra principal e simples: o backend decide a
pedagogia, o LLM executa a resposta.

## Estado Atual

### Concluido

- Chat com IA integrado ao backend.
- Sistema de memoria do usuario.
- Feedback gramatical e cards no frontend.
- XP, streak, badges, ranking semanal e ligas.
- Estimativa CEFR e estruturas avancadas.
- Grammar Engine novo em shadow mode.
- Pipeline inicial `Grammar -> Pedagogical -> Teacher -> Conversation -> Prompt`.
- `TeacherEngine` inicial com `CorrectionStrategy` e `ConversationStrategy`.
- Sanitizer preservando erro confirmado pelo Grammar Engine.

### Em Andamento

- Migracao gradual da logica pedagogica antiga para `backend/app/services/teacher`.
- Separacao entre estado pedagogico (`PedagogicalAnalysis`) e conteudo de aula.
- Reducao de decisoes duplicadas entre `TeacherEngine` e `chat_service.generate_response`.
- Estrutura de pastas do `teacher` criada, com varios arquivos ainda vazios.

## Principios Anti-Regressao

- Uma fase por vez, sempre mantendo o backend atual funcionando.
- Nunca apagar logica antiga antes de rodar em shadow mode.
- O Grammar Engine tem prioridade sobre decisoes fragis do LLM.
- O sanitizer pode bloquear falso positivo do LLM, mas nao deve apagar erro confirmado pelo Grammar.
- `TeacherEngine` deve decidir; `generate_response` deve executar.
- Toda mudanca deve passar por `python -m compileall backend/app`.
- Para cada fase, validar pelo menos:
  - frase correta continua como `chat`;
  - erro gramatical real continua como `correction`;
  - falso rewrite continua sendo bloqueado;
  - memoria nao registra skill errada.

## Arquitetura Alvo Do Teacher

```text
TeacherContext
    -> decision/engine.py
    -> decision/*
    -> registry.py
    -> strategies/*
    -> teaching/* ou exercise/* ou personality/*
    -> TeacherDecision / TeacherOutput
    -> PromptContext
    -> LLM executor
```

## Fase 1: Contrato Central Do Teacher

Objetivo: deixar os modelos e o contexto estaveis antes de preencher as pastas vazias.

Arquivos:

- `backend/app/services/teacher/models.py`
- `backend/app/services/teacher/context.py`
- `backend/app/services/teacher/engine.py`
- `backend/app/services/teacher/logger.py`

Passos:

1. Consolidar `TeacherIntent` e `TeacherDecision` como contrato oficial.
2. Criar `TeacherOutput` somente se a decisao comecar a carregar conteudo pronto.
3. Expandir `TeacherContext` com campos seguros:
   - `user_text`
   - `memory_data`
   - `conversation_turns`
   - `messages_since_last_teaching`
   - `english_level`
4. Garantir que `TeacherEngine` apenas coordene:
   - recebe `TeacherContext`;
   - chama `decision_engine`;
   - seleciona strategy;
   - retorna `TeacherDecision`.
5. Marcar `teacher/decision.py` antigo como legado ou remover depois que nenhum import depender dele.

Checkpoint:

- `TeacherEngine` decide `correction` para erro real.
- `TeacherEngine` decide `conversation` para frase sem erro.
- Nenhum arquivo antigo importa `app.services.teacher.decision.TeacherDecision`.

## Fase 2: Decision Brain

Objetivo: fazer o `teacher/decision` virar o juiz principal.

Arquivos:

- `teacher/decision/engine.py`
- `teacher/decision/intent.py`
- `teacher/decision/priority.py`
- `teacher/decision/confidence.py`
- `teacher/decision/review.py`
- `teacher/decision/selector.py`

Passos:

1. `intent.py`: detectar intencao pedagogica:
   - `CORRECT`
   - `EXPLAIN`
   - `PRACTICE`
   - `REVIEW`
   - `CONVERSATION`
   - `IGNORE`
2. `priority.py`: aplicar prioridade:
   - erro gramatical real;
   - pedido direto do aluno;
   - revisao vencida;
   - pratica de skill fraca;
   - conversa natural.
3. `confidence.py`: calcular confianca usando:
   - `grammar.confidence`;
   - `grammar.has_errors`;
   - `pedagogical.has_any_real_error`;
   - historico da memoria.
4. `selector.py`: escolher `target_skill` sem brigar com erro atual.
   - Se `grammar.primary_error` existe, ele vence.
   - Se nao existe erro, pode usar memoria/skill fraca.
5. `review.py`: decidir quando revisar skill antiga.

Checkpoint:

- `I go to school yesterday` sempre escolhe `past_tense`, nunca `verb_usage`.
- Skill fraca so entra quando nao existe erro atual.
- Logs mostram a razao da decisao.

## Fase 3: Strategies

Objetivo: cada tipo de decisao tem uma strategy pequena e previsivel.

Arquivos:

- `teacher/strategies/base.py`
- `teacher/strategies/correction.py`
- `teacher/strategies/conversation.py`
- `teacher/strategies/explanation.py`
- `teacher/strategies/exercise.py`
- `teacher/strategies/review.py`
- `teacher/registry.py`

Passos:

1. Manter `CorrectionStrategy` para erros reais.
2. Manter `ConversationStrategy` para conversa natural.
3. Implementar `ExplanationStrategy` quando:
   - aluno erra a mesma skill repetidas vezes;
   - usuario pede explicacao;
   - erro tem conceito associado.
4. Implementar `ExerciseStrategy` quando:
   - houve ensino recente;
   - skill fraca precisa de pratica;
   - intervalo pedagogico permite intervencao.
5. Implementar `ReviewStrategy` quando:
   - skill antiga esta vencida;
   - memoria mostra queda de dominio.
6. Atualizar `registry.py` para selecionar por `TeacherIntent`.

Checkpoint:

- Uma strategy por intent principal.
- Nenhuma strategy chama LLM.
- Strategy retorna decisao, nao texto final longo.

## Fase 4: Teaching

Objetivo: gerar conteudo pedagogico controlado pelo backend.

Arquivos:

- `teacher/teaching/engine.py`
- `teacher/teaching/explanation.py`
- `teacher/teaching/examples.py`
- `teacher/teaching/templates.py`
- `teacher/teaching/formatter.py`

Passos:

1. `templates.py`: criar templates por skill e CEFR.
2. `examples.py`: gerar exemplos corretos/incorretos.
3. `explanation.py`: produzir explicacao curta em PT-BR com exemplo em ingles.
4. `formatter.py`: formatar conteudo para `PromptContext`.
5. `engine.py`: coordenar templates, exemplos e formato final.

Checkpoint:

- `past_tense` em A1/A2 gera explicacao curta.
- `third_person` gera exemplo com `he/she/it`.
- Conteudo de aula nao entra em `PedagogicalAnalysis`; entra em output/plan proprio.

## Fase 5: Exercise

Objetivo: migrar exercicios para `teacher/exercise`.

Arquivos:

- `teacher/exercise/engine.py`
- `teacher/exercise/fill_blank.py`
- `teacher/exercise/rewrite.py`
- `teacher/exercise/mini.py`
- `teacher/exercise/challenge.py`

Passos:

1. Criar interface comum para geradores de exercicio.
2. `fill_blank.py`: lacunas simples.
3. `rewrite.py`: reescrita guiada.
4. `mini.py`: pergunta curta de reforco.
5. `challenge.py`: desafio para skill dominada.
6. `engine.py`: escolher tipo usando skill, CEFR e memoria.
7. Rodar em paralelo com `skill_exercise_engine.py` antes de substituir.

Checkpoint:

- Exercicio gerado sempre tem `skill`, `type`, `prompt`, `answer`.
- Nao gerar exercicio quando `teacher_action=chat`.
- Nao treinar skill diferente do erro atual na mesma rodada.

## Fase 6: Curriculum

Objetivo: organizar progressao de aprendizagem.

Arquivos:

- `teacher/curriculum/roadmap.py`
- `teacher/curriculum/progression.py`
- `teacher/curriculum/selector.py`

Passos:

1. `roadmap.py`: mapear skills por CEFR.
2. `progression.py`: decidir avancar, manter ou revisar.
3. `selector.py`: escolher proxima skill quando nao ha erro atual.
4. Integrar com memoria, mastery e weak skills.

Checkpoint:

- Erro atual continua tendo prioridade sobre curriculo.
- Curriculo so escolhe nova skill em modo conversa/pratica.
- CEFR estimado nao rebaixa usuario por uma frase curta isolada.

## Fase 7: Teacher Memory

Objetivo: transformar memoria bruta em resumo pedagogico limpo.

Arquivos:

- `teacher/memory/engine.py`
- `teacher/memory/recall.py`
- `teacher/memory/preferences.py`
- `teacher/memory/evolution.py`

Passos:

1. `recall.py`: buscar skills fracas, ultima skill e erros comuns.
2. `preferences.py`: extrair tema favorito e estilo de conversa.
3. `evolution.py`: resumir progresso, quedas e dominio.
4. `engine.py`: entregar um objeto simples para `TeacherContext`.

Checkpoint:

- `TeacherContext` nao precisa conhecer o JSON bruto inteiro.
- Memoria nao incrementa skill errada quando o sanitizer bloqueia falso positivo.
- `last_target_skill` continua coerente.

## Fase 8: Personality

Objetivo: controlar tom sem interferir na decisao pedagogica.

Arquivos:

- `teacher/personality/engine.py`
- `teacher/personality/confidence.py`
- `teacher/personality/motivation.py`
- `teacher/personality/adaptive.py`

Passos:

1. `confidence.py`: ajustar tom conforme confianca/acerto.
2. `motivation.py`: incentivo curto e contextual.
3. `adaptive.py`: adaptar intensidade por nivel e historico.
4. `engine.py`: aplicar personalidade depois da decisao.

Checkpoint:

- Personality nunca troca `teacher_action`.
- Personality nao cria correcao nova.
- Tom muda, decisao nao.

## Fase 9: Prompt E LLM Executor

Objetivo: o LLM obedecer o Teacher, nao decidir por conta propria.

Arquivos:

- `prompt_builder/context.py`
- `prompt_builder/builder.py`
- `prompt_builder/composer.py`
- `chat_service.py`

Passos:

1. Expandir `PromptContext` com `TeacherDecision`.
2. Incluir no prompt:
   - action final;
   - target skill;
   - correction policy;
   - exercise policy;
   - teaching content quando existir.
3. Reduzir decisoes internas de `generate_response`.
4. Manter shadow log:
   - `TeacherDecision.teacher_action`
   - `generate_response.teacher_action`
   - `sanitized.teacher_action`
5. So remover logica antiga quando os tres baterem por varios casos.

Checkpoint:

- `generate_response` nao escolhe skill diferente do Teacher.
- `allowed_mode` nao contradiz `TeacherDecision`.
- LLM devolve JSON valido mesmo quando so deve conversar.

## Fase 10: Sanitizer E Guardrails

Objetivo: bloquear falso positivo sem apagar erro real.

Arquivos:

- `pedagogical/sanitizer.py`
- `correction_validator.py`
- `debug/sanitizer_logger.py`
- `debug/migration_error_logger.py`

Passos:

1. Preservar erro confirmado pelo Grammar.
2. Bloquear rewrite inventado do LLM.
3. Separar razoes:
   - `grammar_confirmed_error`
   - `invalid_rewrite`
   - `generic_praise`
   - `rephrase_equivalent`
   - `target_skill_marker_match`
4. Adicionar testes de contrato para sanitizer.
5. Garantir que memoria recebe `had_error` e `target_skill_error` corretos.

Checkpoint:

- `I go to school yesterday` nao vira `Correct!`.
- `I went yesterday` nao recebe correcao inventada.
- `She listen to music` continua third person.
- Frase correta nao incrementa weak skill.

## Fase 11: Testes De Regressao

Objetivo: criar uma suite pequena antes de mexer mais fundo.

Testes recomendados:

- `backend/tests/teacher/test_teacher_decision.py`
- `backend/tests/teacher/test_teacher_registry.py`
- `backend/tests/pedagogical/test_sanitizer_contract.py`
- `backend/tests/conversation/test_teacher_pipeline.py`

Casos minimos:

- `I go to school yesterday` -> correction, `past_tense`.
- `She listen to music` -> correction, `third_person`.
- `I went yesterday` -> chat ou praise, sem erro.
- `I went yesterday` + rewrite inventado -> sanitizer bloqueia.
- Skill fraca `verb_usage` nao vence erro atual `past_tense`.

Comandos:

```bash
python -m compileall backend/app
python -m pytest backend/tests -q
```

Observacao: se `pytest` nao estiver instalado no ambiente, instalar dependencias do
backend antes de considerar a fase concluida.

## Fase 12: Limpeza De Legado

Objetivo: remover duplicacao so depois de estabilizar.

Arquivos candidatos:

- `teacher/decision.py`
- `teacher/decision_engine.py`
- partes decisorias de `chat_service.py`
- engines antigas de exercicio, quando `teacher/exercise` cobrir os casos.

Passos:

1. Marcar legado nos comentarios.
2. Confirmar que nenhum import usa o arquivo.
3. Rodar testes.
4. Remover em PR pequeno.

Checkpoint:

- Menos de uma fonte decide `teacher_action`.
- Menos de uma fonte decide `target_skill`.
- Logs continuam explicando a decisao final.

## Ordem Recomendada De Implementacao

1. Finalizar testes do sanitizer e Teacher atual.
2. Completar `teacher/decision/*`.
3. Completar `teacher/strategies/*`.
4. Completar `teacher/teaching/*`.
5. Completar `teacher/exercise/*`.
6. Completar `teacher/curriculum/*`.
7. Completar `teacher/memory/*`.
8. Completar `teacher/personality/*`.
9. Migrar `generate_response` para executor.
10. Remover legado com testes passando.

## Visao Final

O projeto deve chegar a um tutor onde:

- Grammar Engine detecta fatos linguisticos.
- Pedagogical Analysis guarda estado pedagogico.
- Teacher Brain decide a acao correta.
- Teaching/Exercise geram conteudo controlado.
- Personality adapta o tom.
- LLM transforma decisao em resposta natural.
- Memory registra progresso sem contaminar skills.
- Frontend apresenta a experiencia com cards, voz, XP e gamificacao.
