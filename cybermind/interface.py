from typing import Any

import gradio as gr

from cybermind.memory import (
    delete_conversation,
    list_conversations,
    load_conversation,
    new_conversation,
    save_conversation,
)
from cybermind.ollama_client import chat_with_ollama
from cybermind.settings import load_settings, save_settings


APP_NAME = "CyberMind-AI"


HERO_HTML = """
<div class="cyber-home">
    <div class="matrix matrix-left">
        01001<br>10110<br>00101<br>11010<br>01011<br>10101
    </div>

    <div class="matrix matrix-right">
        10110<br>00101<br>11001<br>01010<br>10101<br>00110
    </div>

    <div class="online-badge">
        <span></span>
        IA locale connectée
    </div>

    <div class="scanner">
        <div class="orbit orbit-one"></div>
        <div class="orbit orbit-two"></div>
        <div class="orbit orbit-three"></div>
        <div class="orbit orbit-four"></div>
        <div class="radar-line"></div>
        <div class="scanner-glow"></div>

        <div class="shield-logo">
            <svg viewBox="0 0 150 170" aria-hidden="true">
                <path
                    d="M75 7 L135 31 V78
                       C135 119 109 148 75 164
                       C41 148 15 119 15 78
                       V31 Z"
                    fill="none"
                    stroke="currentColor"
                    stroke-width="6"
                />

                <path
                    d="M75 40
                       C58 25 40 39 45 57
                       C27 65 33 88 52 88
                       C46 107 65 118 75 101

                       M75 40
                       C92 25 110 39 105 57
                       C123 65 117 88 98 88
                       C104 107 85 118 75 101

                       M75 40 V119"
                    fill="none"
                    stroke="currentColor"
                    stroke-width="5"
                    stroke-linecap="round"
                    stroke-linejoin="round"
                />

                <circle cx="53" cy="57" r="4" fill="currentColor"/>
                <circle cx="97" cy="57" r="4" fill="currentColor"/>
                <circle cx="49" cy="84" r="4" fill="currentColor"/>
                <circle cx="101" cy="84" r="4" fill="currentColor"/>
            </svg>
        </div>
    </div>

    <h1>CyberMind-AI</h1>
    <p>Votre assistant IA local en cybersécurité</p>
</div>
"""


