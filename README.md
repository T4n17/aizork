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

- 🤖 Supports multiple LLM backends:
  - Ollama with Llama 3.1:8B (default)
  - Local models via llama-cpp-python
- 🎮 Fully automated gameplay through AI decision-making
- 🔄 Real-time interaction with the Zork game environment
- 📊 Observe how AI interprets game context and generates commands
- 💬 Ability to provide suggestions to guide the AI during gameplay
- 🧩 Structured output using Pydantic for reliable command generation

## 🔧 Prerequisites

- **Python 3.8+** - For running the main application
- **[Ollama](https://ollama.ai/)** (optional) - For Ollama-based LLM inference
- **llama-cpp-python** (optional) - For local model inference
- **Pydantic** - For data validation and structured output
- **[Dosemu2](https://github.com/dosemu2/dosemu2)** - DOS emulator to run Zork
- **Zork I: The Great Underground Empire** - DOS version of the game

## 📁 Directory Structure

```
.
├── ZORK/           # Directory containing Zork game files
├── models/         # Directory for storing local GGUF models (for llama-cpp-python)
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

5. Choose your LLM backend:
   - For Ollama:
     ```bash
     ollama pull llama3.1:8B
     ```
   - For llama-cpp-python:
     Place your GGUF model files in the `models/` directory

## 🎮 Usage

Start the AIZork application:

```bash
python3 main.py
```

The AI will automatically begin playing Zork using the default Ollama backend. You can observe its decisions and gameplay in real-time.

### Game Modes and Model Types

AIZork supports different game modes and model backends:

1. **Game Modes**:
   - **Autoplay Mode** (default): The AI plays the game completely autonomously.
     ```bash
     python3 main.py --mode autoplay
     ```
   - **Suggestion Mode**: You can provide suggestions to guide the AI during gameplay.
     ```bash
     python3 main.py --mode suggestion
     ```
     When prompted with "Suggest:", you can type a suggestion that will be passed to the AI.

2. **Model Types**:
   - **Ollama** (default): Uses Ollama for LLM inference.
     ```bash
     python3 main.py --model-type ollama
     ```
   - **llama-cpp-python**: Uses local GGUF models for inference.
     ```bash
     python3 main.py --model-type llama-cpp
     ```

Combined example:
```bash
python3 main.py --mode suggestion --model-type llama-cpp
```

To exit the application, press `CTRL+C`.

## ⚙️ Configuration

### Ollama Model Configuration

You can customize the Ollama model by modifying the parameters in the `OllamaModel` class initialization:

```python
self.model = OllamaModel(host='localhost:11434', model='YOUR_PREFERRED_MODEL')
```

### llama-cpp-python Model Configuration

You can customize the local model by modifying the parameters in the `LlamaCppModel` class initialization:

```python
self.model = LlamaCppModel(model_path='./models/YOUR_MODEL_FILE.gguf')
```

The model should be in GGUF format and placed in the `models/` directory.