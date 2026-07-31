import requests

OLLAMA_URL = "http://127.0.0.1:11434/api/chat"
DEFAULT_MODEL = "qwen2.5:3b"

SYSTEM_PROMPT = """
Tu es CyberMind AI, un assistant local spécialisé en informatique,
Linux et cybersécurité défensive.

Règles :
- Réponds principalement en français.
- Utilise un langage clair, naturel et précis.
- Donne des définitions techniquement correctes.
- Structure les réponses avec des paragraphes et des listes courtes.
- Ne prétends jamais avoir exécuté une action non réalisée.
- Privilégie la prévention, l'analyse défensive et les environnements autorisés.
""".strip()


def chat_with_ollama(
    user_message: str,
    history: list[dict[str, str]] | None = None,
    model: str = DEFAULT_MODEL,
    temperature: float = 0.6,
    max_tokens: int = 700,
) -> str:
    if not user_message.strip():
        return "Veuillez écrire une question."

    messages = [{"role": "system", "content": SYSTEM_PROMPT}]

    if history:
        messages.extend(history)

    messages.append({
        "role": "user",
        "content": user_message.strip(),
    })

    payload = {
        "model": model,
        "messages": messages,
        "stream": False,
        "options": {
            "temperature": float(temperature),
            "num_predict": int(max_tokens),
        },
    }

    try:
        response = requests.post(
            OLLAMA_URL,
            json=payload,
            timeout=240,
        )
        response.raise_for_status()

        data = response.json()
        return data["message"]["content"].strip()

    except requests.ConnectionError:
        return (
            "Impossible de contacter Ollama. "
            "Vérifie que le service Ollama est actif."
        )

    except requests.Timeout:
        return "Le modèle a mis trop de temps à répondre."

    except (requests.RequestException, KeyError, ValueError) as error:
        return f"Erreur Ollama : {error}"
