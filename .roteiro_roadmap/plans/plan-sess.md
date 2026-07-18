# 🚀 Plano de Migração — Eliminação da Arquitetura Antiga e Dual Brain

## 🎯 Escopo Confirmado
**Limpeza + Eliminar Dual Brain** (sem unificação de dataclasses ainda), com **absorção do `choose_teaching_skill` no Brain** e execução em **fases incrementais com commits**.

## 📊 Princípios Orientadores
1. **O Teacher Brain é a ÚNICA fonte de decisão pedagógica** — nenhum `_prepare_pedagogical_context` paralelo
2. **Cada fase produz um commit verde** (sintaxe valida + imports resolvem) antes da próxima
3. **Sem alteração de contratos JSON** externos (`teacher_action`, etc. permanecem os mesmos)
4. **Zero quebra de testes** (já verificado: nenhum teste depende do que está sendo removido)

---

## 🗂️ FASE 1 — Remover Código Morto (zero risco)
**Objetivo:** Deletar arquivos sem nenhuma referência externa.

**Deletar:**
- `backend/app/services/conversation/` (diretório inteiro — 0 imports)
- `backend/app/services/teacher/state/student_sync.py` (0 imports)
- `backend/app/services/teacher/pedagogy/memory_provider.py` (0 imports externos)
- `backend/app/services/teacher/pedagogy/memory_snapshot.py` (0 imports externos)
- `backend/app/services/teacher/decision.py` (raiz, duplicado, 0 imports)
- `backend/app/services/teacher/decision/confidence.py`, `intent.py`, `priority.py`, `review.py`, `selector.py` (5 arquivos vazios, 0 bytes cada)

**Commit:** `refactor: remove dead code with no external references`

---

## 🗂️ FASE 2 — Eliminar Subsistema `teacher/strategies/` (camada de strategies antiga)
**Objetivo:** Remover a hierarquia `TeacherStrategy` (no-op) e o `TeacherDecision`/`TeacherIntent` antigos.

### Passo 2a — Refatorar `teacher/engine.py`:
O `TeacherEngine.decide()` atualmente chama `teacher_execution_engine.decide()` + `teacher_registry.select()` + `strategy.build()` (que são todos no-ops). Simplificar para:
```python
def decide(self, context: TeacherContext) -> TeacherResult:
    brain_state = teacher_brain.think(context)
    teacher_logger.brain(brain_state)
    lesson_manager.set_last_action(brain_state.planning.action)
    lesson_manager.advance()
    return TeacherResult(brain=brain_state)
```
Remove imports de: `teacher_execution_engine`, `teacher_registry`, `TeacherDecision`, `TeacherIntent`.

### Passo 2b — Deletar:
- `backend/app/services/teacher/strategies/` (diretório inteiro — base, conversation, correction + 3 vazios)
- `backend/app/services/teacher/registry.py`
- `backend/app/services/teacher/decision/teacher_execution_engine.py`
- `backend/app/services/teacher/models.py` (TeacherDecision + TeacherIntent)
- `backend/app/services/teacher/decision/` (diretório, após mover o `teacher_execution_engine.py` deletado)

### Passo 2c — Bugfix: Remover campos duplicados em `state/models.py`:
`TeachingState` declara `has_error`, `detected_skill`, `target_skill` **duas vezes**. Deletar o bloco duplicado (linhas 28-33).

**Commit:** `refactor: remove legacy TeacherStrategy hierarchy and TeacherDecision`

---

## 🗂️ FASE 3 — Eliminar `TeacherResponsePlanner`/`TeacherResponsePlan` (camada temporária)
**Objetivo:** Remover a camada de compatibilidade que apenas copia campos do `TeacherActionPlan`.

### Passo 3a — Atualizar `brain/state.py`:
Remover import de `TeacherResponsePlan` e o campo `response: TeacherResponsePlan` do `TeacherBrainState`.

### Passo 3b — Atualizar `brain/engine.py`:
Remover import de `teacher_response_planner`, remover a chamada `response = teacher_response_planner.create_response_plan(plan)` e o kwarg `response=response` no `TeacherBrainState(...)`.

