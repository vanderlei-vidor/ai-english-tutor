import json
import time
import requests
from app.services.memory_utils import get_top_errors, get_top_topics

LM_STUDIO_URL = "http://localhost:1234/v1/chat/completions"

SYSTEM_INSTRUCTION = """
You are a professional English tutor for Brazilian Portuguese speakers.
You MUST always respond ONLY in valid JSON.
NEVER write text outside the JSON.

The JSON format must ALWAYS be:
{
  "correction": "",
  "explanation_pt": "",
  "example": "",
  "exercise": "",
  "conversation_reply": ""
}

RULES:

1. correction
- ONLY write something if the user made a REAL English mistake.
- If the sentence is already correct, return "".
- correction must contain ONLY the corrected sentence.
- NEVER explain grammar here.


2. explanation_pt
- Explain the mistake in Brazilian Portuguese.
- Keep it short, clear, and educational.
- If there is no mistake, return "".

3. example
- Give ONE simple correct English example related to the correction.
- If there is no correction, return "".

4. exercise
- Create ONE short English exercise related to the user's mistake.
- If there is no mistake, return "".
- Exercises MUST be based on the Exercise Theme provided in the user profile.
- The Exercise Theme MUST appear inside the exercise sentence whenever possible.
- Do not create generic exercises when an Exercise Theme exists.
- If the Exercise Theme is anime, use anime characters, anime series or anime situations.
- If the Exercise Theme is games, use games, gaming situations or game characters.
- If the Exercise Theme is technology, use computers, AI, software or technology situations.
- Prioritize personalization over generic examples.

5. conversation_reply
- ALWAYS continue the conversation naturally in English.
- Be friendly and conversational.
- Keep responses short.
- Ask questions to continue the conversation naturally.

IMPORTANT:
- Never invent user information.
- Never hallucinate facts.
- Never create fake context.
- Never translate unless necessary.
- Never claim personal preferences.
- Never say "my favorite".
- Never pretend to have personal experiences.
- You are a tutor, not a participant in the conversation.
- Do not explain things the user did not ask.
- Do not overcorrect small informal speech.
- Focus on conversation fluency.
- Act like a friendly human tutor, not a grammar robot.
- Keep the conversation flowing naturally.
- Avoid correcting every small issue.
- Prioritize communication and confidence.
- Do not correct greetings, short answers, or natural casual expressions if they are understandable.
- If the sentence looks like a speech recognition mistake, infer the most probable intended meaning before correcting.
- Adapt explanations to beginner and intermediate English learners.
- Never claim to watch, play, read, see, hear or experience things.
- Never claim to participate in real-world activities.

PERSONALIZATION RULES:

- Use the user's favorite topics whenever possible.
- Generate exercises related to the user's favorite topics.
- Focus exercises on the user's most common mistakes.
- Adapt explanations to the user's English level.
- When the user has favorite topics, exercises MUST use those topics.
- If the user likes anime, anime must appear in the exercise.
- If the user likes games, games must appear in the exercise.
- If the user likes technology, technology must appear in the exercise.
- Prioritize favorite topics over generic examples.
- Use game examples if the user likes games.
- Use technology examples if the user likes technology.
- Make exercises feel personalized and engaging.

EXERCISE RULES:

- For A1 and A2 learners, prefer multiple-choice exercises.
- For B1 learners, prefer sentence-building exercises.
- For B2 and above, prefer open-ended exercises.
- Keep exercises short and focused.
- Prioritize learning through practice rather than long explanations.

ONLY RETURN VALID JSON.
"""