CUSTOM_CSS = """
:root {
    --green: #45f58a;
    --green-bright: #62ff9c;
    --green-soft: rgba(69, 245, 138, 0.13);
    --background: #030709;
    --background-two: #071017;
    --panel: rgba(7, 12, 16, 0.98);
    --surface: rgba(15, 22, 28, 0.92);
    --border: rgba(69, 245, 138, 0.22);
    --text: #edf7f0;
    --muted: #819087;
}

html,
body {
    margin: 0 !important;
    min-height: 100%;
    background: var(--background) !important;
}

body {
    overflow: hidden;
}

.gradio-container {
    width: 100% !important;
    max-width: none !important;
    min-height: 100vh !important;
    margin: 0 !important;
    padding: 0 !important;
    color: var(--text) !important;
    background:
        radial-gradient(
            circle at 50% 42%,
            rgba(35, 140, 80, 0.13),
            transparent 31%
        ),
        linear-gradient(
            180deg,
            var(--background),
            var(--background-two)
        ) !important;
}

/* Fond grille */

.gradio-container::before {
    content: "";
    position: fixed;
    inset: 0;
    z-index: 0;
    pointer-events: none;
    background-image:
        linear-gradient(
            rgba(69, 245, 138, 0.025) 1px,
            transparent 1px
        ),
        linear-gradient(
            90deg,
            rgba(69, 245, 138, 0.025) 1px,
            transparent 1px
        );
    background-size: 52px 52px;
    mask-image: linear-gradient(
        to bottom,
        transparent,
        black 20%,
        black 80%,
        transparent
    );
}

/* Barre supérieure */

#top-header {
    position: fixed;
    z-index: 30;
    top: 0;
    left: 0;
    right: 0;
    height: 66px;
    pointer-events: none;
    background:
        linear-gradient(
            180deg,
            rgba(3, 7, 9, 0.98),
            rgba(3, 7, 9, 0.72)
        );
    border-bottom: 1px solid rgba(69, 245, 138, 0.08);
    backdrop-filter: blur(18px);
}

/* Bouton hamburger */

#hamburger {
    position: fixed !important;
    z-index: 100 !important;
    top: 13px !important;
    left: 18px !important;
    width: 44px !important;
    min-width: 44px !important;
    max-width: 44px !important;
    height: 42px !important;
    min-height: 42px !important;
    padding: 0 !important;
    border: 1px solid var(--border) !important;
    border-radius: 12px !important;
    color: var(--green) !important;
    background: rgba(7, 13, 17, 0.96) !important;
    font-size: 24px !important;
    line-height: 1 !important;
    box-shadow:
        0 0 20px rgba(69, 245, 138, 0.08),
        inset 0 0 15px rgba(69, 245, 138, 0.03);
}

#hamburger:hover {
    border-color: var(--green) !important;
    background: rgba(14, 30, 21, 0.98) !important;
    box-shadow: 0 0 25px rgba(69, 245, 138, 0.24);
}

/* Menu latéral */

#sidebar {
    position: fixed !important;
    z-index: 80 !important;
    top: 0 !important;
    bottom: 0 !important;
    left: 0 !important;
    width: 350px !important;
    max-width: calc(100vw - 24px) !important;
    padding: 82px 18px 20px !important;
    overflow-y: auto !important;
    border-right: 1px solid var(--border) !important;
    background:
        linear-gradient(
            145deg,
            rgba(11, 17, 22, 0.995),
            rgba(3, 7, 10, 0.995)
        ) !important;
    box-shadow:
        25px 0 80px rgba(0, 0, 0, 0.72),
        0 0 45px rgba(69, 245, 138, 0.04);
}

.sidebar-brand {
    margin-bottom: 24px;
    padding: 18px;
    border: 1px solid var(--border);
    border-radius: 17px;
    background:
        linear-gradient(
            145deg,
            rgba(18, 28, 34, 0.88),
            rgba(8, 13, 17, 0.88)
        );
}

.sidebar-brand h2 {
    margin: 0 0 5px;
    color: var(--text);
    font-size: 21px;
}

.sidebar-brand p {
    margin: 0;
    color: var(--green);
    font-size: 12px;
}

.sidebar-title {
    margin: 23px 0 9px !important;
    color: var(--muted) !important;
    font-size: 11px !important;
    font-weight: 700 !important;
    letter-spacing: 1.6px !important;
    text-transform: uppercase;
}

#sidebar button {
    min-height: 42px !important;
    border: 1px solid rgba(255, 255, 255, 0.065) !important;
    border-radius: 11px !important;
    color: var(--text) !important;
    background: rgba(255, 255, 255, 0.035) !important;
}

#sidebar button:hover {
    color: var(--green) !important;
    border-color: var(--border) !important;
    background: var(--green-soft) !important;
}

#sidebar .wrap,
#sidebar .form {
    border-color: rgba(255, 255, 255, 0.07) !important;
    background: rgba(255, 255, 255, 0.035) !important;
}

/* Zone principale */

#main-content {
    position: relative;
    z-index: 2;
    width: min(100%, 1050px);
    height: 100vh;
    margin: 0 auto;
    padding: 72px 24px 18px;
    display: flex !important;
    flex-direction: column !important;
    box-sizing: border-box;
}

/* Écran d'accueil */

#hero {
    flex: 1;
    min-height: 0;
}

.cyber-home {
    position: relative;
    width: 100%;
    height: 100%;
    min-height: 420px;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    overflow: hidden;
    text-align: center;
}

.cyber-home h1 {
    position: relative;
    z-index: 5;
    margin: 20px 0 5px;
    color: var(--text);
    font-size: clamp(37px, 4.5vw, 57px);
    font-weight: 700;
    letter-spacing: -1.7px;
}

.cyber-home p {
    position: relative;
    z-index: 5;
    margin: 0;
    color: var(--green);
    font-size: 15px;
}

.online-badge {
    position: absolute;
    z-index: 7;
    top: 17px;
    left: 50%;
    transform: translateX(-50%);
    padding: 8px 14px;
    white-space: nowrap;
    border: 1px solid rgba(69, 245, 138, 0.16);
    border-radius: 999px;
    color: #a2ffc0;
    background: rgba(7, 19, 13, 0.72);
    font-size: 12px;
    backdrop-filter: blur(10px);
}

.online-badge span {
    display: inline-block;
    width: 7px;
    height: 7px;
    margin-right: 7px;
    border-radius: 50%;
    background: var(--green);
    box-shadow: 0 0 12px var(--green);
    animation: online-pulse 1.5s ease-in-out infinite;
}

.matrix {
    position: absolute;
    top: 5%;
    bottom: 0;
    color: rgba(69, 245, 138, 0.07);
    font-family: monospace;
    font-size: 18px;
    line-height: 2.8;
    letter-spacing: 15px;
    writing-mode: vertical-rl;
    animation: matrix-fall 13s linear infinite;
}

.matrix-left {
    left: 4%;
}

.matrix-right {
    right: 4%;
    animation-delay: -6s;
}

.scanner {
    position: relative;
    z-index: 4;
    width: min(340px, 65vw);
    aspect-ratio: 1;
    display: grid;
    place-items: center;
}

.orbit {
    position: absolute;
    border-radius: 50%;
    border: 1px solid rgba(69, 245, 138, 0.25);
}

.orbit-one {
    inset: 0;
    border-style: dashed;
    animation: rotate-right 18s linear infinite;
}

.orbit-two {
    inset: 8%;
    border-width: 3px;
    border-top-color: var(--green);
    border-right-color: transparent;
    border-bottom-color: rgba(69, 245, 138, 0.09);
    animation: rotate-left 10s linear infinite;
}

.orbit-three {
    inset: 18%;
    border-style: dotted;
    border-width: 2px;
    animation: rotate-right 7s linear infinite;
}

.orbit-four {
    inset: 29%;
    border-width: 2px;
    box-shadow:
        inset 0 0 35px rgba(69, 245, 138, 0.07),
        0 0 55px rgba(69, 245, 138, 0.08);
}

.radar-line {
    position: absolute;
    inset: 6%;
    overflow: hidden;
    border-radius: 50%;
    animation: rotate-right 4.5s linear infinite;
}

.radar-line::before {
    content: "";
    position: absolute;
    top: 50%;
    left: 50%;
    width: 48%;
    height: 2px;
    transform-origin: left center;
    background:
        linear-gradient(
            90deg,
            var(--green),
            transparent
        );
    box-shadow: 0 0 17px var(--green);
}

.scanner-glow {
    position: absolute;
    inset: 19%;
    border-radius: 50%;
    background:
        radial-gradient(
            circle,
            rgba(69, 245, 138, 0.16),
            transparent 66%
        );
    animation: scanner-pulse 2.7s ease-in-out infinite;
}

.shield-logo {
    position: relative;
    z-index: 6;
    width: 115px;
    color: var(--green);
    filter:
        drop-shadow(0 0 10px rgba(69, 245, 138, 0.75))
        drop-shadow(0 0 28px rgba(69, 245, 138, 0.28));
}

.shield-logo svg {
    display: block;
    width: 100%;
}

/* Chat */

#chat-area {
    flex: 1;
    min-height: 0;
    overflow: hidden;
}

#chatbot {
    height: calc(100vh - 220px) !important;
    min-height: 360px !important;
    max-height: none !important;
    border: 0 !important;
    border-radius: 18px !important;
    background: transparent !important;
}

#chatbot > div {
    background: transparent !important;
}

#composer {
    flex: 0 0 auto;
    width: 100%;
    padding: 10px 11px !important;
    border: 1px solid var(--border) !important;
    border-radius: 21px !important;
    background: rgba(14, 20, 26, 0.96) !important;
    box-shadow:
        0 18px 60px rgba(0, 0, 0, 0.5),
        0 0 35px rgba(69, 245, 138, 0.055);
    backdrop-filter: blur(20px);
}

#message-input {
    flex: 1 !important;
}

#message-input textarea {
    min-height: 58px !important;
    max-height: 160px !important;
    padding: 13px 10px !important;
    color: var(--text) !important;
    background: transparent !important;
    border: 0 !important;
    box-shadow: none !important;
    resize: none !important;
}

#send {
    align-self: center !important;
    width: 50px !important;
    min-width: 50px !important;
    max-width: 50px !important;
    height: 50px !important;
    min-height: 50px !important;
    padding: 0 !important;
    border: 0 !important;
    border-radius: 50% !important;
    color: #031109 !important;
    background: var(--green) !important;
    font-size: 24px !important;
    box-shadow: 0 0 25px rgba(69, 245, 138, 0.34);
}

#send:hover {
    transform: translateY(-2px);
    background: var(--green-bright) !important;
    box-shadow: 0 0 33px rgba(69, 245, 138, 0.58);
}

#status {
    flex: 0 0 auto;
    min-height: 26px;
    margin-top: 6px;
    color: var(--muted);
    text-align: center;
    font-size: 11px;
}

/* Mode clair */

body.cyber-light {
    --background: #eaf3ed;
    --background-two: #dfece4;
    --panel: rgba(246, 251, 248, 0.99);
    --surface: rgba(255, 255, 255, 0.92);
    --border: rgba(19, 137, 69, 0.26);
    --text: #102218;
    --muted: #566b5d;
}

body.cyber-light .gradio-container {
    background:
        radial-gradient(
            circle at 50% 40%,
            rgba(35, 160, 85, 0.15),
            transparent 33%
        ),
        linear-gradient(
            180deg,
            var(--background),
            var(--background-two)
        ) !important;
}

body.cyber-light #sidebar {
    background:
        linear-gradient(
            145deg,
            rgba(248, 252, 249, 0.995),
            rgba(229, 240, 233, 0.995)
        ) !important;
}

body.cyber-light #composer {
    background: rgba(255, 255, 255, 0.92) !important;
}

/* Animations */

@keyframes rotate-right {
    to {
        transform: rotate(360deg);
    }
}

@keyframes rotate-left {
    to {
        transform: rotate(-360deg);
    }
}

@keyframes scanner-pulse {
    50% {
        transform: scale(1.09);
        opacity: 0.48;
    }
}

@keyframes online-pulse {
    50% {
        opacity: 0.3;
    }
}

@keyframes matrix-fall {
    from {
        transform: translateY(-15%);
    }

    to {
        transform: translateY(15%);
    }
}

/* Mobile */

@media (max-width: 760px) {
    #main-content {
        padding: 68px 11px 10px;
    }

    #sidebar {
        width: 315px !important;
    }

    .scanner {
        width: min(270px, 70vw);
    }

    .shield-logo {
        width: 88px;
    }

    .cyber-home {
        min-height: 370px;
    }

    .cyber-home h1 {
        margin-top: 14px;
    }

    #chatbot {
        height: calc(100vh - 205px) !important;
    }
}

footer {
    display: none !important;
}
"""


