import json
import os

def get_file(username):
    return f"{username}_chat.json"

def load_chat(username):
    file = get_file(username)
    if not os.path.exists(file):
        return []
    with open(file, "r") as f:
        return json.load(f)

def save_chat(username, chat):
    file = get_file(username)
    with open(file, "w") as f:
        json.dump(chat, f)