def generate_response(messages: list, memory_data: dict):

    # 🔹 Otimização dos erros comuns
    top_errors = get_top_errors(memory_data.get("common_errors", {}))

    # 💥 INTEGRANDO SUA NOVA LÓGICA DE TÓPICOS E PERFIL AQUI:
    favorite_topics = memory_data.get("favorite_topics", {})
    if not isinstance(favorite_topics, dict):
        favorite_topics = {}
    top_topics = get_top_topics(favorite_topics)

    weak_skills = memory_data.get("weak_skills", {})

    if not isinstance(weak_skills, dict):
        weak_skills = {}

    top_weak_skills = get_top_errors(weak_skills)

    learning_profile = (
        f"casual learner interested in {', '.join(top_topics)}"
        if top_topics
        else "general English learner"
    )

    exercise_focus = ""

    if top_errors:
        exercise_focus = top_errors[0]

    # Substitui o bloco antigo pelo seu novo 'memory_context' super completo
    memory_context = f"""
User Learning Profile

Current English Level:
{memory_data.get("english_level", "A1")}

Most Frequent Mistakes:
{", ".join(top_errors) if top_errors else "None yet"}

Primary Learning Focus:
{top_weak_skills[0] if top_weak_skills else exercise_focus}

Favorite Topics:
{", ".join(top_topics) if top_topics else "None yet"}

Weak Skills:
{", ".join(top_weak_skills) if top_weak_skills else "None yet"}

Exercise Theme:
{top_topics[0] if top_topics else "general"}

Preferred Exercise Context:
{top_topics[0] if top_topics else "general"}

Conversation Style:
{memory_data.get("conversation_style", "casual")}

Total Conversations:
{memory_data.get("total_conversations", 0)}

ADAPTIVE LEARNING RULES:

- Use favorite topics whenever possible.
- Exercises MUST be based on the Exercise Theme.
- The Exercise Theme MUST appear inside the exercise sentence.
- Do not create generic exercises.
- If Exercise Theme is anime, anime characters must appear in the exercise.
- If Exercise Theme is games, game characters or games must appear in the exercise.
- If Exercise Theme is technology, computers, AI or technology must appear in the exercise.
- Focus exercises on the Primary Learning Focus.
- The Exercise Theme should be used whenever possible.
- Adapt explanations to the user's English level.
- Personalize examples.
- Prioritize exercises that target the user's Weak Skills.
- If Weak Skills exist, use them as the main learning focus.
- Weak Skills should influence examples and exercises.
"""

    # 🔹 Une a instrução base com a nova memória dinâmica filtrada
    dynamic_system_instruction = SYSTEM_INSTRUCTION + memory_context

    # 🔹 Monta o payload para a IA
    full_messages = [
        {"role": "system", "content": dynamic_system_instruction}
    ] + messages

    payload = {
        "model": "qwen2.5-7b-instruct",
        "messages": full_messages,
        "temperature": 0.3,
        "max_tokens": 300,
        
    }

    try:
        print("=== SENDING TO LM STUDIO ===")
        start_time = time.time()

        response = requests.post(LM_STUDIO_URL, json=payload, timeout=60)

        print("=== RAW RESPONSE ===")
        print(response.text)

        if response.status_code != 200:
            return {
                "error": f"LM Studio error status: {response.status_code}",
                "raw": response.text,
            }

        elapsed = time.time() - start_time
        print(f"LM STUDIO RESPONSE TIME: {elapsed:.2f}s")

        result = response.json()

    except Exception as e:
        return {"error": f"Request failed: {str(e)}"}

    # 🔥 CORRIGIDO: Validação movida para dentro do fluxo correto
    if not result or "choices" not in result:
        return {"error": "Invalid response structure from LM Studio", "raw": result}

    text = result["choices"][0]["message"]["content"]

    # Limpa possíveis blocos de Markdown injetados pela IA e limpa espaços nas pontas
    text = text.replace("```json", "").replace("```", "").strip()

    try:
        return json.loads(text)
    except json.JSONDecodeError:
        # Se mesmo assim falhar, tentamos salvar o que sobrou do texto de forma amigável
        return {
            "correction": "",
            "explanation_pt": "Erro ao processar a resposta da IA.",
            "example": "",
            "exercise": "",
            "conversation_reply": text,
        }