### Passo 3c — Deletar:
- `backend/app/services/teacher/response/models.py`
- `backend/app/services/teacher/response/planner.py`
- Manter `backend/app/services/teacher/response/executor.py` (lê `brain.planning.action`, é usado por `chat_service.py`)

**Commit:** `refactor: remove temporary TeacherResponsePlan compatibility layer`

---

## 🗂️ FASE 4 — Eliminar Subsistema `teacher/pedagogy/` (TeachingStrategyPlan morto)
**Objetivo:** Remover o `TeachingStrategyPlan` e toda sua machinery (registry, strategies, teaching_engine) — nenhuma pipeline lê esses campos, só o logger.

### Passo 4a — Atualizar `brain/state.py`:
Remover import de `TeachingStrategyPlan` e o campo `teaching: TeachingStrategyPlan` do `TeacherBrainState`.

### Passo 4b — Atualizar `brain/engine.py`:
Remover import de `teaching_engine`, remover a chamada `teaching_plan = teaching_engine.build(state)` e o kwarg `teaching=teaching_plan`. Ajustar assinatura do `teacher_prompt_builder.build(plan, teaching_plan)` → `teacher_prompt_builder.build(plan)`.

### Passo 4c — Atualizar `teacher/prompt/builder.py`:
Remover parâmetro `teaching_plan` (não é mais usado — verificar uso real antes).

### Passo 4d — Atualizar `teacher/logger.py`:
Remover método `_teaching()` (linhas 115-128) e as referências em `brain()` (linhas 149, 170-171).

### Passo 4e — Deletar:
- `backend/app/services/teacher/pedagogy/teaching_engine.py`
- `backend/app/services/teacher/pedagogy/teaching_models.py`
- `backend/app/services/teacher/pedagogy/registry.py`
- `backend/app/services/teacher/pedagogy/strategies/` (diretório inteiro: communicative, direct_instruction, guided_discovery, minimal_hint, socratic)
- `backend/app/services/teacher/pedagogy/__init__.py`

**Commit:** `refactor: remove dead TeachingStrategyPlan subsystem`

---

## 🗂️ FASE 5 — Absorver `choose_teaching_skill` no Teacher Brain
**Objetivo:** Migrar o algoritmo de seleção de skill (mastery 70% + weak_skills 30%) para dentro do Brain, eliminando a dependência do `chat_service` no `weighted_teaching_engine`.

### Passo 5a — Criar `teacher/student/skill_selector.py`:
Mover a lógica de `weighted_teaching_engine.choose_teaching_skill()` + `skill_score_service.calculate_skill_scores()` para um módulo interno do Brain:
```python
class StudentSkillSelector:
    def select(self, student: StudentState, memory_data: dict) -> str | None:
        # Algoritmo: combina mastery (70%) + weak_skills (30%)
        # Retorna a skill prioritária ou None
```
Singleton `student_skill_selector`.

### Passo 5b — Integrar no `memory_sync.py`:
Na fase de sincronização de memória (após carregar `weak_skills` e antes da reflection), se NÃO houver erro gramatical detectado, usar o `student_skill_selector` para definir `state.target_skill` e `state.skill_focus.teaching`.

### Passo 5c — Atualizar `student_manager.py` / `profile_builder.py`:
Corrigir o bug dos loaders executando **2x** (remover a chamada duplicada em `_run_loaders` OU inline).

### Passo 5d — Mover `get_top_topics` para dentro do carregamento de memória (será usado na Fase 6).

**Commit:** `refactor: absorb weighted skill selection into Teacher Brain`

---

## 🗂️ FASE 6 — Eliminar Dual Brain no `chat_service.py`
**Objetivo:** Remover `_prepare_pedagogical_context()` e fazer do Teacher Brain a ÚNICA decisão pedagógica.

### Passo 6a — Adicionar `exercise_type` ao `TeacherActionPlan`:
Novo campo `exercise_type: str | None = None`. Populado no `planning.py` pela chamada ao utilitário `choose_exercise_type` (movido de `exercise_engine.py` para `teacher/` ou mantido como utilitário importado).

