

import os
import requests
from groq import Groq
from memory import add_memory, search_memory


GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
SERP_API_KEY = os.getenv("SERP_API_KEY", "")

if not GROQ_API_KEY or not SERP_API_KEY:
    raise ValueError(
        "Missing API keys. Set GROQ_API_KEY and SERP_API_KEY in your environment."
    )

client = Groq(api_key=GROQ_API_KEY)

# 🔎 SEARCH
def search_web(query):
    try:
        url = "https://serpapi.com/search.json"
        params = {"q": query, "api_key": SERP_API_KEY, "engine": "google"}
        res = requests.get(url, params=params).json()

        snippets = []
        for r in res.get("organic_results", [])[:3]:
            snippets.append(r.get("snippet", ""))

        return " ".join(snippets)
    except:
        return ""

# 🤖 MODEL + FALLBACK
def call_llm(prompt):

    try:
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content
    except:
        pass

    # fallback
    try:
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={"model": "llama3:8b", "prompt": prompt, "stream": False}
        )
        return response.json().get("response", "")
    except:
        return "All systems failed."

# 🚀 MAIN AGENT
def autogpt(query, chat_history):

    # 🔎 Get memory
    memory = "\n".join(search_memory(query))

    # 🔎 Search
    search_result = search_web(query)

    # 📜 Chat history
    history_text = "\n".join([f"{r}: {m}" for r, m in chat_history[-3:]])

    prompt = f"""
You are an intelligent assistant.

Chat History:
{history_text}

Memory:
{memory}

Web Data:
{search_result}

Question: {query}

Give accurate and contextual answer.
"""

    answer = call_llm(prompt)

    # Save memory
    add_memory(f"Q: {query} → A: {answer}")

    return answer