DARK_THEME_JS = """
() => {
    document.body.classList.remove("cyber-light");
    localStorage.setItem("cybermind-theme", "dark");
}
"""


LIGHT_THEME_JS = """
() => {
    document.body.classList.add("cyber-light");
    localStorage.setItem("cybermind-theme", "light");
}
"""


LOAD_THEME_JS = """
() => {
    const theme = localStorage.getItem("cybermind-theme");

    if (theme === "light") {
        document.body.classList.add("cyber-light");
    } else {
        document.body.classList.remove("cyber-light");
    }
}
"""


def make_dropdown(
    choices: list[str],
    value: str | None,
):
    return gr.Dropdown(
        choices=choices,
        value=value,
        label="Historique",
        interactive=True,
    )


def create_start_conversation() -> str:
    """
    L'application démarre toujours sur une nouvelle conversation vide.
    Les anciennes conversations restent accessibles depuis le menu.
    """
    return new_conversation()


def toggle_menu(is_open: bool):
    new_state = not is_open

    return (
        new_state,
        gr.Column(visible=new_state),
    )


def create_new_chat():
    conversation_id = new_conversation()
    choices = list_conversations()

    return (
        [],
        conversation_id,
        make_dropdown(choices, conversation_id),
        gr.HTML(value=HERO_HTML, visible=True),
        gr.Column(visible=False),
        "🔒 Nouvelle conversation locale",
    )


