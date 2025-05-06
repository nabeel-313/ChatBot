import os
import re
import requests
from langchain.utilities import SerpAPIWrapper
from langchain.tools import Tool, tool
from dotenv import load_dotenv, find_dotenv


load_dotenv(find_dotenv())
def get_api_key(api_key_name):
    return os.getenv(api_key_name)

@tool
def google_search_tool(query:str):
    '''
    Useful for answering questions by searching Google.
    '''
    search = SerpAPIWrapper(serpapi_api_key=get_api_key("SERPAPI_API_KEY"))
    return search.run(query)


@tool
def weather_info_tool(location:str):
    '''
    Useful for gettnig the temperature and other weather realted information 
    '''
    base_url = "https://api.openweathermap.org/data/2.5/weather"
    params = {
        "q": location,
        "appid": get_api_key("OPENWEATHERMAP_API_KEY"),
        "units": "metric"  # for temperature in Celsius
    }
    response = requests.get(base_url, params=params)
    
    if response.status_code != 200:
        return f"Error fetching weather: {response.text}"
    
    data = response.json()
    temp = data["main"]["temp"]
    description = data["weather"][0]["description"]
    return f"The weather in {location} is {description} with a temperature of {temp}°C."


@tool
def convert_c_to_f(temp_input: str) -> str:
    """
    Converts a temperature from Celsius to Fahrenheit.
    Input should be a string that includes the Celsius value (e.g., '15', '15°C', or full sentence).
    """
    # Extract the first number from the input string
    match = re.search(r'-?\d+(\.\d+)?', temp_input)
    if not match:
        return "Could not find a valid Celsius temperature in the input."
    
    temp_celsius = float(match.group())
    temp_fahrenheit = (temp_celsius * 9/5) + 32
    return f"{temp_celsius}°C is equal to {temp_fahrenheit:.2f}°F."


@tool
def live_cricket_score(input:str):
    '''
    Useful to get the information about on going live cricker score
    Input can be anything (ignored).
    '''
    api_key = get_api_key("Cricket_API")
    #print(api_key)
    url = f"https://api.cricapi.com/v1/currentMatches?apikey={api_key}&offset=0"

    response = requests.get(url)
    if response.status_code != 200:
        return f"Error fetching score: {response.text}"

    data = response.json()
    print(data)

    if not data.get("data"):
        return "No live matches found."

    results = []
    for match in data["data"]:
        if match["status"] == "live":
            team1 = match["teams"][0]
            team2 = match["teams"][1]
            score = match.get("score", [])
            status = match.get("status", "Unknown")

            results.append(f"{team1} vs {team2} - Status: {status}")

    if not results:
        return "No ongoing live matches at the moment."

    return "\n".join(results)