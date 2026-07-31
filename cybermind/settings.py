import json
from pathlib import Path

SETTINGS_PATH = Path("config/settings.json")

DEFAULT_SETTINGS = {
    "model": "qwen2.5:3b",
    "temperature": 0.6,
    "max_tokens": 700,
}


def load_settings() -> dict:
    SETTINGS_PATH.parent.mkdir(exist_ok=True)

    if not SETTINGS_PATH.exists():
        save_settings(DEFAULT_SETTINGS)
        return DEFAULT_SETTINGS.copy()

    try:
        saved = json.loads(SETTINGS_PATH.read_text(encoding="utf-8"))
        return {**DEFAULT_SETTINGS, **saved}
    except (json.JSONDecodeError, OSError):
        return DEFAULT_SETTINGS.copy()


def save_settings(
    model: str,
    temperature: float,
    max_tokens: int,
) -> str:
    settings = {
        "model": model,
        "temperature": float(temperature),
        "max_tokens": int(max_tokens),
    }

    SETTINGS_PATH.parent.mkdir(exist_ok=True)
    SETTINGS_PATH.write_text(
        json.dumps(settings, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    return "✅ Paramètres enregistrés"
