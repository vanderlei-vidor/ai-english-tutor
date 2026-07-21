# 💡 Exemplos de Uso da Arquitetura Teacher

## 1️⃣ Fluxo Completo: Do Brain até o LLM

```python
from app.services.teacher.brain.engine import TeacherBrain
from app.services.teacher.pedagogy.engine import teaching_engine
from app.services.teacher.lesson.manager import lesson_manager
from app.services.teacher.prompt.builder import teacher_prompt_builder

# ══════════════════════════════════════════════════════════════
# PASSO 1: Teacher Brain - O que fazer?
# ══════════════════════════════════════════════════════════════

teacher_brain = TeacherBrain()

# Alimentar com estado do aluno e contexto
state = {
    "student_level": "intermediate",
    "last_mistake": "verb_conjugation",
    "engagement": 0.8,
    "session_time": 300,
}

# Brain percebe, reflete e planeja
teacher_brain.perception.observe(state)
teacher_brain.reflection.analyze(state)

# Brain retorna: O QUE fazer (TeacherActionPlan)
# Exemplo: "Ensinar verb conjugation para intermediate"


# ══════════════════════════════════════════════════════════════
# PASSO 2: Pedagogy Engine - Como ensinar?
# ══════════════════════════════════════════════════════════════

# Recebe o estado e constrói plano pedagógico
pedagogical_plan = teaching_engine.build(state)

# Internamente no engine:
# 1. Teaching Registry seleciona a melhor estratégia
#    → Retorna: GuidedDiscoveryStrategy (porque aluno está engajado e é novo)
#
# 2. Strategy define parâmetros
#    → use_examples = True
#    → scaffolding = "high"
#    → feedback_style = "encouraging"
#
# 3. Script Registry busca o template
#    → script_registry.get("guided_discovery")
#    → Retorna: GuidedDiscoveryScript com os passos
#
# 4. TeachingStrategyPlan retorna com tudo preenchido
#    → pedagogical_plan.strategy = "GuidedDiscoveryStrategy"
#    → pedagogical_plan.script = TeachingScript com 5 passos
#    → pedagogical_plan.scaffolding = "high"

print(f"Estratégia: {pedagogical_plan.strategy}")
print(f"Script: {pedagogical_plan.script.name}")
print(f"Passos: {len(pedagogical_plan.script.steps)}")
# Output:
# Estratégia: GuidedDiscoveryStrategy
# Script: guided_discovery_script
# Passos: 5


# ══════════════════════════════════════════════════════════════
# PASSO 3: Lesson Manager - Executar os passos
# ══════════════════════════════════════════════════════════════

lesson = lesson_manager.create(pedagogical_plan)

# Executar cada passo do script
for step in pedagogical_plan.script.steps:
    print(f"Executando: {step.action}")
    
    if step.ask_question:
        # Preparar pergunta
        pass
    
    if step.use_example:
        # Buscar/preparar exemplos
        pass
    
    if step.wait_student:
        # Esperar resposta do aluno
        pass
    
    if step.reveal_answer:
        # Revelar a resposta correta
        pass


# ══════════════════════════════════════════════════════════════
# PASSO 4: Prompt Builder - Construir prompt para LLM
# ══════════════════════════════════════════════════════════════

prompt_context = teacher_prompt_builder.build(
    pedagogical_plan=pedagogical_plan,
    student_state=state,
    current_step=pedagogical_plan.script.steps[0],  # activate_prior_knowledge
)

# Enviar para LLM
llm_response = llm.generate(prompt_context)

# LLM retorna com a resposta formatada
# Ex: "Great! What do you think happens with 'I go' in past tense?"
```

---

## 2️⃣ Acessando o Script Registry Diretamente

```python
from app.services.teacher.pedagogy.scripts import script_registry

# Obter um script específico
script = script_registry.get("socratic")
print(f"Script: {script.name}")
print(f"Tipo: {script.strategy_type}")
print(f"Steps:")
for i, step in enumerate(script.steps, 1):
    print(f"  {i}. {step.action}")

# Output:
# Script: socratic_script
# Tipo: socratic
# Steps:
#   1. initial_question
#   2. deepen_question
#   3. guide_contradiction
#   4. lead_to_conclusion
#   5. finish
```

---

## 3️⃣ Listar Todas as Estratégias Disponíveis

```python
from app.services.teacher.pedagogy.registry import teaching_registry
from app.services.teacher.pedagogy.scripts import script_registry

print("=== Estratégias Pedagógicas Disponíveis ===")
for strategy in teaching_registry._strategies:
    print(f"\n{strategy.__class__.__name__}:")
    print(f"  Descrição: {strategy.__doc__}")

print("\n=== Scripts Disponíveis ===")
for strategy_type in script_registry.list_available():
    print(f"  - {strategy_type}")

# Output:
# === Estratégias Pedagógicas Disponíveis ===
#
# GuidedDiscoveryStrategy:
#   Descrição: Estratégia de descoberta guiada...
#
# DirectInstructionStrategy:
#   Descrição: Estratégia de instrução direta...
#
# ... (outras estratégias)
#
# === Scripts Disponíveis ===
#   - direct_instruction
#   - guided_discovery
#   - communicative
#   - minimal_hint
#   - socratic
```

