from __future__ import annotations


class TeacherLogger:
    # ==========================================================
    # Estilização & Helpers de Interface
    # ==========================================================

    def _section(self, title: str) -> None:
        """Imprime um divisor visual de seção."""
        print()
        print("-" * 60)
        print(title)
        print("-" * 60)

    def _field(self, name: str, value: any) -> None:
        """Imprime um campo formatado com alinhamento padrão."""
        if isinstance(value, float):
            value = f"{value:.2f}"
        print(f"{name:<22} {value}")

    def _bullet_list(self, title: str, items: list[str]) -> None:
        """Imprime uma lista de itens com bullets de forma elegante."""
        if not items:
            return
        print(f"\n{title}:")
        for item in items:
            print(f"  • {item}")

    # ==========================================================
    # Componentes do Logger (Orientado a Componentes)
    # ==========================================================

    def _grammar(self, state) -> None:
        self._section("GRAMMAR")
        self._field("HAS ERROR", getattr(state, "has_error", None))
        self._field("CURRENT FOCUS", getattr(state, "current_focus", None))

        # ------------------------------------------------------
        # SKILL FOCUS (Simplificado para o Presente / Teacher Brain)
        # ------------------------------------------------------
        self._section("SKILL FOCUS")

        skill_focus = getattr(state, "skill_focus", None)
        self._field("DETECTED", getattr(skill_focus, "detected", None))
        self._field("TEACHING", getattr(skill_focus, "teaching", None))

    def _pedagogical_memory(self, state, student) -> None:
        # ------------------------------------------------------
        # PEDAGOGICAL MEMORY (Histórico de Longo Prazo)
        # ------------------------------------------------------
        self._section("PEDAGOGICAL MEMORY")

        skill_focus = getattr(state, "skill_focus", None) if state else None

        # Atributos do histórico vindos do Estado Atual (Brain)
        self._field("RECOMMENDED", getattr(skill_focus, "recommended", None))
        self._field("WEAKEST", getattr(skill_focus, "weakest", None))

        # Atributos evolutivos vindos do Perfil do Aluno (Student)
        mastery = getattr(student, "mastery", None) if student else None
        # Formata em porcentagem se for um float válido (Ex: 0.17 -> 17%)
        if isinstance(mastery, float) and mastery <= 1.0:
            mastery_format = f"{mastery * 100:.0f}%"
        else:
            mastery_format = mastery

        self._field("MASTERY", mastery_format)
        self._field(
            "REVIEW", getattr(student, "review_required", None) if student else None
        )
        self._field(
            "EXERCISE", getattr(student, "exercise_required", None) if student else None
        )

    def _student(self, student) -> None:
        self._section("STUDENT")
        self._field("USER ID", getattr(student, "user_id", None))
        self._field("LEVEL", getattr(student, "estimated_level", None))
        self._field("CURRENT SKILL", getattr(student, "current_skill", None))
        self._field("MASTERY", getattr(student, "mastery", None))
        self._field("ACCURACY", getattr(student, "accuracy", None))
        self._field("LEARNING SPEED", getattr(student, "learning_speed", None))
        self._field("LAST SKILL", getattr(student, "last_skill", None))
        self._field("LAST ERROR", getattr(student, "last_error", None))
        self._field("CONSECUTIVE ERRORS", getattr(student, "consecutive_errors", None))
        self._field(
            "CONSECUTIVE SUCCESSES", getattr(student, "consecutive_successes", None)
        )

        self._bullet_list("WEAK SKILLS", getattr(student, "weak_skills", []))
        self._bullet_list("STRONG SKILLS", getattr(student, "strong_skills", []))

    def _lesson(self, state) -> None:
        self._section("LESSON")
        self._field("ACTIVE", getattr(state, "lesson_active", None))
        self._field("GOAL", getattr(state, "lesson_goal", None))
        self._field("PHASE", getattr(state, "lesson_phase", None))

        step = getattr(state, "lesson_step", None)
        total = getattr(state, "lesson_total_steps", None)
        step_format = (
            f"{step}/{total}" if step is not None and total is not None else None
        )
        self._field("STEP", step_format)

    def _decision(self, state) -> None:
        self._section("DECISION")
        self._field("ACTION", getattr(state, "teacher_action", None))
        self._field("MODE", getattr(state, "teacher_mode", None))
        self._field("STYLE", getattr(state, "response_style", None))
        self._field("TONE", getattr(state, "tone", None))
        self._field("REASON", getattr(state, "teacher_reason", None))

    def _teaching(self, teaching) -> None:
        self._section("TEACHING")
        self._field("STRATEGY", getattr(teaching, "strategy", None))
        self._field("EXPLANATION", getattr(teaching, "explanation_style", None))
        self._field("FEEDBACK", getattr(teaching, "feedback_style", None))
        self._field("QUESTION", getattr(teaching, "question_style", None))
        self._field("EXAMPLE", getattr(teaching, "example_style", None))
        self._field("EXERCISE", getattr(teaching, "exercise_style", None))
        self._field("REVEAL ANSWER", getattr(teaching, "reveal_answer", None))
        self._field("WAIT STUDENT", getattr(teaching, "wait_student", None))

        explanation = getattr(teaching, "explanation", None)
        self._field("DIFFICULTY", getattr(explanation, "difficulty", None))
        self._field("SCAFFOLDING", getattr(explanation, "scaffolding", None))

    def _prompt(self, state) -> None:
        instructions = getattr(state, "instructions", [])
        constraints = getattr(state, "constraints", [])

        if instructions or constraints:
            self._section("PROMPT")
            self._bullet_list("INSTRUCTIONS", instructions)
            self._bullet_list("CONSTRAINTS", constraints)

    # ==========================================================
    # Métodos Públicos (Orquestradores)
    # ==========================================================

    def brain(self, brain_state) -> None:
        """
        Orquestra a exibição do estado global unificado do Teacher Brain.
        """
        state = getattr(brain_state, "state", None)
        student = getattr(brain_state, "student", None)
        teaching = getattr(brain_state, "teaching", None)

        print()
        print("=" * 60)
        print("TEACHER BRAIN 3.0 (COMPONENTS-BASED)")
        print("=" * 60)

        if state:
            self._grammar(state)

        # Executa a memória pedagógica cruzando dados de estado e do estudante
        if state or student:
            self._pedagogical_memory(state, student)

        if student:
            self._student(student)

        if state:
            self._lesson(state)
            self._decision(state)

        if teaching:
            self._teaching(teaching)

        if state:
            self._prompt(state)

        print()
        print("=" * 60)


# Inicialização padrão
teacher_logger = TeacherLogger()
