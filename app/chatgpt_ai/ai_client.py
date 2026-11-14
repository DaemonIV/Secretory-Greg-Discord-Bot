from dotenv import load_dotenv
import discord
import os
from openai import OpenAI

load_dotenv()

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv('OPENROUTER_API_KEY'),
)

current_dir = os.path.dirname(__file__)


with open(os.path.join(current_dir, 'instructions.txt'), 'r', encoding='utf-8') as f:
    system_instructions = f.read()

with open(os.path.join(current_dir, 'info.txt'), 'r', encoding='utf-8') as f:
    server_info = f.read()

def chatgpt_response(prompt):
    try:
        completion = client.chat.completions.create(
            model="openrouter/free",
            messages=[
                
                {
                    "role": "system", 
                    "content": system_instructions
                },
                                {
                    "role": "user",
                    "content": f"Here is the server info documentation:\n{server_info}\n\nPlayer's question: {prompt}"
                }
            ]
        )
        
        return completion.choices[0].message.content
        return c
    except Exception as e:
        print(f"Error: {e}")
        return "Sorry, I ran into an error generating a response."
