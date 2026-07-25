# NebAI — Desktop AI Assistant

NebAI is a simple desktop AI assistant built with Python and Tkinter. It can tell
you the time and day, take and read back voice/text notes, listen for spoken
commands, and set time-based reminders — all through a small GUI with voice
feedback (text-to-speech).

## Features

- **Tell Time / Tell Day** — speaks the current time or day of the week.
- **Voice Commands** — click "Listen" and speak a command (e.g. "time", "day",
  "note", "read notes", "reminder", "exit") and the assistant routes it to the
  right action.
- **Take a Note** — records a spoken note and appends it, with a timestamp, to
  `notes.txt`.
- **Read Notes** — reads back all previously saved notes out loud.
- **Set Reminder** — set a task and a time (HH:MM, 24-hour format); the app
  checks every minute and pops up + speaks an alert when it's due.
- **Text-to-Speech feedback** for every action via `pyttsx3`.
- **Error logging** to `assistant.log` so failures (mic issues, file errors,
  etc.) don't crash the app silently.

## Project Structure

```
AI-Assistant--main/
├── NebAI.py            # Main application (run this)
├── requirements.txt    # Python dependencies
├── assets/             # Optional: put background.jpg here for a custom UI background
└── README.md
```

## Requirements

- Python 3.9+
- A working microphone (for voice commands and voice notes)
- Speakers (for text-to-speech output)

## Setup Instructions

1. **Clone the repository**
   ```bash
   git clone https://github.com/Sania-Nawaz0/AI-Assistant.git
   cd AI-Assistant
   ```

2. **(Recommended) Create a virtual environment**
   ```bash
   python -m venv venv
   # Windows
   venv\Scripts\activate
   # macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

   > **Note on PyAudio:** `PyAudio` (required by `SpeechRecognition` for
   > microphone access) can fail to install via plain `pip` on Windows.
   > If `pip install -r requirements.txt` fails on `pyaudio`, install it with:
   > ```bash
   > pip install pipwin
   > pipwin install pyaudio
   > ```
   > On macOS, install `portaudio` first: `brew install portaudio`, then
   > `pip install pyaudio`.
   > On Linux: `sudo apt-get install python3-pyaudio` or
   > `sudo apt-get install portaudio19-dev` then `pip install pyaudio`.

4. **(Optional) Add a background image**
   Place an image at `assets/background.jpg` if you want a custom background
   in the app window. The app runs fine without this — it just skips the
   background if the file isn't found.

## Usage

Run the app:
```bash
python NebAI.py
```

A window will open with buttons for each feature. You can either:
- Click a button directly (Tell Time, Tell Day, Take a Note, Read Notes, Set
  Reminder), or
- Click **Listen** and speak a command out loud.

Notes are saved locally in `notes.txt` (created automatically on first use).
Errors are logged to `assistant.log`.

## Known Limitations

- Voice recognition (`speech_recognition`) requires an internet connection
  (it uses Google's speech-to-text API by default).
- Reminders are checked while the app is running only — closing the app
  cancels pending reminders.
- Tested primarily on Windows; TTS voice availability may vary by OS.

## License

This project is for academic/coursework purposes.
