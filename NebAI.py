import os
import pyttsx3
import speech_recognition as sr
import datetime
import tkinter as tk
from tkinter import messagebox, simpledialog
import logging
import threading
import time
from PIL import Image, ImageTk


# Configure logging
logging.basicConfig(filename='assistant.log', level=logging.ERROR,
                    format='%(asctime)s:%(levelname)s:%(message)s')

# Initialize Speech Engine
engine = pyttsx3.init()

# Define Speak Function
def speak(text):
    engine.say(text)
    engine.runAndWait()

# Define Functions for Buttons
def tell_time():
    time_now = datetime.datetime.now().strftime("%H:%M")
    speak("The current time is " + time_now)
    status_label.config(text=f"Status: Time told - {time_now}")

def tell_day():
    day = datetime.datetime.today().strftime("%A")
    speak("Today is " + day)
    status_label.config(text=f"Status: Day told - {day}")

def get_audio():
    r = sr.Recognizer()
    try:
        with sr.Microphone() as source:
            speak("Listening...")
            status_label.config(text="Status: Adjusting for ambient noise...")
            r.adjust_for_ambient_noise(source, duration=1)
            r.dynamic_energy_threshold = True
            
            try:
                audio_data = r.listen(source, timeout=5, phrase_time_limit=5)
                status_label.config(text="Status: Processing audio...")
                text = r.recognize_google(audio_data)
                status_label.config(text=f"Status: Recognized - {text}")
                return text
            except sr.WaitTimeoutError:
                speak("No speech detected.")
                status_label.config(text="Status: No speech detected.")
                return ""
            except sr.UnknownValueError:
                speak("Sorry, I did not catch that.")
                status_label.config(text="Status: Unrecognized speech.")
                return ""
            except sr.RequestError:
                speak("Could not request results; check your network connection.")
                status_label.config(text="Status: Network error.")
                return ""
    except Exception as e:
        speak("Microphone error. Please check your microphone.")
        logging.error(f"Microphone error: {e}")
        status_label.config(text="Status: Microphone error.")
        return ""

def take_note():
    speak("What would you like me to write down?")
    status_label.config(text="Status: Awaiting note input...")
    note = get_audio()
    if note:
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        try:
            with open("notes.txt", "a") as f:
                f.write(f"{timestamp}: {note}\n")
            speak("I've made a note of that.")
            status_label.config(text="Status: Note taken.")
        except Exception as e:
            speak("Failed to save the note.")
            logging.error("Error in take_note: %s", e)
            status_label.config(text="Status: Failed to save note.")
    else:
        speak("I didn't catch that. Please try again.")
        status_label.config(text="Status: Note not taken.")

def read_notes():
    try:
        with open("notes.txt", "r") as f:
            notes = f.read()
            if notes:
                speak("Here are your notes:")
                speak(notes)
                status_label.config(text="Status: Notes read.")
            else:
                speak("You have no notes.")
                status_label.config(text="Status: No notes to read.")
    except FileNotFoundError:
        speak("No notes found.")
        status_label.config(text="Status: No notes file.")
    except Exception as e:
        speak("Failed to read notes.")
        logging.error("Error in read_notes: %s", e)
        status_label.config(text="Status: Failed to read notes.")

def greet_user():
    hour = datetime.datetime.now().hour
    if 0 <= hour < 12:
        greeting = "Good morning!"
    elif 12 <= hour < 18:
        greeting = "Good afternoon!"
    else:
        greeting = "Good evening!"
    speak(greeting)
    speak("I am your AI assistant. How can I help you today?")
    status_label.config(text="Status: User greeted.")

def listen_command():
    try:
        speak("I'm listening. Please say a command.")
        status_label.config(text="Status: Listening for command...")
        command = get_audio().lower()
        
        if not command:
            speak("I didn't hear anything. Please try again.")
            return

        if 'time' in command:
            tell_time()
        elif 'day' in command:
            tell_day()
        elif 'note' in command:
            take_note()
        elif 'read' in command and 'notes' in command:
            read_notes()
        elif 'reminder' in command:
            set_reminder()
        elif 'exit' in command:
            speak("Goodbye!")
            status_label.config(text="Status: Exiting application.")
            root.quit()
        else:
            speak("Sorry, I didn't understand that command.")
            status_label.config(text="Status: Unrecognized command.")
    except Exception as e:
        speak("An error occurred while listening.")
        logging.error(f"Error in listen_command: {e}")
        status_label.config(text="Status: Listening error.")

