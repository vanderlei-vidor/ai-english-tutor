# AI English Tutor

<p align="center">

# 🧠 Your Personal AI English Teacher

### Learn English through natural conversations, adaptive exercises, voice interaction, and intelligent corrections powered by local AI.

</p>

<p align="center">
  <img src="https://img.shields.io/badge/Flutter-02569B?style=for-the-badge&logo=flutter&logoColor=white" />
  <img src="https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white" />
  <img src="https://img.shields.io/badge/PostgreSQL-336791?style=for-the-badge&logo=postgresql&logoColor=white" />
  <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white" />
  <img src="https://img.shields.io/badge/LM_Studio-Local_LLM-purple?style=for-the-badge" />
</p>

---

## 🚀 Overview

AI English Tutor is an adaptive language learning platform designed to act as a real personal English teacher rather than a generic chatbot.

Instead of simply generating answers, the platform continuously evaluates the student's weaknesses, identifies recurring grammar mistakes, tracks learning behavior, and dynamically decides what pedagogical action should happen next.

The result is a personalized learning experience powered by local artificial intelligence, persistent memory, voice interaction, adaptive exercises, and intelligent correction systems.

---

## ✨ Key Highlights

✔ Adaptive AI Teacher

✔ Personalized Learning Paths

✔ Real-Time Grammar Coaching

✔ Voice Conversations

✔ Intelligent Error Detection

✔ Adaptive Exercise Generation

✔ Gamification System

✔ XP & Level Progression

✔ Achievement Badges

✔ Learning Memory Engine

✔ PostgreSQL Persistence

✔ 100% Local AI Processing

---

## 🎯 The Problem

Most AI language tutors work as simple chat interfaces.

They answer questions.

They explain grammar.

They continue conversations.

But they rarely understand:

* What the student struggles with
* Which mistakes are recurring
* When intervention is needed
* How learning should progress

As a result, students often have engaging conversations without actually improving their English skills.

---

## 💡 Our Solution

AI English Tutor introduces a dedicated pedagogical intelligence layer between the user and the language model.

Instead of asking:

> "What should the AI answer?"

The system asks:

> "What should the student learn next?"

The platform continuously analyzes conversations, updates skill metrics, detects weaknesses, and dynamically chooses the most effective teaching strategy.

---

## 🏗 System Architecture

```text
Student
   │
   ▼
Flutter Application
   │
   ▼
FastAPI Backend
   │
   ├── Memory Engine
   ├── Error Pattern Engine
   ├── Exercise Engine
   ├── XP & Progress Engine
   ├── Pedagogical Resolver
   └── Analytics Layer
   │
   ▼
Qwen 2.5 (LM Studio)
   │
   ▼
Structured JSON Response
```

The backend acts as a deterministic educational orchestrator, ensuring pedagogical consistency regardless of model variability.

---

## 🧠 Ecosystem Components

### AI Teacher

An intelligent conversational tutor capable of adapting responses based on student weaknesses, interests, and learning history.

### Learning Memory

Persistent student memory stored in PostgreSQL that tracks:

* Vocabulary usage
* Grammar patterns
* Interests
* Progress metrics
* Historical mistakes

### Error Detection Engine

Recognizes recurring ESL mistakes and triggers contextual corrections automatically.

Examples:

* talk English
* she don't
* I have 25 years
* depend of

---

### Adaptive Exercise Engine

Generates contextual exercises based on:

* Student weaknesses
* Recent conversations
* Favorite topics
* Learning goals

Supported exercise formats:

* Multiple Choice
* Fill in the Blank
* Sentence Correction
* Verb Transformation
* Translation Challenges
* Vocabulary Reinforcement

---

### Voice Learning Experience

Complete hands-free learning flow:

* Voice Activity Detection (VAD)
* Speech-to-Text (STT)
* Text-to-Speech (TTS)
* Real-time conversation

---

### Gamification System

Transforms learning into a rewarding experience through:

* XP progression
* Daily streaks
* Achievement badges
* Level milestones
* Learning challenges

---

## 🧩 Core Features

### Pedagogical Intelligence Layer

A deterministic orchestration system responsible for deciding educational actions independently of the LLM.

Features:

* Teacher Action Resolver
* Intervention Probability Engine
* Silent Teacher Logic
* Learning State Management

---

### Smart Correction Engine

Differentiates between:

* Minor mistakes
* Critical mistakes
* Confidence-sensitive situations

This prevents excessive corrections while maintaining natural conversation flow.

---

### Portuguese Explanation Engine

Converts grammar concepts into friendly Brazilian Portuguese explanations.

Example:

Incorrect:

```text
She don't like anime.
```

Correction:

```text
She doesn't like anime.
```

