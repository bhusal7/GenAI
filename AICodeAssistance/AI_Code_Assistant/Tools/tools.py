from __future__ import annotations

import datetime
from pathlib import Path

from langchain.tools import tool

from config import mistral_llm

_retriever = None


def set_retriever(retriever) -> None:
    """
    Store retriever globally so tools can use it.
    """
    global _retriever
    _retriever = retriever


def _require_retriever():
    if _retriever is None:
        raise ValueError(
            "Retriever is not initialized. Call set_retriever(retriever) in pipeline.py first."
        )
    return _retriever


def _retrieve_text(query: str, k: int = 4) -> str:
    retriever = _require_retriever()
    docs = retriever.invoke(query)

    if not docs:
        return "No relevant code found."

    parts = []
    for i, doc in enumerate(docs[:k], start=1):
        source = doc.metadata.get("source", "unknown")
        parts.append(
            f"[Chunk {i}] Source: {source}\n{doc.page_content}"
        )

    return "\n\n".join(parts)


def _llm_response(system_task: str, query: str) -> str:
    context = _retrieve_text(query)

    prompt = f"""
You are an expert AI Code Assistant.

Task: {system_task}

User query:
{query}

Relevant code context:
{context}

Give a clear, useful, and concise answer.
"""

    response = mistral_llm.invoke(prompt)
    return response.content if hasattr(response, "content") else str(response)


@tool
def read_code(query: str) -> str:
    """Read relevant source code from the project."""
    return _retrieve_text(query)


@tool
def analyze_code(query: str) -> str:
    """Explain what the code does."""
    return _llm_response("Explain the code", query)


@tool
def find_bugs(query: str) -> str:
    """Find possible bugs or issues in the code."""
    return _llm_response("Detect bugs, errors, and risky patterns", query)


@tool
def optimize_code(query: str) -> str:
    """Suggest performance and code-quality improvements."""
    return _llm_response("Suggest optimization improvements", query)


@tool
def refactor_code(query: str) -> str:
    """Suggest cleaner and better structured code."""
    return _llm_response("Refactor the code for readability and maintainability", query)


@tool
def generate_docs(query: str) -> str:
    """Generate documentation for the code."""
    return _llm_response("Generate documentation for the code", query)


@tool
def save_report(content: str, filename: str = "dataset_report") -> str:
    """Save report into reports folder."""
    reports_dir = Path("reports")
    reports_dir.mkdir(exist_ok=True)

    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    filepath = reports_dir / f"{filename}_{timestamp}.md"

    filepath.write_text(content, encoding="utf-8")

    return f"Report saved successfully: {filepath}"