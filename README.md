---
title: AgenticRAG
emoji: 🌖
colorFrom: pink
colorTo: pink
sdk: gradio
sdk_version: 5.29.1
app_file: app.py
pinned: false
license: apache-2.0
---

Check out the chatbot at - https://huggingface.co/spaces/Situm/agenticrag-chatbot

🤖 AgenticRAG Chatbot
A Python-based intelligent chatbot built with Gradio UI and SmolAgents, capable of answering user queries using agentic reasoning, retrieval-augmented generation (RAG), and tool integrations.

🚀 Features
🧠 Agentic Reasoning: Powered by SmolAgents and CodeAgent
🔎 Web Search: DuckDuckGo integration for real-time results
🌦️ Weather Tool: Real-time weather using OpenWeather App API
📊 Hub Stats Tool: Retrieve popular models from Hugging Face Hub
👤 Guest Info Tool: BM25 keyword-based search over custom dataset
🖥️ Gradio UI: Interactive web interface to test and chat with the agent

📁 Project Structure
AgenticRAG/
├── app.py                # Gradio UI launcher
├── tools.py              # Custom tools like weather, hub stats, search
├── retriever.py          # GuestInfoRetrieverTool using BM25
├── requirements.txt      # All dependencies
├── README.md             # You are here
└── .gitignore            # Python, PyCharm, and venv exclusions

If you are cloning this to your local machine then, you need to create your HF_API_TOKEN (Hugging Face Token) and OPENWEATHER_API_KEY (Open Weather API Key) at https://huggingface.co/settings/tokens and https://openweathermap.org/api.


