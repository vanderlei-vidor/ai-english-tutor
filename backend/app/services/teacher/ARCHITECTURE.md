# 🏗️ Arquitetura Final do Teacher

Essa é a arquitetura definitiva do Teacher Engine. Praticamente não muda mais.

## 🎯 Princípios Fundamentais

1. **Separação de Responsabilidades**: Brain decide O QUE fazer, Pedagogy Engine decide COMO ensinar
2. **Desacoplamento Total**: Brain nunca fala direto com Scripts
3. **Fluxo Claro**: Perception → Reflection → Planning → TeacherActionPlan → PedagogicalPlan
4. **Escalabilidade**: Novos scripts e estratégias podem ser adicionados sem quebrar nada

## 📊 Diagrama de Arquitetura

```
                        Teacher Engine
                               │
                               ▼
                        Teacher Brain
                               │
              ┌────────────┬──────────────┬──────────────┐
              ▼            ▼              ▼              ▼
         Perception    Reflection     Planning      State Sync
              │            │              │
              └────────────┴──────────────┘
                           │
                           ▼
                    TeacherActionPlan
                       (O QUE fazer?)
                           │
                           ▼
                     Pedagogy Engine
                           │
                ┌───────────┴───────────┐
                ▼                       ▼
        Teaching Registry        Script Registry
                │                       │
                ▼                       ▼
        Teaching Strategy        Teaching Script
                │                       │
                └───────────┬───────────┘
                            ▼
                    PedagogicalPlan
                      (COMO ensinar?)
                            │
                            ▼
                    Lesson Manager
                            │
                            ▼
                    Current Lesson
                            │
                            ▼
                    Prompt Builder
                            │
                            ▼
                  PromptContext
                            │
                            ▼
                          LLM
                            │
                            ▼
                    Response Executor
```

## 📁 Estrutura de Diretórios

```
teacher/
│
├── brain/                      # 🧠 Cérebro do Professor
│   ├── engine.py              # Orquestrador principal
│   ├── perception.py          # Observa o estado do aluno
│   ├── reflection.py          # Reflete sobre o aprendizado
│   ├── planning.py            # Planeja próximos passos
│   ├── state.py              # Estado interno do Brain
│   └── models.py             # Modelos de dados
│
├── pedagogy/                   # 🎓 Engine Pedagógico
│   ├── engine.py             # Orquestrador (O QUE → COMO)
│   ├── registry.py           # Teaching Strategy Registry
│   ├── base.py               # Base classes
│   ├── models.py             # TeachingStrategyPlan
│   │
│   ├── strategies/           # 📚 Estratégias Pedagógicas
│   │   ├── base.py           # TeachingStrategyBase
│   │   ├── models.py         # Modelos das estratégias
│   │   ├── registry.py       # Strategy Registry
│   │   ├── direct_instruction.py      # Instrução direta
│   │   ├── guided_discovery.py        # Descoberta guiada
│   │   ├── communicative.py           # Abordagem comunicativa
│   │   ├── minimal_hint.py            # Dica mínima
│   │   └── socratic.py               # Método socrático
│   │
│   └── scripts/              # 📝 Scripts Pedagógicos
│       ├── base.py           # TeachingScriptBase
│       ├── models.py         # TeachingScript, TeachingStep
│       ├── registry.py       # Script Registry (O coração!)
│       ├── direct_instruction.py      # Script: instrução direta
│       ├── guided_discovery.py        # Script: descoberta guiada
│       ├── communicative.py           # Script: comunicativo
│       ├── minimal_hint.py            # Script: dica mínima
│       └── socratic.py               # Script: socrático
│
├── lesson/                     # 📖 Gerenciador de Lições
│   ├── manager.py            # Executa os scripts
│   ├── models.py             # Modelos de lição
│   └── phases.py             # Fases da lição
│
├── prompt/                     # 💬 Construtor de Prompts
│   ├── builder.py            # Constrói prompts LLM
│   └── models.py             # PromptContext
│
└── [outros módulos...]
```

## 🔄 Flow de Execução

### 1️⃣ Teacher Brain (Decision Making)

```python
brain = TeacherBrain()

# Perception: Observa o estado do aluno
brain.perception.observe(student_state)

# Reflection: Reflete sobre o aprendizado
brain.reflection.analyze(student_progress)

# Planning: Planeja próximos passos
teacher_action_plan = brain.planning.decide(state)
```

