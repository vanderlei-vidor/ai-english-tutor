# Grammar Engine Architecture

> AI English Tutor
>
> Grammar Engine v2
>
> Architecture Documentation


---

# Philosophy

The Grammar Engine is **not** a grammar checker.

It is a complete language analysis pipeline.

Its responsibility is to transform a student's sentence into structured linguistic knowledge that can later be used by the teaching system.

Every layer has **one single responsibility**.

The Grammar Engine never teaches.

The Pedagogical Engine never parses.

The Memory Engine never analyzes grammar.

This separation keeps the system simple, scalable and easy to maintain.

---

# High Level Pipeline

```text
Student Sentence
        │
        ▼
Tokenizer
        │
        ▼
Lexical Layer
        │
        ▼
Structural Layer
        │
        ▼
Grammar Rules
        │
        ▼
Semantic Engine
        │
        ▼
Concept Engine
        │
        ▼
Pedagogical Engine
        │
        ▼
Memory Engine
        │
        ▼
LLM
        │
        ▼
Final Response
```

---

# Layer Responsibilities

## 1. Tokenizer

Responsible for splitting the sentence into individual tokens.

Input:

```
I went yesterday.
```

Output:

```
I
went
yesterday
```

The tokenizer performs no grammatical analysis.

---

## 2. Lexical Layer

Responsible for classifying each token.

Examples:

- Verb
- Auxiliary
- Article
- Adverb
- Preposition
- Pronoun
- Modal

This layer answers:

> "What kind of word is this?"

It does **not** determine sentence structure.

---

## 3. Structural Layer

Responsible for locating grammatical elements.

Examples:

- Subject
- Verb
- Auxiliary
- Object
- Article
- Adverb
- Preposition
- Markers

This layer answers:

> "What role does each word play in the sentence?"

---

## 4. Grammar Rule Layer

Responsible for validating grammatical correctness.

Examples:

- Third Person Rule
- Past Tense Rule
- Future Rules...

Output:

GrammarError objects.

No pedagogical decision is made here.

---

## 5. Semantic Engine

Responsible for identifying linguistic relationships.

Examples:

- interested + in

- depend + on

- good + at

- listen + to

Output:

SemanticRelation objects.

---

## 6. Concept Engine

Transforms grammar errors and semantic information into grammar concepts.

Examples:

GrammarError

↓

Simple Past

↓

Present Perfect

↓

Articles

↓

Prepositions

Output:

GrammarConcept objects.

The Concept Engine understands **what concept is involved**.

---

## 7. Pedagogical Engine

Responsible for deciding how to teach.

Examples:

- Explanation

- Examples

- Exercises

- Review strategy

Output:

TeachingPlan objects.

No grammar parsing occurs here.

---

## 8. Memory Engine

Responsible for tracking student learning.

Examples:

- Mastery

- Weak skills

- Review schedule

- Learning history

The Memory Engine never analyzes grammar.

It only stores learning progress.

---

## 9. LLM

The language model is the final layer.

Its responsibility is to:

- explain

- motivate

- converse naturally

- adapt language to the student

The LLM never decides grammar rules.

The system already provides structured knowledge.

---

# GrammarAnalysis

The GrammarAnalysis object is the central object of the entire architecture.

Every layer enriches the same object.

```
GrammarAnalysis

├── Context

├── Errors

├── Semantic Relations

├── Grammar Concepts

├── Teaching Plans

├── Compatibility Layer

└── Metadata
```

No layer replaces another.

Each layer only adds information.

---

# Core Design Principles

## Single Responsibility

Every engine has one responsibility.

---

## Open for Extension

New grammar rules should be added without modifying existing ones.

---

## Modular Architecture

Each component can evolve independently.

---

## Pedagogy First

Grammar analysis exists to support teaching.

Not the opposite.

---

## Deterministic Grammar

Grammar decisions should come from the engine whenever possible.

The LLM is responsible for communication, not validation.

---

# Long-Term Vision

The final system should behave like a private English teacher.

Instead of simply correcting mistakes, it should:

- understand the sentence

- identify concepts

- build a teaching strategy

- generate exercises

- remember student progress

- adapt future lessons

Every module contributes to this goal.

---

# Architecture Status

Current Stage:

✅ Tokenizer

✅ Lexical Layer

✅ Structural Layer

✅ Grammar Rules

✅ Semantic Engine

✅ Concept Engine

🚧 Pedagogical Engine

🚧 Memory Integration

🚧 Adaptive Lesson Planning

🚧 Intelligent Exercise Generator

🚧 Full CEFR Curriculum


# Architecture Evolution

## Phase 12

Correction Routing

## Phase 13

Routing Sanitizer

## Phase 14

Grammar Engine

## Phase 15

Parser Architecture

## Phase 16

Semantic Layer

Concept Engine

## Phase 17

Pedagogical Engine