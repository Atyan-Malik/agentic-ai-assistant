
import requests
import streamlit as st

from utils.errors import get_error_message


# ============================================================
# Configuration
# ============================================================

API_BASE_URL = "http://127.0.0.1:8000"
REQUEST_TIMEOUT = 300


# ============================================================
# Streamlit Configuration
# ============================================================

st.set_page_config(
    page_title="Agentic AI Assistant",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ============================================================
# Session State
# ============================================================

if "messages" not in st.session_state:
    st.session_state.messages = []

if "session_id" not in st.session_state:
    st.session_state.session_id = None


# ============================================================
# Sidebar
# ============================================================

with st.sidebar:
    st.title("🤖 Agentic AI")
    st.caption("Local AI Assistant")

    st.divider()

    if st.button(
        "➕ New Conversation",
        use_container_width=True,
    ):
        st.session_state.messages = []
        st.session_state.session_id = None
        st.rerun()

    st.divider()

    st.subheader("Backend")

    try:
        response = requests.get(
            f"{API_BASE_URL}/health",
            timeout=5,
        )

        if response.ok:
            st.success("Backend Online")
        else:
            st.warning("Backend Responding")

    except requests.RequestException as error:
        st.error(get_error_message(error))

    st.divider()

    st.subheader("Configuration")
    st.caption("LLM: Qwen2.5")
    st.caption("Runtime: Ollama")
    st.caption("Agent: Tool-enabled")


# ============================================================
# Main Page
# ============================================================

st.title("🤖 Agentic AI Assistant")

st.caption(
    "Ask general questions or request tasks that require "
    "your agent's registered tools."
)

st.divider()


# ============================================================
# Chat History
# ============================================================

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])


# ============================================================
# Chat Input
# ============================================================

prompt = st.chat_input(
    "Ask the AI assistant anything..."
)


if prompt:
    # --------------------------------------------------------
    # Display and save user message
    # --------------------------------------------------------

    st.session_state.messages.append({
        "role": "user",
        "content": prompt,
    })

    with st.chat_message("user"):
        st.markdown(prompt)

    # --------------------------------------------------------
    # Call FastAPI Agent
    # --------------------------------------------------------

    with st.chat_message("assistant"):
        with st.spinner("Agent is thinking..."):
            try:
                response = requests.post(
                    f"{API_BASE_URL}/agent/run",
                    json={
                        "message": prompt,
                        "session_id": st.session_state.session_id,
                    },
                    timeout=REQUEST_TIMEOUT,
                )

                if not response.ok:
                    answer = get_error_message(
                        Exception("Agent API request failed"),
                        response=response,
                    )

                    answer = (
                        f"**Agent error ({response.status_code}):** "
                        f"{answer}"
                    )

                else:
                    data = response.json()

                    # Preserve the agent's conversation session.
                    if data.get("session_id"):
                        st.session_state.session_id = (
                            data["session_id"]
                        )

                    answer = (
                        data.get("response")
                        or data.get("message")
                        or data.get("answer")
                        or "The agent returned no response."
                    )

            except requests.RequestException as error:
                answer = get_error_message(error)

            except Exception as error:
                answer = get_error_message(error)

            st.markdown(answer)

    # --------------------------------------------------------
    # Save Assistant Response
    # --------------------------------------------------------

    st.session_state.messages.append({
        "role": "assistant",
        "content": answer,
    })
