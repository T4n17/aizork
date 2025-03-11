# 🎮 AIZork: Let Your LLM Play Zork!

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.8%2B-blue" alt="Python 3.8+">
  <img src="https://img.shields.io/badge/Game-Zork%20I-yellow" alt="Game: Zork I">
</p>

## 📖 Description

AIZork is a project that lets Large Language Models (LLMs) play the classic text adventure game Zork I: The Great Underground Empire. Watch as AI navigates the underground empire, solves puzzles, and attempts to win the game through natural language commands.

This project demonstrates how modern AI can interact with classic interactive fiction games through a pseudo-terminal interface.

<p align="center">
  <img src="demo.gif" alt="AIZork Demo" width="400">
</p>

### Features

- 🤖 Uses Llama 3.1:8B by default (customizable to other models)
- 🎮 Fully automated gameplay through AI decision-making
- 🔄 Real-time interaction with the Zork game environment
- 📊 Observe how AI interprets game context and generates commands
- 💬 Ability to provide suggestions to guide the AI during gameplay

## 🔧 Prerequisites

- **Python 3.8+** - For running the main application
- **[Ollama](https://ollama.ai/)** - For local LLM inference
- **Pydantic** - For data validation and settings management
- **[Dosemu2](https://github.com/dosemu2/dosemu2)** - DOS emulator to run Zork
- **Zork I: The Great Underground Empire** - DOS version of the game

## 📁 Directory Structure

```
.
├── ZORK/           # Directory containing Zork game files
├── main.py         # Main application script
├── requirements.txt # Project dependencies
└── README.md       # Project documentation
```

## 🚀 Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/AIZork.git
   cd AIZork
   ```

2. Set up a virtual environment:
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Place your Zork DOS game files in the `ZORK` directory

5. Ensure Ollama is running with the Llama 3.1:8B model:
   ```bash
   ollama pull llama3.1:8B
   ```

## 🎮 Usage

Start the AIZork application:

```bash
python3 main.py
```

The AI will automatically begin playing Zork. You can observe its decisions and gameplay in real-time.

### Game Modes

AIZork supports two different game modes:

1. **Autoplay Mode** (default): The AI plays the game completely autonomously.
   ```bash
   python3 main.py --mode autoplay
   ```

2. **Suggestion Mode**: You can provide suggestions to guide the AI during gameplay.
   ```bash
   python3 main.py --mode suggestion
   ```
   When prompted with "Suggest:", you can type a suggestion that will be passed to the AI.

To exit the application, press `CTRL+C`.

## ⚙️ Configuration

You can customize the LLM used by modifying the `model` parameter in the `LLMmodel` class initialization:

```python
self.model = LLMmodel(host='localhost:11434', model='YOUR_PREFERRED_MODEL')