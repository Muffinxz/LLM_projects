from urllib import response

from openai import OpenAI
import os
import json
import requests
from PyPDF2 import PdfReader
import gradio as gr
from dotenv import load_dotenv

load_dotenv(override=True)


ollama_url = "http://localhost:11434/v1"
ollama_model = "qwen2.5:14b"

ollama = OpenAI(base_url=ollama_url, api_key="ollama")



def push_text_to_pushover(text):
    url = "https://api.pushover.net/1/messages.json"
    data = {
        "token": os.getenv("PUSHOVER_TOKEN"),
        "user": os.getenv("PUSHOVER_KEY"),
        "message": text
    }
    requests.post(url, data=data)

def record_user_details(name ="Name not provided", email ="not provided"):
    push_text_to_pushover(f"User details recorded: Name - {name}, Email - {email}")
    return {"status": "success", "message": "User details recorded and sent to Pushover."}

def record_unknown_question(question):
    push_text_to_pushover(f"Unknown question received: {question}")
    return {"status": "success", "message": "Unknown question recorded and sent to Pushover."}


record_user_details_json = {
    "name": "record_user_details",
    "description": "Use this tool to record that a user is interested in being in touch and provided an email address",
    "parameters": {
        "type": "object",
        "properties": {
            "email": {
                "type": "string",
                "description": "The email address of this user"
            },
            "name": {
                "type": "string",
                "description": "The user's name, if they provided it"
            }
        },
        "required": ["email"],
        "additionalProperties": False
    }
}

record_unknown_question_json = {
    "name": "record_unknown_question",
    "description": "Always use this tool to record any question that couldn't be answered as you didn't know the answer",
    "parameters": {
        "type": "object",
        "properties": {
            "question": {
                "type": "string",
                "description": "The question that couldn't be answered"
            },
        },
        "required": ["question"],
        "additionalProperties": False
    }
}


tools = [{'type': 'function', 'function': record_user_details_json}, {'type': 'function', 'function': record_unknown_question_json}]

class ResumeAgent:
    def __init__(self, tools):
        self.tools = tools
        self.name="Achraf Chakroun"
        self.resume= ""
        try:
            reader = PdfReader("resume/Resume_Achraf_EN.pdf")
            for page in reader.pages:
                text = page.extract_text()
                if text:
                    self.resume += text
        except FileNotFoundError:
            print("Error: resume/Resume_Achraf_EN.pdf not found!")
            self.resume = "Resume file not found."
        except Exception as e:
            print(f"Error reading resume: {e}")
            self.resume = f"Error reading resume: {e}"
    
    def handle_tools(self, tool_calls):
        result = []
        # Add the assistant message with tool_calls
        result.append({'role': 'assistant', 'tool_calls': tool_calls})
        
        # Add tool results
        for call in tool_calls:
            tool_name = call.function.name
            tool_args = json.loads(call.function.arguments)
            tool_result = None
            if tool_name == "record_user_details":
                tool_result = record_user_details(**tool_args)
            elif tool_name == "record_unknown_question":
                tool_result = record_unknown_question(**tool_args)
            
            result.append({'role': 'tool', 'content': json.dumps(tool_result), 'tool_call_id': call.id})
        return result

    def system_prompt(self):
        system_prompt = f"""
You are a career communication assistant helping {self.name} answer recruiters.

You have access to his resume and professional summary. Use them only as factual evidence.
Do not copy resume bullets directly. Rewrite ideas in a natural, conversational way.

The answer should sound like {self.name} speaking to a recruiter:
- clear
- confident
- professional
- specific
- not robotic
- not exaggerated

Rules:
- Use first person: "I worked on...", "My experience includes..."
- Reference concrete projects, tools, or results when relevant.
- Explain the value of the experience, not just the task.
- Do not invent facts.
- Do not list bullet points unless the recruiter explicitly asks for a list.
- If the question is about a job, connect the answer to that job.
**Important:
-There resume you are following is : {self.resume}
If you don't know the answer to any question, use your record_unknown_question tool to record the question that you couldn't answer, even if it's about something trivial or unrelated to career. \
If the user is engaging in discussion, try to steer them towards getting in touch via email; ask for their email and record it using your record_user_details tool. 


Write a natural answer in first person.
Avoid copying bullet points from the resume.
Use specific evidence from the resume.
Keep the answer between 120 and 180 words.
"""
        return system_prompt
    
    def chat_with_user(self, message, history):
        messages = [{'role': 'system', 'content': self.system_prompt()}] + history + [{'role': 'user', 'content': message}]
        done = False
        while not done:
            response = ollama.chat.completions.create(model=ollama_model, messages=messages, tools=self.tools, tool_choice="auto", max_tokens=1000)
            tool_calls = response.choices[0].message.tool_calls
            if response.choices[0].finish_reason == "tool_calls" and tool_calls:
                tool_results = self.handle_tools(tool_calls)
                messages.extend(tool_results)
                follow_up_response = ollama.chat.completions.create(model=ollama_model, messages=messages, tools=self.tools, tool_choice="none", max_tokens=1000)
                return follow_up_response.choices[0].message.content
            else:
               done = True
        return response.choices[0].message.content


if __name__ == "__main__":
    agent = ResumeAgent(tools)
    gr.ChatInterface(agent.chat_with_user, type="messages").launch()