def open_saved_chat(conversation_id):
    if not conversation_id:
        return (
            [],
            None,
            gr.HTML(value=HERO_HTML, visible=True),
            gr.Column(visible=False),
            "Aucune conversation sélectionnée.",
        )

    messages = load_conversation(conversation_id)

    if messages:
        return (
            messages,
            conversation_id,
            gr.HTML(value="", visible=False),
            gr.Column(visible=True),
            f"Conversation chargée · {conversation_id}",
        )

    return (
        [],
        conversation_id,
        gr.HTML(value=HERO_HTML, visible=True),
        gr.Column(visible=False),
        f"Conversation vide · {conversation_id}",
    )


def remove_chat(conversation_id):
    delete_conversation(conversation_id)

    conversations = list_conversations()

    if conversations:
        next_id = conversations[0]
        messages = load_conversation(next_id)
    else:
        next_id = new_conversation()
        conversations = list_conversations()
        messages = []

    has_messages = bool(messages)

    return (
        messages,
        next_id,
        make_dropdown(conversations, next_id),
        gr.HTML(
            value="" if has_messages else HERO_HTML,
            visible=not has_messages,
        ),
        gr.Column(visible=has_messages),
        "Conversation supprimée.",
    )


def refresh_history():
    conversations = list_conversations()

    return make_dropdown(
        conversations,
        conversations[0] if conversations else None,
    )


