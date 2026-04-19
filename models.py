import requests

def call_model(model, prompt):
    response = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": model,
            "prompt": prompt,
            "stream": False
        }
    )
    return response.json()["response"]

def planner_model(prompt):
    return call_model("deepseek-r1", prompt)

def executor_model(prompt):
    return call_model("mistral", prompt)

def critic_model(prompt):
    return call_model("llama3", prompt)

def chatbot_model(prompt):
    return call_model("qwen", prompt)