---

## 4️⃣ Exemplo: Seleção Automática de Estratégia

```python
from app.services.teacher.pedagogy.registry import teaching_registry

# Diferentes estados do aluno
states = [
    {
        "level": "beginner",
        "engagement": 0.3,
        "time_spent": 600,
        "mistakes": 5,
    },
    {
        "level": "intermediate",
        "engagement": 0.8,
        "time_spent": 300,
        "mistakes": 1,
    },
    {
        "level": "advanced",
        "engagement": 0.6,
        "time_spent": 200,
        "mistakes": 0,
    },
]

for state in states:
    strategy = teaching_registry.select(state)
    print(f"Estado: {state['level']} → Estratégia: {strategy.__class__.__name__}")

# Output:
# Estado: beginner → Estratégia: DirectInstructionStrategy
# Estado: intermediate → Estratégia: GuidedDiscoveryStrategy
# Estado: advanced → Estratégia: SocraticStrategy
```

---

## 5️⃣ Registrando um Novo Script

```python
from app.services.teacher.pedagogy.scripts import script_registry, TeachingScriptBase, TeachingScript, TeachingStep

# Criar um novo script customizado
class MyCustomScript(TeachingScriptBase):
    @property
    def strategy_type(self) -> str:
        return "my_custom_strategy"
    
    def build(self) -> TeachingScript:
        script = TeachingScript(
            name="my_custom_script",
            strategy_type=self.strategy_type,
            description="Meu script customizado",
        )
        
        script.steps = [
            TeachingStep(action="step_1", ask_question=True),
            TeachingStep(action="step_2", use_example=True),
            TeachingStep(action="step_3", finish=True),
        ]
        
        return script

# Registrar
custom_script = MyCustomScript()
script_registry.register("my_custom_strategy", custom_script)

# Usar
script = script_registry.get("my_custom_strategy")
print(f"Script: {script.name}")
print(f"Steps: {len(script.steps)}")
```

---

## 6️⃣ Estrutura do TeachingStrategyPlan (Retorno do Engine)

```python
from app.services.teacher.pedagogy.engine import teaching_engine
from app.services.teacher.pedagogy.models import TeachingStrategyPlan

plan = teaching_engine.build(state)

# plan é um TeachingStrategyPlan com:
plan.strategy              # Ex: "GuidedDiscoveryStrategy"
plan.explanation_style     # Ex: "interactive"
plan.reveal_answer         # True/False
plan.use_example          # True/False
plan.use_analogy          # True/False
plan.ask_question         # True/False
plan.scaffolding          # Ex: "high", "medium", "low"
plan.difficulty           # Ex: "intermediate"
plan.feedback_style       # Ex: "encouraging"
plan.conversation_style   # Ex: "dialogue"
plan.exercise_style       # Ex: "guided_practice"
plan.wait_student         # True/False
plan.teacher_reason       # Explicação da decisão
plan.script               # TeachingScript com os passos!

# O script é o template que será executado
for step in plan.script.steps:
    print(f"- {step.action}")
```

---

## 🎯 Princípios Importantes

### ✅ CORRETO:

```python
# Brain decide o QUE
# Engine decide o COMO
plan = teaching_engine.build(state)

# Plan tem tudo que precisa para executar
lesson = lesson_manager.create(plan)
```

### ❌ ERRADO:

```python
# Brain acessando script direto (ACOPLAMENTO!)
from app.services.teacher.pedagogy.scripts import script_registry
script = script_registry.get("socratic")  # ❌ Brain não deve fazer isso

# Brain deveria ir através do Engine
plan = teaching_engine.build(state)
script = plan.script  # ✅ Script vem dentro do plan
```

---

## 📊 Fluxo de Dados

```
┌──────────────────────────────────────────────────────┐
│  Teacher State (aluno, contexto, etc)                │
└────────────────┬─────────────────────────────────────┘
                 │
                 ▼
    ┌───────────────────────────┐
    │  Teaching Registry        │
    │  (seleciona estratégia)   │
    └────────────┬──────────────┘
                 │
                 ▼
    ┌───────────────────────────────────┐
    │  Teaching Strategy                │
    │  (define parâmetros pedagógicos)  │
    │  - scaffolding = "high"           │
    │  - use_examples = True            │
    └────────────┬──────────────────────┘
                 │
                 ▼
    ┌───────────────────────────────────┐
    │  Script Registry                  │
    │  (busca template de steps)        │
    └────────────┬──────────────────────┘
                 │
                 ▼
    ┌───────────────────────────────────┐
    │  Teaching Script                  │
    │  (passos específicos)             │
    │  - activate_prior_knowledge       │
    │  - guide_thinking                 │
    │  - encourage_discovery            │
    └────────────┬──────────────────────┘
                 │
                 ▼
    ┌───────────────────────────────────┐
    │  TeachingStrategyPlan             │
    │  (tudo junto para executar)       │
    └─────────────────────────────────┘
```

---

Essa arquitetura garante que tudo é **claro**, **desacoplado** e **fácil de manter**! ❤️