def change_model(model_name: str):
    settings = load_settings()

    save_settings(
        model=model_name,
        temperature=float(settings.get("temperature", 0.6)),
        max_tokens=int(settings.get("max_tokens", 700)),
    )

    return f"Modèle actif : `{model_name}`"


def normalize_history(
    history: list[dict[str, Any]] | None,
) -> list[dict[str, str]]:
    normalized: list[dict[str, str]] = []

    for item in history or []:
        if not isinstance(item, dict):
            continue

        role = item.get("role")
        content = item.get("content")

        if (
            role in {"user", "assistant"}
            and isinstance(content, str)
            and content.strip()
        ):
            normalized.append(
                {
                    "role": role,
                    "content": content.strip(),
                }
            )

    return normalized


def send_message(
    message,
    history,
    conversation_id,
    model_name,
):
    question = str(message or "").strip()
    chat_history = history or []

    if not question:
        return (
            "",
            chat_history,
            conversation_id,
            gr.HTML(visible=False),
            gr.Column(visible=True),
            "Écris une question avant de l’envoyer.",
        )

    if not conversation_id:
        conversation_id = new_conversation()

    settings = load_settings()

    answer = chat_with_ollama(
        user_message=question,
        history=normalize_history(chat_history),
        model=model_name,
        temperature=float(settings.get("temperature", 0.6)),
        max_tokens=int(settings.get("max_tokens", 700)),
    )

    updated_history = chat_history + [
        {
            "role": "user",
            "content": question,
        },
        {
            "role": "assistant",
            "content": answer,
        },
    ]

    save_conversation(
        conversation_id=conversation_id,
        messages=updated_history,
    )

    return (
        "",
        updated_history,
        conversation_id,
        gr.HTML(value="", visible=False),
        gr.Column(visible=True),
        f"🔒 Conversation sauvegardée · {model_name}",
    )


