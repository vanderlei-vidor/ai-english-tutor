from __future__ import annotations


class QuestionPurposeBuilder:
    """
    Produz instruções de ensino concretas — não apenas meta-instruções genéricas.
    """

    _SKILL_TEACHING: dict[str, dict[str, str]] = {
        "past_tense": {
            "initial_question": (
                'Which tense normally follows time markers like "yesterday"?'
            ),
            "guide_thinking": (
                'Yesterday tells us something happened in the past. '
                'Can you think of another form of "go"?'
            ),
            "deepen_question": (
                'If the action already happened, what form should the verb take?'
            ),
            "guide_contradiction": (
                '"Yesterday" points to the past — does the present form of "go" '
                "still fit here?"
            ),
            "lead_to_conclusion": (
                "What is the past form of the verb you used?"
            ),
        },
        "verb_usage": {
            "initial_question": (
                'When talking about languages, which verb do we normally use — '
                '"talk" or "speak"?'
            ),
            "guide_thinking": (
                'Think about how native speakers say "I ___ English." '
                "Which verb sounds natural?"
            ),
            "lead_to_conclusion": (
                'What verb do we use when saying we know a language?'
            ),
        },
        "third_person": {
            "initial_question": (
                'With "she" or "he", what form of "do" do we use in negative '
                "sentences?"
            ),
            "guide_thinking": (
                'Third person is different from "I" or "you". '
                'What happens to "don\'t" with he/she/it?'
            ),
            "lead_to_conclusion": (
                'How do we make "She don\'t" grammatically correct?'
            ),
        },
        "articles": {
            "initial_question": (
                "Before a singular countable noun, do we need something extra?"
            ),
            "guide_thinking": (
                'Look at the noun after the verb — is it specific or general? '
                "Does it need an article?"
            ),
            "lead_to_conclusion": (
                'Which article (a, an, or the) fits before this noun?'
            ),
        },
        "prepositions": {
            "initial_question": (
                "Which preposition usually goes with this verb or adjective?"
            ),
            "guide_thinking": (
                "Think about the fixed phrase — which preposition "
                "collocates with this word?"
            ),
            "lead_to_conclusion": (
                "What is the correct preposition in this context?"
            ),
        },
        "nouns": {
            "initial_question": (
                "Is this noun countable or uncountable in English?"
            ),
            "guide_thinking": (
                "Can you count this noun? Does English allow a plural here?"
            ),
            "lead_to_conclusion": (
                "What is the correct singular/plural form?"
            ),
        },
    }

    def build(
        self,
        purpose: str,
        target_skill: str | None = None,
    ) -> str:
        if target_skill:
            skill_hints = self._SKILL_TEACHING.get(target_skill, {})
            if purpose in skill_hints:
                return skill_hints[purpose]

        match purpose:
            case "activate_prior_knowledge":
                return (
                    "Ask a question that connects to what the student already knows. "
                    "Do not explain the grammar yet."
                )

            case "guide_thinking":
                return (
                    "Guide the student to discover the rule through a concrete question. "
                    "Do not reveal the answer."
                )

            case "validate_understanding":
                return (
                    "Ask one question to check whether the student understood the concept."
                )

            case "pose_question":
                return (
                    "Ask the student to think before giving any explanation."
                )

            case "student_solves":
                return (
                    "Invite the student to fix the sentence independently."
                )

            case "initial_question":
                return (
                    "Start with a broad, concrete question about the grammar point."
                )

            case "deepen_question":
                return (
                    "Ask a deeper follow-up based on the student's reasoning."
                )

            case "guide_contradiction":
                return (
                    "Help the student notice the contradiction in their sentence."
                )

            case "lead_to_conclusion":
                return (
                    "Lead the student to reach the correct form by themselves."
                )

            case "practice_communication":
                return (
                    "Encourage the student to use the correct form in a natural reply."
                )

            case "encourage_continuation":
                return (
                    "Encourage the student to continue the conversation naturally."
                )

            case _:
                return "Ask one clear, teaching-focused question."
