from __future__ import annotations

from .models import (
    TeacherPrompt,
)


class TeacherPromptBuilder:
    def build(
        self,
        action_plan,
    ) -> TeacherPrompt:

        prompt = TeacherPrompt()

        prompt.mode = action_plan.teaching_mode
        prompt.action = action_plan.action
        prompt.tone = action_plan.tone
        prompt.style = action_plan.response_style
        prompt.goal = action_plan.goal
        prompt.target_skill = action_plan.target_skill
        prompt.explanation_level = action_plan.explanation_level
        prompt.generate_example = action_plan.generate_example
        prompt.generate_exercise = action_plan.generate_exercise
        prompt.ask_question = action_plan.ask_question
        prompt.wait_student = action_plan.wait_for_student

        # Chamadas dos métodos auxiliares ordenadas conforme sua lógica
        self._build_action_instructions(
            prompt,
        )

        if prompt.action == "correction":

            self._build_skill_instructions(
                prompt,
            )

        self._build_constraints(
            prompt,
        )

        return prompt

    def _build_action_instructions(
        self,
        prompt: TeacherPrompt,
    ) -> None:

        match prompt.action:
            case "correction":
                prompt.instructions.extend(
                    [
                        "Correct only the student's mistake.",
                        "Explain briefly.",
                        "Be encouraging.",
                        "Keep the conversation context.",
                        "Wait for the student's answer.",
                    ]
                )

            case "exercise":
                prompt.instructions.extend(
                    [
                        "Generate one exercise.",
                        "Do not reveal the answer.",
                        "Wait for the student's response.",
                    ]
                )

            case "praise":
                prompt.instructions.extend(
                    [
                        "Praise the student.",
                        "Keep the conversation natural.",
                        "Encourage the student.",
                    ]
                )

            case _:
                prompt.instructions.extend(
                    [
                        "Answer naturally.",
                        "Keep the conversation flowing.",
                    ]
                )

    # Novo método auxiliar para mapear as habilidades (skills) do aluno
    def _build_skill_instructions(
        self,
        prompt: TeacherPrompt,
    ) -> None:

        match prompt.target_skill:
            case "past_tense":
                prompt.instructions.extend(
                    [
                        "Focus only on the past tense error.",
                        "Mention the past time marker.",
                        "Give one corrected example.",
                    ]
                )

            case "articles":
                prompt.instructions.extend(
                    [
                        "Explain article usage.",
                        "Contrast a, an and the.",
                        "Use one simple example.",
                    ]
                )

            case "prepositions":
                prompt.instructions.extend(
                    [
                        "Focus only on the incorrect preposition.",
                        "Use one location example.",
                        "Avoid explaining other grammar topics.",
                    ]
                )

            case "verb_usage":
                prompt.instructions.extend(
                    [
                        "Explain the correct verb form.",
                        "Keep the explanation short.",
                        "Show one corrected sentence.",
                    ]
                )

            case "third_person":
                prompt.instructions.extend(
                    [
                        "Explain third person singular.",
                        "Mention the verb ending.",
                        "Provide one example.",
                    ]
                )

            case _:
                pass

    def _build_constraints(
        self,
        prompt: TeacherPrompt,
    ) -> None:

        match prompt.action:
            case "correction":
                prompt.constraints.extend(
                    [
                        "Do not explain another grammar topic.",
                        "Do not generate exercises.",
                        "Keep the explanation short.",
                    ]
                )

            case "exercise":
                prompt.constraints.extend(
                    [
                        "Do not reveal the solution.",
                        "Ask only one question.",
                    ]
                )

            case _:
                pass


teacher_prompt_builder = TeacherPromptBuilder()
