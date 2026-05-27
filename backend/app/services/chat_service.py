import requests
import json
import time

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

ONLY RETURN VALID JSON.
"""

def generate_response(messages: list, memory_data: dict):

    # 🔹 Otimização dos erros comuns
    common_errors = memory_data.get("common_errors", {})
    if not isinstance(common_errors, dict):
        common_errors = {}

    sorted_errors = sorted(
        common_errors.items(),
        key=lambda x: x[1],
        reverse=True
    )

    top_errors = [
        error[0]
        for error in sorted_errors[:3]
    ]

    # 💥 INTEGRANDO SUA NOVA LÓGICA DE TÓPICOS E PERFIL AQUI:
    favorite_topics = memory_data.get(
        "favorite_topics",
        []
    )

    learning_profile = (
        f"casual learner interested in "
        f"{', '.join(favorite_topics)}"
        if favorite_topics
        else "general English learner"
    )

    # Substitui o bloco antigo pelo seu novo 'memory_context' super completo
    memory_context = f"""
User profile:
- English level: {memory_data.get("english_level", "A1")}
- Most common mistakes: {", ".join(top_errors) if top_errors else "None yet"}
- Preferred style: {memory_data.get("conversation_style", "casual")}
- Total conversations: {memory_data.get("total_conversations", 0)}
- Favorite topics: {", ".join(favorite_topics) if favorite_topics else "None yet"}
- Learning profile: {learning_profile}
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
        "max_tokens": 300
    }

    try:
        print("=== SENDING TO LM STUDIO ===")
        print(messages)
        start_time = time.time()

        response = requests.post(
            LM_STUDIO_URL,
            json=payload,
            timeout=60
        )
        print("=== RAW RESPONSE ===")
        print(response.text)
        if response.status_code != 200:
            return {
                "error": f"LM Studio error: {response.status_code}"
            }
        elapsed = time.time() - start_time

        print(f"LM STUDIO RESPONSE TIME: {elapsed:.2f}s")

        result = response.json()

    except Exception as e:
        return {
            "error": str(e)
        }

    if "error" in result:
        return {"error": result["error"]}

    text = result["choices"][0]["message"]["content"]
    
    # Limpa possíveis blocos de Markdown injetados pela IA
    text = text.replace("```json", "").replace("```", "").strip()

    try:
        return json.loads(text)
    except:
        return {
            "correction": "",
            "explanation_pt": "",
            "example": "",
            "exercise": "",
            "conversation_reply": text
        }