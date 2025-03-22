import os
from dotenv import load_dotenv
import google.generativeai as genai

# Import database functions (which include our system prompt)
from functions.database import get_recent_messages, store_messages, reset_messages

# Load environment variables and configure Gemini API key
load_dotenv()
gemini_api_key = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=gemini_api_key)

def get_chat_response(message_input):
    try:
        # Instantiate the Gemini model
        model = genai.GenerativeModel('gemini-1.5-pro-latest')
        
        # Get recent messages which includes our system prompt and conversation history
        messages = get_recent_messages()
        # Append the current user message
        user_message = {"role": "user", "content": message_input}
        messages.append(user_message)
        
        # Combine the messages into one prompt string
        combined_prompt = "\n".join([f"{msg['role']}: {msg['content']}" for msg in messages])
        
        # Generate the assistant's response using Gemini
        response = model.generate_content(
            combined_prompt, 
            generation_config=genai.GenerationConfig(max_output_tokens=1000, temperature=0.7)
        )
        
        if response and hasattr(response, 'candidates') and len(response.candidates) > 0:
            gemini_response = response.candidates[0].content.parts[0].text.strip()
            # Save the conversation into the database
            store_messages(message_input, gemini_response)
            return gemini_response
        else:
            return "Failed to get response from Gemini"
    except Exception as e:
        print("Failed to get response from Gemini:", e)
        return "Failed to get response from Gemini"
