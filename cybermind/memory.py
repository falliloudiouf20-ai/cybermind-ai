import json
from datetime import datetime
from pathlib import Path
from uuid import uuid4

CONVERSATIONS_DIR = Path("conversations")
CONVERSATIONS_DIR.mkdir(exist_ok=True)


def new_conversation() -> str:
    conversation_id = (
        datetime.now().strftime("%Y%m%d-%H%M%S")
        + "-"
        + uuid4().hex[:6]
    )
    save_conversation(conversation_id, [])
    return conversation_id


def save_conversation(
    conversation_id: str,
    messages: list[dict[str, str]],
) -> None:
    path = CONVERSATIONS_DIR / f"{conversation_id}.json"

    data = {
        "id": conversation_id,
        "updated_at": datetime.now().isoformat(timespec="seconds"),
        "messages": messages,
    }

    path.write_text(
        json.dumps(data, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )


def load_conversation(
    conversation_id: str | None,
) -> list[dict[str, str]]:
    if not conversation_id:
        return []

    path = CONVERSATIONS_DIR / f"{conversation_id}.json"

    if not path.exists():
        return []

    try:
        data = json.loads(path.read_text(encoding="utf-8"))
        return data.get("messages", [])
    except (json.JSONDecodeError, OSError):
        return []


def list_conversations() -> list[str]:
    files = sorted(
        CONVERSATIONS_DIR.glob("*.json"),
        key=lambda file: file.stat().st_mtime,
        reverse=True,
    )
    return [file.stem for file in files]


def delete_conversation(conversation_id: str | None) -> None:
    if not conversation_id:
        return

    path = CONVERSATIONS_DIR / f"{conversation_id}.json"

    if path.exists():
        path.unlink()
