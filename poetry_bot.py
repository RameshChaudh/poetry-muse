from chatbot_base import ChatbotBase
import requests
import json
import threading
import platform
import subprocess

# Try importing pyttsx3 only for Windows/Linux users
try:
    import pyttsx3
    AUDIO_AVAILABLE = True
except ImportError:
    AUDIO_AVAILABLE = False

class PoetryBot(ChatbotBase):
    def __init__(self, model_name="mistral:latest"):
        super().__init__(name="The Poetry Muse")
        self.model_name = model_name 
        self.ollama_url = "http://localhost:11434/api/generate"
        
        self.styles = {
            "Shakespearean": "You are a bard from the 16th century. Write in iambic pentameter using archaic English (thee/thou). Keep it under 10 lines.",
            "Cyberpunk": "You are a rogue AI in the year 2077. Write gritty, neon-soaked free verse about technology and decay. Use slang like 'chrome' and 'glitch'.",
            "Haiku Master": "You are a Zen master. Respond ONLY in strict 5-7-5 syllable structure. Focus on nature and silence.",
            "Surrealist": "You are a dream weaver. Write bizarre, melting logic similar to Salvador Dali paintings. Use abstract metaphors."
        }

    def process_input(self, user_input):
        return user_input 

    def generate_response(self, processed_input):
        return "I am the Muse."

    # --- CUSTOM METHODS ---

    def generate_poem(self, topic, style, use_mock=False):
        system_prompt = self.styles.get(style, "You are a helpful poetic assistant.")
        full_prompt = f"System: {system_prompt}\nUser: Write a poem about {topic}. Return ONLY the poem text, no intro."

        if use_mock:
            return self._mock_generation(topic, style)

        try:
            payload = {
                "model": self.model_name,
                "prompt": full_prompt,
                "stream": False
            }
            response = requests.post(self.ollama_url, json=payload)
            if response.status_code == 200:
                result = response.json()
                return result.get("response", "Error: No response text found.")
            else:
                return f"Error: Ollama returned status {response.status_code}"
        except Exception as e:
            return f"⚠️ Connection Error: Is Ollama running? (Error: {str(e)})"

    def analyze_emotions(self, poem_text):
        text = poem_text.lower()
        scores = {
            "Joy": 1 + text.count("light") + text.count("love") + text.count("sun") + text.count("hope"),
            "Melancholy": 1 + text.count("dark") + text.count("rain") + text.count("lost") + text.count("gray"),
            "Chaos": 1 + text.count("neon") + text.count("crash") + text.count("burn") + text.count("scream"),
            "Serenity": 1 + text.count("leaf") + text.count("quiet") + text.count("flow") + text.count("peace")
        }
        total = sum(scores.values())
        return {k: (v/total)*100 for k, v in scores.items()}

    def speak_poem(self, text):
        """
        MAC NATIVE FIX: Uses the built-in 'say' command.
        """
        def _speak():
            # CHECK: Are we on a Mac?
            if platform.system() == 'Darwin':
                try:
                    # Use Mac's native voice command
                    # -r 170 sets the speed (slower is better for poetry)
                    subprocess.run(['say', '-r', '170', text])
                except Exception as e:
                    print(f"Mac Audio Error: {e}")
            
            # Fallback for Windows/Linux
            elif AUDIO_AVAILABLE:
                try:
                    engine = pyttsx3.init()
                    engine.setProperty('rate', 130)
                    engine.say(text)
                    engine.runAndWait()
                except Exception as e:
                    print(f"Pyttsx3 Error: {e}")
            else:
                print("Audio library not available.")

        # Run in a separate thread so the app doesn't freeze
        thread = threading.Thread(target=_speak)
        thread.start()

    def _mock_generation(self, topic, style):
        return f"(Mock {style} Poem about {topic})\nIn the digital void,\nWeaving codes of light and sound,\nThe system awakens."