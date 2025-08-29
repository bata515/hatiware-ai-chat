# Htiware AI Chat

A classic terminal-style UI core. Provides an extensible project foundation from chat UI to CLI integration.

> **日本語版**: [README.ja.md](README.ja.md) | **English**: README.md

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/python-3.8%2B-blue.svg)
![Flask](https://img.shields.io/badge/flask-3.0.0-green.svg)

<img width="1180" height="332" alt="image" src="https://github.com/user-attachments/assets/ff9cc6a3-7e09-4169-8aab-45e8ce8ee90f" />

## Features

- **Terminal UI** - Classic green-on-black terminal interface
- **AI Avatar** - Speech-synchronized pixel art avatar display
- **Typewriter Effect** - Character-by-character real-time display animation
- **Sound Effects** - Typing sound generation via Web Audio API
- **Complete Configuration Management** - Centralized management of all operation parameters via `.env` file

## Basic Operations

1. **Send Message**: Enter text in the input field at the bottom of the screen and press Enter
2. **Chat History**: View automatically scrolling conversation history
3. **Avatar**: Avatar displays response animation during AI responses

## Quick Start

### Requirements

- Python 3.8 or higher
- Google AI Studio API key ([Get it here](https://aistudio.google.com/app/apikey))

### Installation Steps

#### 1. Get the Project

```bash
# Clone the repository (or download and extract ZIP)
git clone https://github.com/yourusername/avatar-ui-core.git
cd avatar-ui-core
```

#### 2. Create Python Virtual Environment

Using a virtual environment allows you to run the project without polluting your system's Python environment.

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# Linux/Mac:
source venv/bin/activate
# Windows (Command Prompt):
venv\Scripts\activate
# Windows (PowerShell):
venv\Scripts\Activate.ps1
```

When the virtual environment is activated, `(venv)` will appear in your terminal prompt.

#### 3. Install Required Packages

```bash
# Install packages listed in requirements.txt
pip install -r requirements.txt
```

### Configuration

#### 1. Prepare Environment Variables File

```bash
# Copy template file to create .env file
cp .env.example .env
# Windows: copy .env.example .env
```

#### 2. Set API Key

Open the `.env` file with a text editor and configure the required items:

```bash
# Only these required items need to be changed (other items work with default values)
GEMINI_API_KEY=paste_your_obtained_api_key_here
MODEL_NAME=gemini-2.0-flash  # or gemini-2.5-pro etc.
```

**Important**: The `.env` file contains sensitive information, so never commit it to Git.

### Launch

```bash
# Start the application
python app.py
```

When startup is successful, you'll see a message like this:

```
 * Running on http://127.0.0.1:5000
```

Access `http://localhost:5000` in your browser.

## Project Structure

```
avatar-ui-core/
├── app.py                  # Flask application main body
├── settings.py             # Configuration management module
├── requirements.txt        # Python dependencies
├── .env.example           # Environment variables template
├── static/
│   ├── css/
│   │   └── style.css      # UI style definitions
│   ├── js/
│   │   ├── app.js         # Main entry point
│   │   ├── chat.js        # Chat functionality
│   │   ├── animation.js   # Animation control
│   │   ├── sound.js       # Sound effects
│   │   └── settings.js    # Frontend settings
│   └── images/
│       └── usagi.png       # Avatar
└── templates/
    └── index.html         # HTML template
```

**Note**: The `docs/` folder contains development notes and assets and does not affect application operation.

## Customization Methods

All settings can be adjusted in the `.env` file.

### 1. Change Avatar

Replace image files:

- `static/images/hatiware_close_mouth.png`
- `static/images/hatiware_open_mouth.png`

### 2. AI Personality Settings

Edit the following items in the `.env` file:

```bash
AVATAR_NAME=Hatiware
AVATAR_FULL_NAME=Hatiware Communicator
SYSTEM_INSTRUCTION=You are an AI assistant that behaves like the character "Hachiware" from "Chiikawa". As a speech characteristic, you often use phrases like "nantoka nare~!!" and also speak using inverted word order. You also have a fundamentally positive personality.
```

### 3. UI Behavior Adjustment

Adjust various speeds in the `.env` file:

```bash
# Typing speed (milliseconds, smaller = faster)
TYPEWRITER_DELAY_MS=30

# Lip-sync animation interval (milliseconds)
MOUTH_ANIMATION_INTERVAL_MS=100
```

### 4. Sound Settings

Customize sound effects in the `.env` file:

```bash
BEEP_FREQUENCY_HZ=600   # Sound pitch (Hz)
BEEP_VOLUME=0.1         # Volume (0.0-1.0)
BEEP_DURATION_MS=30     # Sound length (milliseconds)
```

**Note**: Application restart is required after changing settings.

## Environment Variables List

| Variable Name                 | Description                            | Default Value        | Required |
| ----------------------------- | -------------------------------------- | -------------------- | -------- |
| `GEMINI_API_KEY`              | Google Gemini API key                  | -                    | ✅       |
| `MODEL_NAME`                  | Gemini model to use                    | gemini-2.0-flash     | ✅       |
| **Server Settings**           |                                        |                      |          |
| `SERVER_PORT`                 | Server port number                     | 5000                 |          |
| `DEBUG_MODE`                  | Enable debug mode                      | True                 |          |
| **Avatar Settings**           |                                        |                      |          |
| `AVATAR_NAME`                 | AI assistant name                      | Spectra              |          |
| `AVATAR_FULL_NAME`            | AI assistant full name                 | Spectra Communicator |          |
| `AVATAR_IMAGE_IDLE`           | Avatar image when idle                 | idle.png             |          |
| `AVATAR_IMAGE_TALK`           | Avatar image when speaking             | talk.png             |          |
| **AI Personality Settings**   |                                        |                      |          |
| `SYSTEM_INSTRUCTION`          | AI personality and response style      | Technical, concise   |          |
| **UI Settings**               |                                        |                      |          |
| `TYPEWRITER_DELAY_MS`         | Typewriter effect speed (milliseconds) | 50                   |          |
| `MOUTH_ANIMATION_INTERVAL_MS` | Lip-sync animation interval (ms)       | 150                  |          |
| **Sound Settings**            |                                        |                      |          |
| `BEEP_FREQUENCY_HZ`           | Beep sound frequency (Hz)              | 800                  |          |
| `BEEP_DURATION_MS`            | Beep sound length (milliseconds)       | 50                   |          |
| `BEEP_VOLUME`                 | Beep sound volume (0.0-1.0)            | 0.05                 |          |
| `BEEP_VOLUME_END`             | Beep sound end volume                  | 0.01                 |          |

## Tech Stack

### Backend

- **Flask 3.0.0** - Web application framework
- **google-generativeai 0.8.3** - Gemini API integration
- **python-dotenv 1.0.0** - Environment variable management

### Frontend

- **ES6 Modules** - Modularized JavaScript
- **Web Audio API** - Browser-native sound generation
- **CSS3** - Modern styling
- **Fira Code** - Programming monospace font

## License

MIT License - See [LICENSE](LICENSE) file for details

## Credits

Developed by Batannu

### Technologies Used

- Google Gemini API
- Flask Framework
- Fira Code Font

---

**Note**: This project is created for entertainment and creative purposes. When using in production environments, please implement appropriate security measures.

---

## Final Notes

This repository is an improved version of the [original project](https://github.com/sito-sikino/avatar-ui-core/tree/main) created by Sito Sikino.

### Changes Made

- Avatar image replacement
- Avatar conversation settings modification

## Acknowledgments

Special thanks to [Sito Sikino](https://github.com/sito-sikino) for the original implementation that made this project possible.