### Passo 6b — Atualizar `teacher_response_executor.execute()`:
Atualizar para também popular `target_skill` e `exercise_type` no `response_json`, lendo de `brain.planning`.

### Passo 6c — Refatorar `chat_service.py`:
- **Deletar** `_prepare_pedagogical_context()` inteiro (~80 linhas)
- **Deletar** `_build_memory_context()` (a "DYNAMIC USER CONTEXT" era baseada em decisões do Legacy Brain)
- **Refatorar** `generate_response()` para ler tudo de `teacher_result.brain.planning`:
  - `target_skill` ← `brain.planning.target_skill`
  - `exercise_type` ← `brain.planning.exercise_type`
  - `theme` ← (do user_memory direto)
  - `english_level` ← `brain.student.estimated_level`
- **Refatorar** `_generate_exercise()` para usar `brain.planning.target_skill` ao invés do `exercise_focus` do Legacy
- **Remover** imports: `get_weakest_skill` (já morto), `should_generate_exercise` (Brain já decidiu via `generate_exercise`), `get_top_errors`/`get_top_topics` (mover lógica necessária)
- **Construir** `memory_context` novo baseado em `brain_state`, não em `_prepare_pedagogical_context`

### Passo 6d — Deletar (após confirmar 0 referências):
- `backend/app/services/weighted_teaching_engine.py` (absorvido na Fase 5)
- `backend/app/services/personalized_learning_engine.py` (import morto + bug: `max()` encontra mais alto, não mais fraco)
- `backend/app/services/exercise_engine.py` (absorvido: `should_generate_exercise` removido, `choose_exercise_type` movido)
- `backend/tests/test_chat_service_pedagogical_context.py` (testa função removida)

### Passo 6e — Limpar `chat.py`:
Remover linhas comentadas (`# conversation_analysis`, `# conversation_logger`) e o import inline de `pedagogical_analysis_engine` (mover para o topo).

**Commit:** `refactor: eliminate dual-brain — Teacher Brain is sole pedagogical authority`

---

## ✅ FASE 7 — Validação Final
- Rodar todos os testes: `cd backend && python -m pytest -v`
- Smoke test manual: enviar mensagem de chat e verificar resposta
- Verificar imports órfãos: `grep -rn "from app.services" backend/app --include="*.py" | python -c "import sys; ..."`
- Validar que `chat.py` não tem mais imports inline
- Confirmar redução: ~25 arquivos deletados, ~200 linhas de sync removidas

**Commit:** `test: validate post-migration integrity`

---

## 📦 Resumo do Impacto Esperado

| Métrica | Antes | Depois | Redução |
|---------|-------|--------|---------|
| Arquivos no módulo teacher | 105 | ~80 | -25% |
| Dataclasses com campos sobrepostos | 7+ | Mantidos (Fase de unificação fica para depois) | — |
| Fontes de decisão pedagógica | 2 (Brain + chat_service) | **1 (Brain)** | -50% |
| Funções de sync manual | 5 | 4 (removido ResponsePlanner) | -20% |
| Código morto (arquivos) | ~25 | 0 | -100% |
| Testes quebrados | 0 | 0 | — |

## ⚠️ Riscos e Mitigações

1. **Comportamento pedagógico pode mudar** — Antes o Legacy podia forçar exercícios que o Brain não queria. Pós-migração, o Brain é autoridade. **Mitigação:** smoke test manual após Fase 6.

2. **Absorção do `choose_teaching_skill`** — O Brain vai começar a decidir `target_skill` sozinho quando não há erro gramatical. Antes isso era decidido só pelo Legacy. **Mitigação:** algoritmo idêntico (mesmos pesos 70/30), apenas mudou o caller.

3. **Contrato JSON com LLM** — Não muda. `teacher_action`, `correction`, `exercise` continuam os mesmos keys.

## 📋 Ordem de Execução
Fases 1 → 2 → 3 → 4 → 5 → 6 → 7, **uma fase por commit**. Posso parar após qualquer fase para validação.

---

**Pronto para começar pela Fase 1?**