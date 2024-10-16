import threading
import speech_recognition as sr
import pyttsx3
import geocoder
import requests
from datetime import datetime
from bs4 import BeautifulSoup

# OpenWeatherMap API key
API_KEY = 'your_api_key_here'

def listen(language='en-US'):
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        audio = r.listen(source)

    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language=language)
        print(f"You said: {query}")
        return query.lower()
    except sr.UnknownValueError:
        return None
    except sr.RequestError:
        return None

def speak(text):
    engine = pyttsx3.init()
    
    # Adjust speech rate (lower value for slower speech)
    engine.setProperty('rate', 135)  # Adjust this value as needed
    
    # Set voice properties for increased clarity
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[0].id)  # You can try different voice indices for clarity
    
    engine.say(text)
    engine.runAndWait()
    print(f"Krish: {text}")

def get_location():
    try:
        g = geocoder.ip('me')
        return f"You are currently located in {g.city}, {g.country}."
    except Exception as e:
        print(f"An error occurred while fetching location: {e}")
        return "I couldn't determine your current location."

def get_weather(city):
    try:
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
        response = requests.get(url)
        data = response.json()
        if data['cod'] == 200:
            weather_desc = data['weather'][0]['description']
            temp = data['main']['temp']
            humidity = data['main']['humidity']
            wind_speed = data['wind']['speed']
            return f"The weather in {city} is {weather_desc}. The temperature is {temp}°C, humidity is {humidity}%, and wind speed is {wind_speed} m/s."
        else:
            return "Sorry, I couldn't retrieve weather information for that location."
    except Exception as e:
        print(f"An error occurred while fetching weather data: {e}")
        return "Sorry, I encountered an error while fetching weather data."

def get_date_time():
    now = datetime.now()
    current_date = now.strftime("%A, %B %d, %Y")
    current_time = now.strftime("%I:%M %p")
    return f"Today's date is {current_date} and the current time is {current_time}."

def search_and_summarize(query):
    try:
        search_url = f"https://www.google.com/search?q={query}"
        response = requests.get(search_url)
        soup = BeautifulSoup(response.text, 'html.parser')
        search_results = soup.find_all('div', class_='BNeawe s3v9rd AP7Wnd')
        if search_results:
            summary = search_results[0].text
            return summary
        else:
            return "No relevant information found."
    except Exception as e:
        print(f"An error occurred while searching and summarizing: {e}")
        return "Sorry, I encountered an error while searching."

def handle_user_input():
    speak("Hello, my name is Krish. How can I help you today?")
    while True:
        user_input = listen(language='en-US')  # Set default language to English ('en-US')
        if user_input is not None:
            if "exit" in user_input:
                speak("Goodbye! Have a great day!")
                break
            elif "location" in user_input:
                response = get_location()
                speak(response)
            elif "weather" in user_input:
                city_name = input("Please specify the city name: ")
                response = get_weather(city_name)
                speak(response)
            elif "date and time" in user_input or "current date" in user_input or "current time" in user_input:
                response = get_date_time()
                speak(response)
            elif "name" in user_input:
                speak("My name is Krish.")
            else:
                response = search_and_summarize(user_input)
                speak(response)
        else:
            speak("Sorry, I didn't catch that. Could you please repeat?")

# Start the user input handling thread
input_thread = threading.Thread(target=handle_user_input)
input_thread.daemon = True
input_thread.start()

# Keep the main thread running to prevent the program from exiting
while True:
    pass
