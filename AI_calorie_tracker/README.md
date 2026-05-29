## Full Project Description

AI Calorie Tracker is a proof-of-concept Python project that combines image understanding and language model prompting to estimate calories and nutritional information from food photos.

The prototype uses a local Ollama llama3.2-vision model to process uploaded images and generate nutrition analysis. It includes image preprocessing with PIL, conversion to base64 for API submission, and a structured prompt design that guides the model to act as a nutrition analyst. The notebook also features a lightweight Gradio interface for interactive image upload, prompt editing, and real-time response display.

## Key features

Upload food images and inspect image metadata
Encode images as base64 for multimodal model requests
Send image + prompt payloads to Ollama via openai.OpenAI
Receive calorie estimates and nutritional recommendations
Interactive web UI built with Gradio for easy testing

## Why it matters

This project demonstrates how to build a practical multimodal AI workflow in a notebook environment, integrating vision and language capabilities for a real-world task. It is useful for exploring rapid prototyping of computer vision + LLM systems, especially in nutrition tracking or food analysis applications.