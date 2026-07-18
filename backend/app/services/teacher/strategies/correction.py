from __future__ import annotations

from app.services.teacher.strategies.base import (
    TeacherStrategy,
)


class CorrectionStrategy(TeacherStrategy):
    """
    Estratégia responsável pelas respostas
    de correção gramatical.

    A pedagogia já foi definida pelo
    TeachingEngine.
    """

    def matches(
        self,
        grammar,
        pedagogical,
    ) -> bool:

        return grammar.has_errors

    def build(
        self,
        brain_state,
    ) -> None:

        # A estratégia pedagógica já foi construída
        # pelo TeachingEngine.
        #
        # Nesta fase a CorrectionStrategy não precisa
        # modificar nada.

        return
