import speech_recognition as sr
import pyttsx3
import datetime
import webbrowser
import os

class VoiceAssistant:
    def __init__(self):
        # Initialize the text-to-speech engine
        self.engine = pyttsx3.init()
        # Set properties for the voice
        voices = self.engine.getProperty('voices')
        self.engine.setProperty('voice', voices[0].id)  # Index 0 for male voice
        self.engine.setProperty('rate', 150)  # Speaking rate
        
        # Initialize speech recognizer
        self.recognizer = sr.Recognizer()
        
    def speak(self, text):
        """Convert text to speech"""
        self.engine.say(text)
        self.engine.runAndWait()
        
    def listen(self):
        """Listen to user's voice input and convert to text"""
        with sr.Microphone() as source:
            print("Listening...")
            # Adjust for ambient noise
            self.recognizer.adjust_for_ambient_noise(source, duration=1)
            # Listen for user's input
            audio = self.recognizer.listen(source)
            
            try:
                # Use Google's speech recognition
                text = self.recognizer.recognize_google(audio)
                print(f"You said: {text}")
                return text.lower()
            except sr.UnknownValueError:
                print("Sorry, I didn't catch that.")
                return ""
            except sr.RequestError:
                print("Sorry, there was an error with the speech recognition service.")
                return ""
    
    def process_command(self, command):
        """Process user's command and execute appropriate action"""
        if 'time' in command:
            current_time = datetime.datetime.now().strftime('%I:%M %p')
            self.speak(f"The current time is {current_time}")
            
        elif 'date' in command:
            current_date = datetime.datetime.now().strftime('%B %d, %Y')
            self.speak(f"Today's date is {current_date}")
            
        elif 'search' in command:
            search_term = command.replace('search', '').strip()
            url = f"https://www.google.com/search?q={search_term}"
            webbrowser.open(url)
            self.speak(f"Searching for {search_term}")
            
        elif 'open' in command:
            if 'notepad' in command:
                os.system('notepad.exe')
                self.speak("Opening Notepad")
            elif 'calculator' in command:
                os.system('calc.exe')
                self.speak("Opening Calculator")
                
        elif 'exit' in command or 'quit' in command:
            self.speak("Goodbye!")
            return False
            
        return True

    def run(self):
        """Main loop to run the voice assistant"""
        self.speak("Hello! I'm your voice assistant. How can I help you?")
        
        running = True
        while running:
            command = self.listen()
            if command:
                running = self.process_command(command)

if __name__ == "__main__":
    # Create and run the voice assistant
    assistant = VoiceAssistant()
    assistant.run()