# Reminders Feature
reminders = []

def set_reminder():
    task = simpledialog.askstring("Set Reminder", "What do you want to be reminded about?")
    if not task:
        speak("No task entered. Reminder not set.")
        status_label.config(text="Status: Reminder not set.")
        return

    time_str = simpledialog.askstring("Set Reminder", "When should I remind you? (HH:MM in 24-hour format)")
    if not time_str:
        speak("No time entered. Reminder not set.")
        status_label.config(text="Status: Reminder not set.")
        return

    try:
        reminder_time = datetime.datetime.strptime(time_str, "%H:%M").replace(
            year=datetime.datetime.now().year,
            month=datetime.datetime.now().month,
            day=datetime.datetime.now().day
        )
        if reminder_time < datetime.datetime.now():
            reminder_time += datetime.timedelta(days=1)

        reminders.append({"task": task, "time": reminder_time})
        speak(f"Reminder set for {time_str}.")
        status_label.config(text=f"Status: Reminder set for {time_str} - {task}")
    except ValueError:
        speak("Invalid time format. Please enter time in HH:MM format.")
        status_label.config(text="Status: Invalid time format.")

def check_reminders():
    while True:
        now = datetime.datetime.now().replace(second=0, microsecond=0)
        due_reminders = [rem for rem in reminders if rem["time"] == now]
        for rem in due_reminders:
            speak(f"Reminder: {rem['task']}")
            messagebox.showinfo("Reminder", f"Reminder: {rem['task']}")
            reminders.remove(rem)
            status_label.config(text=f"Status: Reminder triggered - {rem['task']}")
        time.sleep(60)  # Check every minute

def start_reminder_thread():
    reminder_thread = threading.Thread(target=check_reminders, daemon=True)
    reminder_thread.start()

# Set Up GUI
root = tk.Tk()
root.title("AI Assistant")
root.geometry("400x700")

# Add background image (optional — app still runs if the image is missing)
BG_IMAGE_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets", "background.jpg")
try:
    bg_image = Image.open(BG_IMAGE_PATH)
    bg_image = bg_image.resize((400, 700), Image.LANCZOS)
    bg_photo = ImageTk.PhotoImage(bg_image)
    bg_label = tk.Label(root, image=bg_photo)
    bg_label.place(x=0, y=0, relwidth=1, relheight=1)
except FileNotFoundError:
    logging.error(f"Background image not found at {BG_IMAGE_PATH}; continuing without it.")

# Add a Label to Display Status
status_label = tk.Label(root, text="Status: Ready", wraplength=350, anchor='w', justify='left', bg="lightgray")
status_label.pack(pady=10, padx=10, fill='x')

# Define Button Styles
button_width = 25
button_padding = 10

btn_time = tk.Button(root, text="Tell Time", command=tell_time, width=button_width)
btn_time.pack(pady=button_padding)

btn_day = tk.Button(root, text="Tell Day", command=tell_day, width=button_width)
btn_day.pack(pady=button_padding)

btn_note = tk.Button(root, text="Take a Note", command=take_note, width=button_width)
btn_note.pack(pady=button_padding)

btn_read_notes = tk.Button(root, text="Read Notes", command=read_notes, width=button_width)
btn_read_notes.pack(pady=button_padding)

btn_listen = tk.Button(root, text="Listen", command=listen_command, width=button_width)
btn_listen.pack(pady=button_padding)

btn_set_reminder = tk.Button(root, text="Set Reminder", command=set_reminder, width=button_width)
btn_set_reminder.pack(pady=button_padding)

btn_exit = tk.Button(root, text="Exit", command=root.quit, width=button_width)
btn_exit.pack(pady=button_padding)

# Run the Application
greet_user()
start_reminder_thread()
root.mainloop()
