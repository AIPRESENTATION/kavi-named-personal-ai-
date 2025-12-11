import wikipedia
import pyttsx3
import webbrowser
import os
import datetime
import psutil
import speech_recognition as sr
import pvporcupine
import pyaudio
import struct

# Initialize speech engine and recognizer
engine = pyttsx3.init()
recognizer = sr.Recognizer()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)  # Female voice
engine.setProperty('volume', 1.0)

def speak(text):
    print("Kavi:", text)
    engine.say(text)
    engine.runAndWait()

def listen():
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source, duration=0.5)
        print("Listening to you, Rakesh...")
        try:
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=8)
            command = recognizer.recognize_google(audio)
            print(f"You: {command}")
            return command.lower()
        except sr.WaitTimeoutError:
            speak("I didn't hear anything.")
        except sr.UnknownValueError:
            speak("Sorry, I didn't understand.")
        except sr.RequestError:
            speak("Network issue. Try again.")
    return ""

def handle_personal_commands(query):
    if "play" in query and "youtube" in query:
        song = query.replace("play", "").replace("on youtube", "").strip()
        if not song:
            speak("Please specify a song to play.")
            return True
        speak(f"Playing {song} on YouTube.")
        pywhatkit.playonyt(song)

    elif "open youtube" in query or "go to youtube" in query or "turn on youtube" in query:
        speak("Opening YouTube.")
        webbrowser.open("https://www.youtube.com")

    elif "open google" in query:
        speak("Opening Google.")
        webbrowser.open("https://www.google.com")

    elif "open notepad" in query:
        speak("Opening Notepad.")
        os.system("notepad")

    elif "search" in query or "find" in query:
        search_term = query.replace("search", "").replace("find", "").strip()
        if not search_term:
            speak("Please specify what to search for.")
            return True
        speak(f"Searching for {search_term} on Google.")
        webbrowser.open(f"https://www.google.com/search?q={search_term}")

    elif "time" in query:
        current_time = datetime.datetime.now().strftime("%I:%M %p")
        speak(f"The time is {current_time}")

    elif "girlfriend name " in query or "who is my girlfriend" in query or "my bujji name " in query:
        speak("kavya bangaram is your girlfriend ")

    elif "date" in query:
        today = datetime.date.today().strftime("%B %d, %Y")
        speak(f"Today is {today}")

    elif "battery" in query:
        battery = psutil.sensors_battery()
        if battery:
            percent = battery.percent
            plugged = battery.power_plugged
            status = "charging" if plugged else "not charging"
            speak(f"Your battery is at {percent} percent and it is {status}.")
        else:
            speak("Unable to retrieve battery information.")

    elif "shutdown" in query:
        speak("Shutting down the system. Goodbye!")
        os.system("shutdown /s /t 1")

    elif "restart" in query:
        speak("Restarting the system. Hold tight!")
        os.system("shutdown /r /t 1")

    elif "walk wave" in query:
        speak("Here is your walk wave.")
        try:
            from playsound import playsound
            playsound("walk.wav")
        except Exception:
            speak("Sorry, I couldn't play the walk wave sound.")
        return True

    else:
        return False
    return True

def handle_information_query(query):
    try:
        # Remove leading keywords
        topic = query.replace("tell me about", "").replace("what is", "").replace("who is", "").replace("explain", "").strip()
        if not topic:
            speak("Please specify a topic to explain.")
            return True
        speak(f"Let me explain {topic}.")
        summary = wikipedia.summary(topic, sentences=3)
        speak(summary)
        return True
    except wikipedia.exceptions.DisambiguationError:
        speak("That topic has multiple meanings. Can you be more specific?")
        return True
    except wikipedia.exceptions.PageError:
        speak("Sorry, I couldn't find anything on that.")
        return True
    except Exception as e:
        speak("Something went wrong while searching Wikipedia.")
        return True


 
if __name__ == "__main__":
    speak("Hello Rakesh, I’m Kavi. Your personal AI. ""How can I assist you today?")
    listen()