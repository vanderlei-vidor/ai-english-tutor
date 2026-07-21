# ⚡ Quick Reference - Teacher Architecture

## 🎯 The Golden Rule

```
Brain says: "O QUE fazer?"
Pedagogy Engine says: "COMO ensinar?"
Brain NEVER accesses Scripts directly
```

## 📊 One-Liner Architecture

```
TeacherBrain → TeachingEngine → TeachingRegistry → Strategy
                                    ↓
                            ScriptRegistry → Script
                                    ↓
                            TeachingStrategyPlan
```

## 📁 Where Things Live

| Component | File | Purpose |
|-----------|------|---------|
| **Brain** | `brain/engine.py` | Decision maker |
| **Engine** | `pedagogy/engine.py` | Orchestrator (WHAT → HOW) |
| **Teaching Registry** | `pedagogy/registry.py` | Selects strategy |
| **Scripts Registry** | `pedagogy/scripts/registry.py` | Provides templates |
| **Strategies** | `pedagogy/strategies/` | Define teaching parameters |
| **Scripts** | `pedagogy/scripts/` | Define execution steps |
| **Lesson Manager** | `lesson/manager.py` | Executes scripts |

## 🔄 Step-by-Step Usage

```python
# 1. Brain decides WHAT
state = {...}  # student context
teacher_brain.perception.observe(state)
teacher_brain.reflection.analyze(state)
# Brain has TeacherActionPlan

# 2. Engine decides HOW
plan = teaching_engine.build(state)
# Engine returns: TeachingStrategyPlan with script included

# 3. Execute
lesson_manager.create(plan)
for step in plan.script.steps:
    execute(step)

# 4. Build prompt for LLM
context = teacher_prompt_builder.build(plan, state, step)
```

## 📜 Available Scripts (Teaching Templates)

| Script | What It Does | Best For |
|--------|-------------|----------|
| **direct_instruction** | Present → Examples → Practice → Feedback | Complex concepts |
| **guided_discovery** | Question → Guide → Discover → Validate | New learning, engaged students |
| **communicative** | Context → Practice → Feedback → Continue | Speaking/communication |
| **minimal_hint** | Question → Hint → Solve → Praise | Autonomous learners |
| **socratic** | Question deeply → Guide contradiction → Lead to conclusion | Critical thinking |

## 🎯 How Strategy Selection Works

```python
# Teaching Registry matches strategies based on state
if student.is_new_concept and student.is_engaged:
    return GuidedDiscoveryStrategy()
    
if student.concept_is_complex:
    return DirectInstructionStrategy()
    
if student.is_autonomous:
    return MinimalHintStrategy()
    
if student.needs_communication:
    return CommunicativeStrategy()
    
if student.is_consolidating:
    return SocraticStrategy()
```

## 🔧 Adding a New Script

```python
# 1. Create scripts/my_strategy.py
class MyStrategyScript(TeachingScriptBase):
    @property
    def strategy_type(self) -> str:
        return "my_strategy"
    
    def build(self) -> TeachingScript:
        script = TeachingScript(name="my_script", strategy_type=self.strategy_type)
        script.steps = [
            TeachingStep(action="step1", ...),
            TeachingStep(action="step2", ...),
        ]
        return script

# 2. Register in scripts/__init__.py
from .my_strategy import MyStrategyScript

# 3. Add to scripts/registry.py
self._scripts["my_strategy"] = MyStrategyScript()
```

## ✅ Architecture Checklist

- [x] Brain isolated from scripts
- [x] Teaching Registry for strategy selection
- [x] Script Registry as central hub
- [x] Clear separation: WHAT vs HOW
- [x] TeachingStrategyPlan carries everything needed
- [x] Easy to add new strategies/scripts
- [x] Fully decoupled

## ⚠️ Common Mistakes

```python
# ❌ WRONG
script = script_registry.get("socratic")  # Brain accessing scripts!

# ✅ RIGHT
plan = teaching_engine.build(state)
script = plan.script  # Script comes within plan
```

```python
# ❌ WRONG
strategy = teaching_registry.select(state)
strategy.do_something_random()  # Strategy should only be used by Engine

# ✅ RIGHT
plan = teaching_engine.build(state)  # Let Engine handle it
```

## 📚 Documentation Files

- `ARCHITECTURE.md` - Full architecture explanation with diagrams
- `USAGE_EXAMPLE.md` - Detailed usage examples and flows
- `QUICK_REFERENCE.md` - This file! Quick lookup

## 🚀 Next Steps

1. **Integrate with Brain** - Ensure Brain calls `teaching_engine.build()`
2. **Enhance Strategies** - Improve matching logic in `teaching_registry.select()`
3. **Expand Scripts** - Add more TeachingScript variations
4. **Connect Lesson Manager** - Ensure it executes scripts correctly

---

**Remember**: This architecture won't change much. Future work is:
- Adding more strategies
- Adding more scripts per strategy
- Refining selection criteria
- Improving step executions

**Not**: Changing the fundamental structure or adding direct Brain↔Script communication
