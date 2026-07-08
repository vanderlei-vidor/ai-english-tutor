from __future__ import annotations

from app.services.debug.grammar_logger import grammar_logger
from app.services.debug.pedagogical_logger import pedagogical_logger
from app.services.debug.migration_logger import migration_logger
from app.services.debug.sanitizer_logger import sanitizer_logger
from app.services.debug.memory_logger import memory_logger
from app.services.debug.skill_logger import skill_logger
from app.services.debug.llm_logger import llm_logger


class DebugManager:
    grammar = grammar_logger

    pedagogical = pedagogical_logger

    migration = migration_logger

    sanitizer = sanitizer_logger

    memory = memory_logger

    skill = skill_logger

    llm = llm_logger


debug = DebugManager()
