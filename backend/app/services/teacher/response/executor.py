from __future__ import annotations

from typing import Any

from app.services.teacher.brain.state import (
    TeacherBrainState,
)

from .builder import (
    teacher_response_builder,
)

from .serializer import (
    teacher_response_serializer,
)


class TeacherOutput:
    """
    Responsável apenas por orquestrar
    a construção da resposta do Teacher.

    Não toma decisões.
    Não monta JSON.
    Não conhece o Flutter.

    Apenas conecta:

        Brain
            ↓
        ResponseBuilder
            ↓
        ResponseSerializer
    """

    def apply(
        self,
        brain: TeacherBrainState,
        llm_response: dict[str, Any],
    ) -> dict[str, Any]:

        response = teacher_response_builder.build(
            brain=brain,
            llm_response=llm_response,
        )

        return teacher_response_serializer.serialize(
            response,
        )


teacher_output = TeacherOutput()

# -------------------------------------------------------
# Compatibilidade temporária
# -------------------------------------------------------

teacher_response_executor = teacher_output
