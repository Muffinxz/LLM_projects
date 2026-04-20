# Multi Model GUI

A simple Gradio-based interface for testing a local Ollama model inside a notebook environment.

This project connects a local LLM served with **Ollama** to a lightweight **Gradio** UI, making it easy to send prompts and view streaming responses directly from a notebook.

## Overview

The notebook launches a small interactive app where a user can enter text and receive a model-generated response. It is currently configured to use a **local `llama3.2` model through Ollama**.

Although the interface looks like a general chatbot, the current system prompt is designed for **customer support triage**. As a result, the most relevant use case at the moment is analyzing customer-style messages and producing structured support-oriented answers.

## Features

- Local LLM inference using **Ollama**
- Simple **Gradio** interface for interaction
- Streaming responses in the notebook UI
- Configurable system prompt
- Easy to adapt for other prompt-engineering experiments

## Requirements

Before running the notebook, make sure you have:

- **Python 3.10+**
- **Ollama installed and running**
- A local Ollama model available, such as **`llama3.2`**
- The required Python packages installed

Install dependencies with:

```bash
pip install gradio openai requests
