# Lexicon

Lexicon is a locally executed AI chat application designed to provide fast and natural responses without requiring an internet connection. It utilizes the **Meta-Llama-3.1-8B-Instruct-Q4_K_M.gguf** model to process and generate responses.

## Features

- **Local execution**: No internet connection required.
- **Graphical interface**: Built with `CustomTKinter` for an intuitive experience.
- **Automatic conversation saving**: Chats are automatically stored in JSON format.
- **Load previous conversations**: Load saved chats from JSON to continue previous sessions.
- **Multiple conversation support**: Manage multiple chats based on stored JSON files.
- **Text-to-Speech (TTS)**: Option for the AI to read responses aloud using `pyttsx3`.
- **Speech-to-Text transcription**: Convert voice into text for AI interaction.
- **GPU optimization**: Can utilize GPU acceleration for better performance with `llama-cpp-python`.
- **Voice command support** (coming soon).

## Installation & Execution

### Prerequisites

- Python 3.8 or later
- Required dependencies:
  ```bash
  pip install customtkinter llama-cpp-python pyttsx3 speechrecognition
  ```

### Running the Application

1. Download or clone this repository.
2. Run the main script:
   ```bash
   python lex.py
   ```

## Usage

- Type a message in the input field and press "Send".
- Enable the "TTS" switch to have the AI read responses aloud.
- Use the "Save JSON" and "Load JSON" buttons to manage conversations.
- Enable voice recognition to send spoken messages.

## Compiling to Executable

To generate a standalone executable for Windows using PyInstaller:
```bash
pyinstaller --distpath DEV/dist --workpath DEV/build --specpath DEV/ \
--noconfirm --hidden-import llama-cpp-python --hidden-import pyttsx3 \
--hidden-import speechrecognition --hidden-import comtypes.client \
--windowed --hidden-import comtypes.gen --onedir \
--add-data "assets;assets/" --add-data "models/;models/" \
--icon "assets/lex_1.ico" lex.py
```

## Contributions

If you want to improve Lexicon, contributions are welcome! Feel free to fork the project and submit a pull request with your enhancements.

## License

This project is licensed under the MIT License.

## Support

If you like this project and want to support it, you can donate via GitHub Sponsors or PayPal. Your support helps maintain and improve Lexicon!

