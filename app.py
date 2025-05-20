# Standard libraries
import os
import random

# UI library for creating the frontend
import gradio as gr

# Core SmolAgents components for UI, agent behavior, and Hugging Face model
from smolagents import GradioUI, CodeAgent, HfApiModel

# Custom tools used by the agent
from tools import DuckDuckGoSearchTool, WeatherInfoTool, HubStatsTool
from retriever import load_guest_dataset

# Environment and authentication handling
from huggingface_hub import login
from dotenv import load_dotenv

# ------------------------
# Authentication Setup
# ------------------------

# Load environment variables from a .env file (e.g., HF_API_TOKEN)
load_dotenv()

# Log into Hugging Face using the API token from the environment
login(token=os.getenv("HF_API_TOKEN"))

# -----------------------------
# Tool and Model Initialization
# -----------------------------

# Initialize the Hugging Face language model wrapper (LLM API interface)
model = HfApiModel()

# Initialize the external tool for web searching using DuckDuckGo
search_tool = DuckDuckGoSearchTool()

# Initialize the tool to get current weather information
weather_info_tool = WeatherInfoTool()

# Initialize the tool to retrieve stats from the Hugging Face Hub
hub_stats_tool = HubStatsTool()

# Load and prepare the guest info retrieval tool (based on dataset)
guest_info_tool = load_guest_dataset()

# ------------------------
# Agent Definition
# ------------------------

# Create an AI agent (named Alfred) that can use all the tools
alfred = CodeAgent(
    tools=[
        guest_info_tool,       # Guest information retrieval
        weather_info_tool,     # Weather details
        hub_stats_tool,        # Hugging Face Hub statistics
        search_tool            # General web search
    ],
    model=model,               # Assign the LLM model to the agent
    add_base_tools=True,       # Include built-in tools like code execution or calculator
    planning_interval=3        # Agent re-evaluates its plan every 3 steps
)

# ------------------------
# Launch Gradio Interface
# ------------------------

# Run the interactive Gradio UI only if this script is executed directly
if __name__ == "__main__":
    GradioUI(alfred).launch()