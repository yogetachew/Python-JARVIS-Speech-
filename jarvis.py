"""
    Name: jarvis.py
    Author: Yonatan Getachew
    Created: 02/16/25
    Purpose: Voice recognition from Google Speech API with Wikipedia integration
"""

from wikipedia_oop import WikipediaApp
import speech_recognition as sr
import pyttsx3
from sys import exit

name = "Yonatan"

class Jarvis:
    def __init__(self):
        # Initialize SpeechRecognition recognizer object
        self.recognizer = sr.Recognizer()
        # Initialize pyttsx3 text-to-speech engine
        self.engine = pyttsx3.init()
        # Adjust the speech rate (speed)
        self.engine.setProperty('rate', 120)
        # Initialize WikipediaApp
        self.wikipedia = WikipediaApp()

    # Function to recognize user voice input
    def recognize_voice(self):
        with sr.Microphone() as source:
            print("Listening . . .")
            audio = self.recognizer.listen(source)
            try:
                print('Recognizing . . .')
                recognized_words = self.recognizer.recognize_google(
                    audio, language='en-US', show_all=True
                )
                # Extract the recognized words with the highest confidence
                recognized_text = recognized_words['alternative'][0]['transcript']
                print(f"You may have said: {recognized_text}")
                return recognized_text
            except sr.UnknownValueError:
                print("Google Speech Recognition could not understand audio")
                return None
            except sr.RequestError as e:
                print(f"Google Speech did not respond: {e}")
                return None

    # Function to speak out the provided text
    def speak(self, text):
        self.engine.say(text)
        self.engine.runAndWait()

    # Function to execute voice commands
    def execute_commands(self, command):
        command = command.lower()

        if command == "quit":
            self.speak("Goodbye!")
            exit()
        
        elif command == "what is my name":
            self.speak(f"Your name is {name}")

        elif "search wikipedia for" in command:
            search_term = command.replace("search wikipedia for", "").strip()
            if search_term:
                self.speak(f"Searching Wikipedia for {search_term}")
                result = self.wikipedia.get_wikipedia(search_term)
                print(result)
                self.speak(result[:200])  # Read the first 200 characters for brevity
            else:
                self.speak("Please say a search term after 'search Wikipedia for'.")

        else:
            self.speak("Command not recognized.")

# Create a Jarvis program object
jarvis = Jarvis()

while True:
    # Recognize user voice input
    recognized_text = jarvis.recognize_voice()

    if recognized_text:
        # Repeat the recognized words
        jarvis.speak(f"You said: {recognized_text}")
        # Execute voice commands
        jarvis.execute_commands(recognized_text)
