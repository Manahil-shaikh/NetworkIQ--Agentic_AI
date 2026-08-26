from langchain_ollama import ChatOllama

from networkiq.config import OLLAMA_MODEL


def create_llm() -> ChatOllama:
    """Create the local Ollama chat model."""

    return ChatOllama(
        model=OLLAMA_MODEL,
        temperature=0,
    )