Explanation:

```text
Na terceira pessoa do singular utilizamos "doesn't" em vez de "don't".
```

---

### Dynamic Context Personalization

Exercises automatically incorporate topics the student enjoys.

Examples:

* Technology
* Anime
* Games
* Movies
* Sports
* Business

This significantly increases engagement and retention.

---

## 📊 Current Capabilities

| Feature                 | Status |
| ----------------------- | ------ |
| Adaptive Conversations  | ✅      |
| Grammar Correction      | ✅      |
| Portuguese Explanations | ✅      |
| Persistent Memory       | ✅      |
| Voice Interaction       | ✅      |
| Gamification            | ✅      |
| XP System               | ✅      |
| Achievement System      | ✅      |
| Learning Analytics      | 🚧     |
| Pronunciation Scoring   | 🚧     |
| Multi-Agent Teachers    | 🚧     |

---

## 📱 Application Preview

### Main Conversation Interface

<p align="center">
  <img width="260" alt="AI English Tutor Interface" src="https://github.com/user-attachments/assets/727d0f39-0e07-4c9a-b0a8-79724c7bd2d8">
</p>

<p align="center">
Adaptive glassmorphism interface featuring intelligent tutoring, voice interaction, and personalized learning experiences.
</p>

---

## 🛠 Technology Stack

| Layer      | Technology      |
| ---------- | --------------- |
| Frontend   | Flutter         |
| Backend    | FastAPI         |
| Database   | PostgreSQL      |
| ORM        | SQLAlchemy      |
| Validation | Pydantic        |
| AI Runtime | LM Studio       |
| LLM        | Qwen 2.5        |
| Audio      | STT / TTS / VAD |
| API        | REST            |

---

## 📂 Project Structure

```bash
AI-English-Tutor/
│
├── backend/
│   ├── app/
│   │   ├── services/
│   │   │   ├── chat_service.py
│   │   │   ├── skill_exercise_engine.py
│   │   │   ├── error_pattern_engine.py
│   │   │   ├── exercise_engine.py
│   │   │   └── memory_utils.py
│   │   │
│   │   └── main.py
│   │
│   ├── .env.example
│   └── requirements.txt
│
├── frontend/
│   ├── lib/
│   └── pubspec.yaml
│
├── docs/
│   ├── ARCHITECTURE.md
│   ├── AI_SYSTEM.md
│   ├── GAME_SYSTEM.md
│   └── ROADMAP.md
│
└── README.md
```

---

## 🔌 API Response Example

```json
{
  "grammar_confidence": 0.8,
  "needs_correction": true,
  "teacher_action": "question",
  "correction": "She doesn't like anime.",
  "explanation_pt": "Na terceira pessoa do singular usamos doesn't.",
  "example": "She doesn't like watching movies.",
  "exercise": "",
  "conversation_reply": "Good try! Can you think about how we form negative sentences with she?"
}
```

---

## ⚙ Installation

### Backend

```bash
cd backend

python -m venv venv

source venv/bin/activate
```

Windows:

```bash
venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Create:

```env
DATABASE_URL=postgresql://USER:PASSWORD@localhost:5432/DATABASE_NAME

LM_STUDIO_URL=http://localhost:1234/v1/chat/completions

LM_STUDIO_MODEL=qwen2.5-7b-instruct
```

Run:

```bash
uvicorn app.main:app --reload
```

---

### Frontend

```bash
cd frontend

flutter pub get

flutter run
```

---

## 🗺 Product Roadmap

### Phase 1

✅ Conversational Tutor

### Phase 2

✅ Grammar Intelligence

### Phase 3

✅ Voice Learning

### Phase 4

✅ Gamification

### Phase 5

🚧 Learning Analytics Dashboard

### Phase 6

🚧 Personalized Study Plans

### Phase 7

🚧 Pronunciation Scoring

### Phase 8

🚧 Multi-Agent Teaching System

### Phase 9

🚧 Cloud Synchronization

### Phase 10

🚧 Community Learning Marketplace

---

## 🌟 Why This Project Is Different

Most AI learning applications simply wrap a language model.

AI English Tutor introduces a deterministic pedagogical layer capable of analyzing, guiding, correcting, motivating, and adapting learning experiences over time.

This transforms the system from a chatbot into a genuine AI-powered educational platform.

---

## 🎯 Vision

Our mission is to democratize high-quality language education through locally powered artificial intelligence.

We believe every student deserves access to a tutor capable of understanding their weaknesses, adapting to their pace, encouraging progress, and evolving alongside them.

The long-term goal is to create a complete educational ecosystem capable of delivering world-class language instruction directly from consumer hardware without requiring cloud dependency.
