import tkinter as tk
from tkinter import scrolledtext, filedialog, messagebox
import speech_recognition as sr
import pyttsx3
from pydub import AudioSegment

# Set the path to the ffmpeg binary
AudioSegment.converter = r"C:\path\to\ffmpeg\bin\ffmpeg.exe"

# Initialize text-to-speech engine
engine = pyttsx3.init()


def load_audio_file():
    file_path = filedialog.askopenfilename(filetypes=[("Audio files", "*.wav *.mp3 *.flac")])
    if file_path:
        transcribe_audio_file(file_path)


def transcribe_audio_file(file_path):
    recognizer = sr.Recognizer()
    try:
        # Convert audio file to WAV format if necessary
        if not file_path.endswith('.wav'):
            audio = AudioSegment.from_file(file_path)
            file_path = "temp.wav"
            audio.export(file_path, format="wav")

        with sr.AudioFile(file_path) as source:
            audio = recognizer.record(source)
            text = recognizer.recognize_google(audio)
            text_area.insert(tk.END, text + '\n')
    except sr.UnknownValueError:
        text_area.insert(tk.END, "Sorry, I could not understand the audio.\n")
    except sr.RequestError:
        text_area.insert(tk.END, "Could not request results; check your network connection.\n")
    except ValueError as ve:
        messagebox.showerror("Error", f"Audio file could not be processed: {ve}")


def text_to_speech():
    text = text_area.get("1.0", tk.END)
    engine.say(text)
    engine.runAndWait()


# Create the main window
root = tk.Tk()
root.title("Speech-to-Text and Text-to-Speech Application")

# Create a frame for the text area and buttons
frame = tk.Frame(root)
frame.pack(pady=10)

# Create a text area widget
text_area = scrolledtext.ScrolledText(frame, wrap=tk.WORD, width=50, height=10, font=("Arial", 12))
text_area.pack(pady=10)

# Create button to load and transcribe audio file
load_button = tk.Button(frame, text="Load Audio File", command=load_audio_file, font=("Arial", 12))
load_button.pack(side=tk.LEFT, padx=10)

# Create button for text-to-speech
tts_button = tk.Button(frame, text="Text to Speech", command=text_to_speech, font=("Arial", 12))
tts_button.pack(side=tk.RIGHT, padx=10)

root.mainloop()