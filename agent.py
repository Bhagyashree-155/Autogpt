import os
import requests
from groq import Groq
from memory import add_memory, search_memory

GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
SERP_API_KEY = os.getenv("SERP_API_KEY", "")

# 🚫 Do NOT crash app if keys missing (important for deployment)
client = Groq(api_key=GROQ_API_KEY) if GROQ_API_KEY else None


# 🔎 SEARCH
def search_web(query):
    if not SERP_API_KEY:
        return ""

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


# 🤖 MODEL
def call_llm(prompt):
    if client:
        try:
            response = client.chat.completions.create(
                model="llama-3.1-8b-instant",
                messages=[{"role": "user", "content": prompt}]
            )
            return response.choices[0].message.content
        except:
            pass

    return "AI service not available right now."


# 🚀 MAIN AGENT
def autogpt(query, chat_history):
    try:
        history_text = "\n".join([f"{r}: {m}" for r, m in chat_history[-5:]])
        memory = "\n".join(search_memory(query))
        search_result = search_web(query)

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

        add_memory(f"Q: {query} → A: {answer}")

        return answer

    except Exception as e:
        return f"Error: {str(e)}"