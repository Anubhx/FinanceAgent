import os
from typing import TypedDict, Annotated
from langgraph.graph import StateGraph, END
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage, AIMessage
from agent.memory import get_memories, save_memory
from agent.tools import (
    get_spending_summary,
    detect_anomalies,
    generate_savings_plan,
    answer_finance_question,
)

# ── State Schema ──────────────────────────────────────────────────────────────

class AgentState(TypedDict):
    user_id: str
    user_message: str
    memory_context: str
    tool_results: list[str]
    final_response: str

# ── LLM ───────────────────────────────────────────────────────────────────────
def get_gemini_llm(api_key_env: str = "GEMINI_API_KEY") -> ChatGoogleGenerativeAI:
    api_key = os.getenv(api_key_env)
    if not api_key:
        raise ValueError(f"Missing environment variable: {api_key_env}")

    return ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",
        google_api_key=api_key,
        max_tokens=1024,
        temperature=0.3,
    )
tools = [get_spending_summary, detect_anomalies, generate_savings_plan, answer_finance_question]

# ── Nodes ──────────────────────────────────────────────────────────────────────

def fetch_memory_node(state: AgentState) -> AgentState:
    """Retrieve relevant memories for the current query."""
    memories = get_memories(state["user_id"], state["user_message"])
    return {**state, "memory_context": memories}

def plan_and_execute_node(state: AgentState) -> AgentState:
    """
    Use Gemini to decide which tools to call, then execute them.
    This is a simple ReAct-style single-pass planner.
    """
    llm = get_llm()
    if not llm.google_api_key:
        return {**state, "tool_results": ["Error: GEMINI_API_KEY_1 is missing."]}
        
    llm_with_tools = llm.bind_tools(tools)
    
    system_prompt = f"""You are a personal finance assistant with memory of past conversations.
You have access to the user's real bank transaction data.
Use the tools to fetch real data before answering.

User's memory context (from past conversations):
{state['memory_context']}

Always call at least one tool to ground your response in actual data.
After getting tool results, give a clear, warm, and actionable response.
"""
    messages = [
        HumanMessage(content=system_prompt + "\n\nUser: " + state["user_message"])
    ]
    
    tool_results = []
    try:
        response = llm_with_tools.invoke(messages)
        
        # Execute tool calls
        if hasattr(response, "tool_calls") and response.tool_calls:
            for tool_call in response.tool_calls:
                tool_name = tool_call["name"]
                tool_args = tool_call["args"]
                tool_args["user_id"] = state["user_id"]  # Always inject user_id
                
                tool_fn = next((t for t in tools if t.name == tool_name), None)
                if tool_fn:
                    result = tool_fn.invoke(tool_args)
                    tool_results.append(f"[{tool_name}]: {result}")
    except Exception as e:
        tool_results.append(f"Tool execution error: {e}")
    
    return {**state, "tool_results": tool_results}

def synthesise_response_node(state: AgentState) -> AgentState:
    """Combine tool results into a final response using Gemini."""
    from agent.gemini_client import call_gemini
    
    tools_str = "\n\n".join(state["tool_results"]) if state["tool_results"] else "No tool data."
    
    prompt = f"""You are a warm, helpful personal finance assistant.
User asked: {state['user_message']}
What the user has told you before: {state['memory_context']}
Data from your analysis tools:
{tools_str}

Write a helpful, friendly response. Be specific. Use ₹ for amounts. Max 200 words.
Do not mention "tool results" or technical jargon. Just speak naturally.
"""
    response = call_gemini(prompt)
    return {**state, "final_response": response}

def save_memory_node(state: AgentState) -> AgentState:
    """Save the conversation turn to persistent memory."""
    content = f"User asked: {state['user_message']}. Assistant replied: {state['final_response']}"
    save_memory(state["user_id"], content)
    return state

# ── Graph ─────────────────────────────────────────────────────────────────────

def build_agent():
    graph = StateGraph(AgentState)
    
    graph.add_node("fetch_memory", fetch_memory_node)
    graph.add_node("plan_and_execute", plan_and_execute_node)
    graph.add_node("synthesise", synthesise_response_node)
    graph.add_node("save_memory", save_memory_node)
    
    graph.set_entry_point("fetch_memory")
    graph.add_edge("fetch_memory", "plan_and_execute")
    graph.add_edge("plan_and_execute", "synthesise")
    graph.add_edge("synthesise", "save_memory")
    graph.add_edge("save_memory", END)
    
    return graph.compile()

agent_graph = build_agent()

def run_agent(user_id: str, user_message: str) -> str:
    result = agent_graph.invoke({
        "user_id": user_id,
        "user_message": user_message,
        "memory_context": "",
        "tool_results": [],
        "final_response": "",
    })
    return result["final_response"]
