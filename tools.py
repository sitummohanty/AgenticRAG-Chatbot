# Import the DuckDuckGo search tool and base Tool class from smolagents
from smolagents import DuckDuckGoSearchTool, Tool

# Standard library import for generating random values
import random

# Hugging Face Hub utility for listing models
from huggingface_hub import list_models

import os

from dotenv import load_dotenv

import requests

# -------------------------------------
# DuckDuckGo Search Tool Initialization
# -------------------------------------

# This tool enables the agent to perform web searches using DuckDuckGo
search_tool = DuckDuckGoSearchTool()


# -------------------------------------
# Dummy Weather Information Tool
# -------------------------------------

load_dotenv()
API_KEY = os.getenv("OPENWEATHER_API_KEY")

class WeatherInfoTool(Tool):
    """
    A tool that fetches real-time weather information for a given location using OpenWeatherMap API.
    """

    name = "weather_info"
    description = "Fetches real weather information for a given location using OpenWeatherMap."

    # Define expected input parameters
    inputs = {
        "location": {
            "type": "string",
            "description": "The location (city name) to get weather information for."
        }
    }

    # Define the output type
    output_type = "string"

    def forward(self, location: str):
        """
        Fetches weather data for a specified location using the OpenWeatherMap API.
        """
        if not API_KEY:
            return "Weather API key is missing. Please set OPENWEATHER_API_KEY in your environment."

        try:
            url = (
                f"https://api.openweathermap.org/data/2.5/weather?q={location}"
                f"&appid={API_KEY}&units=metric"
            )
            response = requests.get(url)
            data = response.json()

            if response.status_code != 200:
                return f"Failed to fetch weather: {data.get('message', 'Unknown error')}"

            weather = data["weather"][0]["description"].title()
            temp = data["main"]["temp"]
            humidity = data["main"]["humidity"]
            wind_speed = data["wind"]["speed"]

            return (
                f"Weather in {location.title()}:\n"
                f"- Condition: {weather}\n"
                f"- Temperature: {temp}°C\n"
                f"- Humidity: {humidity}%\n"
                f"- Wind Speed: {wind_speed} m/s"
            )

        except Exception as e:
            return f"Error retrieving weather data: {str(e)}"


# -------------------------------------
# Hugging Face Hub Stats Tool
# -------------------------------------

class HubStatsTool(Tool):
	"""
    A custom tool that fetches information about the most downloaded model
    by a given author or organization on Hugging Face Hub.
    """

	name = "hub_stats"
	description = "Fetches the most downloaded model from a specific author on the Hugging Face Hub."

	# Define expected input parameters
	inputs = {
		"author": {
			"type": "string",
			"description": "The username of the model author/organization to find models from."
		}
	}

	# Define the output type
	output_type = "string"

	def forward(self, author: str):
		"""
        Queries Hugging Face Hub for the author's most downloaded model.
        Returns the model ID and download count.
        """
		try:
			# List models by the given author, sorted by downloads (descending)
			models = list(
				list_models(author=author, sort="downloads", direction=-1, limit=1)
			)

			if models:
				# Extract the top model and format its stats
				model = models[0]
				return f"The most downloaded model by {author} is {model.id} with {model.downloads:,} downloads."
			else:
				return f"No models found for author {author}."

		except Exception as e:
			# Return a friendly error message on failure
			return f"Error fetching models for {author}: {str(e)}"
