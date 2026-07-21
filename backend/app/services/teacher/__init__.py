"""
Teacher Module __init__.py

Exporta os principais componentes da arquitetura do Teacher.
"""

from .brain.engine import (
    TeacherBrain,
)

from .pedagogy.engine import (
    teaching_engine,
)

from .lesson.manager import (
    lesson_manager,
)

__all__ = [
    "TeacherBrain",
    "teaching_engine",
    "lesson_manager",
]