### 2️⃣ Pedagogy Engine (How to Teach)

```python
from app.services.teacher.pedagogy.engine import teaching_engine

# Recebe o plano do Brain (O QUE fazer)
action_plan = brain.planning.decide(state)

# Constrói o plano pedagógico (COMO ensinar)
pedagogical_plan = teaching_engine.build(state)

# Inside teaching_engine.build():
# 1. Teaching Registry seleciona a estratégia ideal
# 2. Strategy define os parâmetros pedagógicos
# 3. Script Registry busca o template de steps
# 4. TeachingStrategyPlan retorna com Script incluído
```

### 3️⃣ Lesson Manager (Execution)

```python
from app.services.teacher.lesson.manager import lesson_manager

# Executa os passos do Teaching Script
lesson = lesson_manager.create(pedagogical_plan)

for step in pedagogical_plan.script.steps:
    lesson.execute_step(step)
```

### 4️⃣ Prompt Builder (LLM Communication)

```python
from app.services.teacher.prompt.builder import teacher_prompt_builder

# Constrói o prompt para o LLM
context = teacher_prompt_builder.build(
    pedagogical_plan,
    student_state,
    current_lesson
)

response = llm.generate(context)
```

## 🎯 Características Principais

### ✨ **Desacoplamento Total**

O Brain NUNCA conversa direto com Scripts:

```
❌ ERRADO:
Brain → Script (Direct)

✅ CORRETO:
Brain → Pedagogy Engine → Teaching Registry → Strategy
                             ↓
                        Script Registry → Script
```

### 📊 **Seleção de Estratégia**

```python
# Teaching Registry seleciona a melhor estratégia
teaching_registry = TeachingRegistry()
strategy = teaching_registry.select(state)  # ← Inteligência aqui!

# Cada estratégia tem critérios de seleção
- GuidedDiscovery: Para aprendizado novo e aluno engajado
- DirectInstruction: Para conceitos complexos
- Socratic: Para consolidação e pensamento crítico
- MinimalHint: Para alunos autônomos
- Communicative: Para prática de fala e interação
```

### 📝 **Teaching Scripts**

Cada estratégia tem um script correspondente:

```python
# DirectInstructionStrategy → direct_instruction_script
script = script_registry.get("direct_instruction")
# Retorna TeachingScript com passos:
# 1. present_concept
# 2. show_examples
# 3. practice_exercise
# 4. provide_feedback
# 5. finish
```

## 🔧 Estendendo a Arquitetura

### Adicionando uma Nova Estratégia

1. Criar arquivo em `strategies/` (ex: `strategies/flipped_classroom.py`)
2. Implementar classe que herda de `TeachingStrategyBase`
3. Implementar método `matches()` com critérios de seleção
4. Adicionar à `TeachingRegistry`

### Adicionando um Novo Script

1. Criar arquivo em `scripts/` (ex: `scripts/flipped_classroom.py`)
2. Implementar classe que herda de `TeachingScriptBase`
3. Definir os `TeachingStep`s no método `build()`
4. Registrar em `ScriptRegistry`

## 🚀 Importantes

- **Brain Decision**: O Brain nunca sabe detalhes pedagógicos
- **Engine Orchestration**: O Engine orquestra tudo
- **Registry Pattern**: Fácil adicionar novos strategies/scripts
- **TeachingScript**: Templates reutilizáveis de execução

## ✅ Checklist da Arquitetura

- [x] Brain isolado de Scripts
- [x] Teaching Registry para seleção de estratégia
- [x] Script Registry centralizado
- [x] Separação clara: O QUE vs COMO
- [x] TeachingStrategyPlan com script incluído
- [x] Lesson Manager executa scripts
- [x] Desacoplamento total
- [x] Escalabilidade para novos strategies/scripts

---

**Essa arquitetura é estável. As principais mudanças futuras serão:**
1. Adicionar mais strategies
2. Adicionar mais scripts por estratégia
3. Melhorar critérios de seleção no registry
4. Refinar os steps do scripts

**Não mexer em:**
1. A estrutura de diretórios principal
2. O flow Brain → Engine → Lesson Manager
3. A separação Teaching Strategy vs Teaching Script
