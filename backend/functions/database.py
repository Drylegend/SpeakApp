import sqlite3
import random

def init_db():
    conn = sqlite3.connect('messages.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            role TEXT NOT NULL,
            content TEXT NOT NULL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

def get_recent_messages():
    # Define the system instruction for Speak AI
    system_prompt = {
        "role": "system",
        "content": (
            "You are Speak AI, a friendly and helpful voice assistant. "
            "If a user explicitly asks for your name (for example, 'What is your name?' or 'Tell me your name?'), "
            "respond with: 'I am Speak AI, your assistant here to help you.' "
            "Otherwise, do not mention your name in your responses. Keep your answers clear, personable, and under 50 words."
        )
    }
    # Optionally add a little variation
    if random.uniform(0, 1) < 0.5:
        system_prompt["content"] += " Add a touch of dry humor when appropriate."
    else:
        system_prompt["content"] += " Occasionally, include a challenging question to engage the user."
    
    messages = [system_prompt]
    
    # Retrieve the last 5 messages from the database (if any)
    conn = sqlite3.connect('messages.db')
    cursor = conn.cursor()
    cursor.execute("SELECT role, content FROM messages ORDER BY timestamp DESC LIMIT 5")
    rows = cursor.fetchall()
    conn.close()
    
    # Reverse the order to maintain conversation order and append to the prompt
    for row in rows[::-1]:
        messages.append({"role": row[0], "content": row[1]})
    return messages

def store_messages(user_message, assistant_message):
    conn = sqlite3.connect('messages.db')
    cursor = conn.cursor()
    # Save the user's message
    cursor.execute("INSERT INTO messages (role, content) VALUES (?, ?)", ("user", user_message))
    # Save the assistant's response
    cursor.execute("INSERT INTO messages (role, content) VALUES (?, ?)", ("assistant", assistant_message))
    conn.commit()
    conn.close()

def reset_messages():
    conn = sqlite3.connect('messages.db')
    cursor = conn.cursor()
    cursor.execute("DELETE FROM messages")
    conn.commit()
    conn.close()

# Initialize the database when this module is imported
init_db()
