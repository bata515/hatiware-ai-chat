# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Avatar UI Core is a Flask-based web application that provides a terminal-style chat interface with an AI avatar. The application uses Google's Gemini API for AI responses and features typewriter effects, sound effects, and animated avatars.

## Essential Commands

### Setup and Installation
```bash
# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate   # Windows

# Install dependencies
pip install -r requirements.txt

# Copy environment template and configure
cp .env.example .env
# Edit .env to add GEMINI_API_KEY and MODEL_NAME
```

### Running the Application
```bash
# Start development server
python app.py

# The app runs on http://localhost:5000 by default
```

### No Build/Test Commands Available
This project currently has no build system, linting, or testing framework configured. The app runs directly via Python.

## Architecture

### Backend (Flask)
- **app.py**: Main Flask application with routes for UI and chat API
- **settings.py**: Centralized configuration management loading from .env
- **requirements.txt**: Python dependencies (Flask, google-generativeai, python-dotenv)

### Frontend (Vanilla JavaScript + ES6 Modules)
- **static/js/app.js**: Main application entry point and module initialization
- **static/js/chat.js**: Chat functionality and API communication
- **static/js/animation.js**: Avatar animation and typewriter effects
- **static/js/sound.js**: Web Audio API sound generation
- **static/js/settings.js**: Frontend configuration management
- **static/css/style.css**: Terminal-style UI styling
- **templates/index.html**: Single HTML template

### Configuration System
All settings are managed through:
1. **.env file**: Contains API keys and customizable parameters
2. **settings.py**: Loads and validates environment variables with defaults
3. **Frontend config**: Settings passed from Flask to JavaScript via template

Required environment variables:
- `GEMINI_API_KEY`: Google Gemini API key
- `MODEL_NAME`: Gemini model to use (e.g., gemini-2.0-flash)

### Key Features
- **Terminal UI**: Green-on-black classic terminal styling
- **AI Chat**: Gemini API integration with persistent chat sessions
- **Avatar Animation**: Image switching during AI responses
- **Typewriter Effect**: Character-by-character text display
- **Sound Effects**: Web Audio API typing sounds
- **Responsive Design**: Works on desktop and mobile

### File Structure Notes
- **static/images/**: Contains avatar images (usagi.png currently in use)
- **docs/**: Development documentation (not required for app functionality)
- **venv/**: Python virtual environment (git ignored)

## Important Implementation Details

### Settings Management
- All configuration flows through `settings.py` which loads from `.env`
- Frontend receives config via Flask template rendering in `index.html`
- No hardcoded values - everything is configurable

### AI Integration
- Uses Google Generative AI library for Gemini API access
- Chat session persists during application runtime
- System instructions and model parameters configurable via .env

### Frontend Architecture
- ES6 modules with clear separation of concerns
- Manager classes for sound, animation, and chat functionality
- Event-driven communication between modules