def build_interface() -> gr.Blocks:
    settings = load_settings()

    initial_id = create_start_conversation()
    initial_choices = list_conversations()

    active_model = settings.get("model", "qwen2.5:3b")

    with gr.Blocks(title=APP_NAME) as demo:
        conversation_state = gr.State(initial_id)
        menu_state = gr.State(False)

        gr.HTML('<div id="top-header"></div>')

        menu_button = gr.Button(
            "☰",
            elem_id="hamburger",
        )

        with gr.Column(
            visible=False,
            elem_id="sidebar",
        ) as sidebar:
            gr.HTML(
                """
                <div class="sidebar-brand">
                    <h2>🛡 CyberMind-AI</h2>
                    <p>Assistant IA local en cybersécurité</p>
                </div>
                """
            )

            gr.Markdown(
                "Historique",
                elem_classes=["sidebar-title"],
            )

            new_button = gr.Button(
                "＋ Nouvelle conversation",
                variant="primary",
            )

            conversation_list = gr.Dropdown(
                choices=initial_choices,
                value=initial_id,
                label="Historique",
                interactive=True,
            )

            with gr.Row():
                refresh_button = gr.Button("↻ Actualiser")
                delete_button = gr.Button("🗑 Supprimer")

            gr.Markdown(
                "Modèles",
                elem_classes=["sidebar-title"],
            )

            model_selector = gr.Radio(
                choices=[
                    "qwen2.5:3b",
                    "qwen2.5:1.5b",
                ],
                value=active_model,
                label="Modèle local",
            )

            model_status = gr.Markdown(
                f"Modèle actif : `{active_model}`"
            )

            gr.Markdown(
                "Thème",
                elem_classes=["sidebar-title"],
            )

            dark_button = gr.Button("☾ Sombre")
            light_button = gr.Button("☀ Clair")

            gr.HTML(
                """
                <div style="
                    margin-top: 28px;
                    padding-top: 18px;
                    border-top: 1px solid rgba(69,245,138,.12);
                    color: #718078;
                    font-size: 11px;
                    line-height: 1.8;
                ">
                    CyberMind-AI v1.0<br>
                    Traitement local avec Ollama
                </div>
                """
            )

        with gr.Column(elem_id="main-content"):
            hero = gr.HTML(
                value=HERO_HTML,
                visible=True,
                elem_id="hero",
            )

            with gr.Column(
                visible=False,
                elem_id="chat-area",
            ) as chat_area:
                chatbot = gr.Chatbot(
                    value=[],
                    label="",
                    height=560,
                    elem_id="chatbot",
                )

            with gr.Row(elem_id="composer"):
                message = gr.Textbox(
                    label="",
                    placeholder="Posez votre question…",
                    lines=2,
                    container=False,
                    elem_id="message-input",
                )

                send_button = gr.Button(
                    "↑",
                    variant="primary",
                    elem_id="send",
                )

            status = gr.Markdown(
                "🔒 Traitement 100 % local et privé",
                elem_id="status",
            )

        menu_button.click(
            fn=toggle_menu,
            inputs=menu_state,
            outputs=[
                menu_state,
                sidebar,
            ],
            show_progress="hidden",
        )

        send_inputs = [
            message,
            chatbot,
            conversation_state,
            model_selector,
        ]

        send_outputs = [
            message,
            chatbot,
            conversation_state,
            hero,
            chat_area,
            status,
        ]

        send_button.click(
            fn=send_message,
            inputs=send_inputs,
            outputs=send_outputs,
            show_progress="full",
        )

        message.submit(
            fn=send_message,
            inputs=send_inputs,
            outputs=send_outputs,
            show_progress="full",
        )

        new_button.click(
            fn=create_new_chat,
            outputs=[
                chatbot,
                conversation_state,
                conversation_list,
                hero,
                chat_area,
                status,
            ],
        )

        conversation_list.change(
            fn=open_saved_chat,
            inputs=conversation_list,
            outputs=[
                chatbot,
                conversation_state,
                hero,
                chat_area,
                status,
            ],
        )

        refresh_button.click(
            fn=refresh_history,
            outputs=conversation_list,
        )

        delete_button.click(
            fn=remove_chat,
            inputs=conversation_state,
            outputs=[
                chatbot,
                conversation_state,
                conversation_list,
                hero,
                chat_area,
                status,
            ],
        )

        model_selector.change(
            fn=change_model,
            inputs=model_selector,
            outputs=model_status,
        )

        dark_button.click(
            fn=None,
            js=DARK_THEME_JS,
        )

        light_button.click(
            fn=None,
            js=LIGHT_THEME_JS,
        )

        demo.load(
            fn=None,
            js=LOAD_THEME_JS,
        )

    return demo


def launch_interface() -> None:
    demo = build_interface()

    demo.queue().launch(
        server_name="127.0.0.1",
        server_port=7860,
        inbrowser=True,
        theme=gr.themes.Base(),
        css=CUSTOM_CSS,
        footer_links=[],
    )
