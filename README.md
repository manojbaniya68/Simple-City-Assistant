# City Assistant

A command-line city assistant that can look up current weather and recent city news. It uses a Gemini model and asks for your approval before each tool call.

## Setup

Install the required packages:

```bash
pip install python-dotenv langchain langchain-google-genai langchain-tavily rich requests
```

Create a `.env` file in the project directory and add the API keys:

```env
GOOGLE_API_KEY=your_google_api_key
TAVILY_API_KEY=your_tavily_api_key
OPENWEATHER_API_KEY=your_openweather_api_key
```

## Run

```bash
python app.py
```

Enter a request for a city's weather or recent news. Approve tool calls by typing `yes` when prompted. Enter `exit` to quit.
