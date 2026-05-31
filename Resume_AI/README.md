# Resume AI Chatbot

This project was inspired by an AI course project. I rebuilt it independently and modified the model integration, prompting strategy, and implementation details to better understand local LLM workflows and tool calling.

An intelligent resume chatbot powered by **Ollama ** with a **Gradio** web interface. The chatbot answers questions about your resume, intelligently handles unknown questions, and captures user interest with real-time Pushover notifications.

## Features

**AI-Powered Resume Q&A** - Answers questions about your experience, skills, and background based on your actual resume  
**Tool Calling** - Uses function calling to record user details and unknown questions  
**Real-Time Notifications** - Sends Pushover alerts when users express interest or ask unanswerable questions  
**Web Interface** - Easy-to-use Gradio chat interface  
**Local LLM** - Runs completely locally with Ollama (no API keys required for the LLM)  
**Conversation Context** - Maintains chat history for coherent multi-turn conversations  

## Tech Stack

- **LLM**: Ollama (qwen2.5:14b model)
- **Framework**: Gradio (web UI)
- **SDK**: OpenAI Python Client (configured for local Ollama)
- **PDF Processing**: PyPDF2
- **Notifications**: Pushover API
- **Runtime**: Python 3.10+

## Setup Instructions

### 1. Prerequisites

- **Ollama**: Download and install from [ollama.ai](https://ollama.ai)
- **Python 3.10+**: Required for the application
- **Pushover Account**: (Optional) For user interest notifications

### 2. Pull the Ollama Model

```bash
ollama pull qwen2.5:14b
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Create a `.env` file in the project directory:

```
PUSHOVER_TOKEN=your_pushover_app_token
PUSHOVER_KEY=your_pushover_user_key
```

**Note**: If you don't have Pushover, leave these blank or set dummy values (the app will still work, but notifications won't send).

### 5. Add Your Resume

Place your resume PDF at:
```
resume folder
```

You can modify the path in `app.py` line 84 if your resume has a different name/location.

## Running the Application

### Start Ollama (in a separate terminal)

```bash
ollama serve
```

### Run the App

```bash
python app.py
```

The Gradio interface will launch at `http://localhost:7860`

## How It Works

1. **User Asks a Question** → Sent to the LLM with your resume as context
2. **LLM Responds** → Generates an answer based on your resume
3. **Tool Calling** → If relevant, the LLM calls tools to:
   - Record user contact details (if they want to connect)
   - Log questions it couldn't answer
4. **Notifications** → Pushover alerts notify you of user interest or unanswerable questions
5. **Response Returned** → User sees the answer in the chat interface

## Project Structure

```
Resume_AI/
├── app.py                      # Main application
├── requirements.txt            # Python dependencies
├── README.md                   # This file
├── .env                        # Environment variables (create this)
└── resume/
    └── Resume_Achraf_EN.pdf   # Your resume PDF
```

## Key Components

### ResumeAgent Class
- **`__init__`**: Loads resume PDF and initializes the agent
- **`system_prompt()`**: Creates context-aware system prompt with resume text
- **`chat_with_user()`**: Main chat loop with tool calling logic
- **`handle_tools()`**: Executes tool calls from the LLM

### Tool Functions
- **`record_user_details()`**: Captures user name and email
- **`record_unknown_question()`**: Logs questions the LLM couldn't answer
- **`push_text_to_pushover()`**: Sends notifications via Pushover API

## Customization

### Change the Model
Edit line 15 in `app.py`:
```python
ollama_model = "mistral"  # or any other Ollama model
```

### Change the Resume File Path
Edit line 84 in `app.py`:
```python
self.reader = PdfReader("path/to/your/resume.pdf")
```

### Modify System Prompt
Edit the `system_prompt()` method in `app.py` to customize the assistant's behavior.

## Troubleshooting

### Error: "404 page not found"
- Ensure Ollama is running: `ollama serve`
- Check the URL is correct: `http://localhost:11434/v1`

### Error: "FileNotFoundError: resume/Resume_Achraf_EN.pdf"
- Ensure your resume PDF exists at the specified path
- Update the path in `app.py` if your file is in a different location

### Gradio won't launch
- Check that port 7860 is not already in use
- Run: `gr.ChatInterface(...).launch(share=False, server_name="0.0.0.0", server_port=7860)`

### No notifications are being sent
- Verify `PUSHOVER_TOKEN` and `PUSHOVER_KEY` are set in your `.env` file
- Check that Pushover credentials are valid


