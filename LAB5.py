import streamlit as st
import requests
import openai
#import google_generativeai as genai  # Assuming genai is the library for Gemini

# Function to get weather from OpenWeatherMap
def get_current_weather(location):
    API_key = st.secrets["weather_key"]
    
    if "," in location:
        location = location.split(",")[0].strip()
        
    urlbase = "https://api.openweathermap.org/data/2.5/"
    urlweather = f"weather?q={location}&appid={API_key}"
    url = urlbase + urlweather
    
    response = requests.get(url)
    data = response.json()
    
    # Extract temperatures and convert from Kelvin to Celsius
    temp = data['main']['temp'] - 273.15
    feels_like = data['main']['feels_like'] - 273.15
    temp_min = data['main']['temp_min'] - 273.15
    temp_max = data['main']['temp_max'] - 273.15
    humidity = data['main']['humidity']
    weather_description = data['weather'][0]['description']
    
    return {
        "location": location,
        "temperature": round(temp, 2),
        "feels_like": round(feels_like, 2),
        "temp_min": round(temp_min, 2),
        "temp_max": round(temp_max, 2),
        "humidity": round(humidity, 2),
        "weather_description": weather_description
    }

# Function to get clothing suggestion from OpenAI (Unchanged)
def get_clothing_suggestion_openai(weather_data):
    openai_api_key = st.secrets["openai_key"]
    openai.api_key = openai_api_key
    
    # Create the prompt with weather data
    prompt = (f"The current weather in {weather_data['location']} is "
              f"{weather_data['temperature']}°C with a feel-like temperature of "
              f"{weather_data['feels_like']}°C. The weather description is "
              f"{weather_data['weather_description']}. "
              "What kind of clothes should I wear today?")
    
    # Call the OpenAI chat completion endpoint (Unchanged)
    response = openai.chat.completion.create(
        model="gpt-3.5-turbo",  # Or "gpt-4" if available
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=100,
        temperature=0.7
    )
    
    # Access the message content from the response
    suggestion = response.choices[0].message['content'].strip()
    return suggestion

# Function to get clothing suggestion from Gemini using GenerativeModel
def get_clothing_suggestion_gemini(weather_data):
    # Load the Gemini model
    model = genai.GenerativeModel("gemini-1.5-flash")  # Load the model (replace with actual model if necessary)
    
    # Create the prompt with weather data
    prompt = (f"The current weather in {weather_data['location']} is "
              f"{weather_data['temperature']}°C with a feel-like temperature of "
              f"{weather_data['feels_like']}°C. The weather description is "
              f"{weather_data['weather_description']}. "
              "What kind of clothes should I wear today?")
    
    # Generate content using the Gemini model
    response = model.generate_content(prompt)
    
    # Extract the generated text
    suggestion = response.text.strip()
    
    return suggestion

# Streamlit UI for the Travel Weather and Suggestion Bot
def weather_suggestion_bot():
    st.title("Travel Weather & Suggestion Bot")
    
    # Get user input for location
    location = st.text_input("Enter a city (e.g., Syracuse, NY or London, England):", "Syracuse, NY")
    
    # Select between OpenAI and Gemini
    api_choice = st.selectbox("Choose the AI model for suggestions:", ["OpenAI", "Gemini"])
    
    if location:
        # Fetch the weather data
        weather_data = get_current_weather(location)
        
        if weather_data:
            st.write(f"Location: {weather_data['location']}")
            st.write(f"Temperature: {weather_data['temperature']}°C")
            st.write(f"Feels Like: {weather_data['feels_like']}°C")
            st.write(f"Weather: {weather_data['weather_description']}")
            
            # Get clothing suggestions from the selected API
            if api_choice == "OpenAI":
                suggestion = get_clothing_suggestion_openai(weather_data)
            else:
                suggestion = get_clothing_suggestion_gemini(weather_data)
                
            st.write(f"Suggested Clothes: {suggestion}")
        else:
            st.error("Unable to fetch weather data.")
    
if __name__ == "__main__":
    weather_suggestion_bot()
