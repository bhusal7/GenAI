from langchain.agents import create_agent
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from config import mistral_llm, groq_llm
from Tools.tools import (read_code,analyze_code,find_bugs,optimize_code,refactor_code,generate_docs,save_report,)

parser = StrOutputParser()


USER_SYSTEM_PROMPT = """
You are the User Agent of an AI Code Assistant.

Your responsibilities:
- Understand the user's request.
- Decide which tool should be used.
- Ask for clarification only if absolutely necessary.
- Give short and clear responses.
"""

RESEARCH_SYSTEM_PROMPT = """
You are the Code Research Agent.

Responsibilities:
- Understand the entire codebase.
- Explain the architecture.
- Identify relationships between files.
- Analyze code flow.
- Never make assumptions.
"""

BUG_SYSTEM_PROMPT = """
You are the Bug Detection Agent.

Responsibilities:
- Detect syntax errors.
- Detect logical errors.
- Detect runtime issues.
- Detect security vulnerabilities.
- Explain every bug clearly.
- Suggest fixes.
"""

OPTIMIZATION_SYSTEM_PROMPT = """
You are the Optimization Agent.

Responsibilities:
- Improve code performance.
- Improve readability.
- Improve maintainability.
- Remove duplicate code.
- Suggest best practices.
"""

DOCUMENTATION_SYSTEM_PROMPT = """
You are the Documentation Agent.

Responsibilities:
- Generate documentation.
- Generate docstrings.
- Explain classes.
- Explain functions.
- Explain modules.
- Produce clean Markdown documentation.
"""

EXPLAIN_SYSTEM_PROMPT = """
You are the Explain Code Agent.

Responsibilities:
- Explain code line by line.
- Explain functions.
- Explain algorithms.
- Explain logic.
- Use beginner-friendly language.
"""

CRITIC_SYSTEM_PROMPT = """
You are the Critic Agent.

Responsibilities:
- Review the final response.
- Find mistakes.
- Improve clarity.
- Verify correctness.
- Produce the best final answer.
"""


bug_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            BUG_SYSTEM_PROMPT,
        ),
        (
            "human",
            """
Question:
{query}

Relevant Code:
{context}

Find every possible bug.
Explain each bug.
Suggest fixes.
""",
        ),
    ]
)

documentation_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            DOCUMENTATION_SYSTEM_PROMPT,
        ),
        (
            "human",
            """
Question:
{query}

Relevant Code:
{context}

Generate complete documentation.
""",
        ),
    ]
)

optimization_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            OPTIMIZATION_SYSTEM_PROMPT,
        ),
        (
            "human",
            """
Question:
{query}

Relevant Code:
{context}

Suggest optimization improvements.
""",
        ),
    ]
)

explain_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            EXPLAIN_SYSTEM_PROMPT,
        ),
        (
            "human",
            """
Question:
{query}

Relevant Code:
{context}

Explain the code clearly.
""",
        ),
    ]
)

critic_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            CRITIC_SYSTEM_PROMPT,
        ),
        (
            "human",
            """
Draft Answer:
{draft}

Review it.

Improve it if necessary.

Return the final improved answer.
""",
        ),
    ]
)

bug_chain = bug_prompt|mistral_llm|parser
documentation_chain = documentation_prompt|groq_llm|parser
optimization_chain = optimization_prompt|mistral_llm|parser
explain_chain = explain_prompt|groq_llm|parser
critic_chain = critic_prompt|mistral_llm|parser


def user_agent():
    return create_agent(
        model=mistral_llm,
        tools = [read_code,analyze_code],
        system_prompt=USER_SYSTEM_PROMPT
    )
    
def research_agent():
    return create_agent(
        model=groq_llm,
        tools = [read_code,analyze_code],
        system_prompt=RESEARCH_SYSTEM_PROMPT
    )
    
def bug_agent():
    return create_agent(
        model=groq_llm,
        tools = [read_code,find_bugs],
        system_prompt=BUG_SYSTEM_PROMPT
    )
    
def optimization_agent():
    return create_agent(
        model=mistral_llm,
        tools = [read_code,optimize_code,refactor_code],
        system_prompt=OPTIMIZATION_SYSTEM_PROMPT
    )
    
def documentation_agent():
    return create_agent(
        model=groq_llm,
        tools = [read_code,generate_docs],
        system_prompt=DOCUMENTATION_SYSTEM_PROMPT
    )
    
def explain_agent():
    return create_agent(
        model=mistral_llm,
        tools = [read_code,analyze_code],
        system_prompt=EXPLAIN_SYSTEM_PROMPT
    )
    
def critic_agent():
    return create_agent(
        model=groq_llm,
        tools = [read_code,analyze_code,find_bugs,optimize_code,refactor_code,generate_docs,save_report],
        system_prompt=CRITIC_SYSTEM_PROMPT
    )
