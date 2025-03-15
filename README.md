# 🎮 AIZork: Let Your LLM Play Zork!

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.8%2B-blue" alt="Python 3.8+">
  <img src="https://img.shields.io/badge/Game-Zork%20I-yellow" alt="Game: Zork I">
  <img src="https://img.shields.io/badge/RAG-Enhanced-green" alt="RAG Enhanced">
</p>

## 📖 Description

AIZork is a project that lets Large Language Models (LLMs) play the classic text adventure game Zork I: The Great Underground Empire. Watch as AI navigates the underground empire, solves puzzles, and attempts to win the game through natural language commands.

This project demonstrates how modern AI can interact with classic interactive fiction games through a pseudo-terminal interface, with optional Retrieval-Augmented Generation (RAG) assistance.

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
- 📚 Enhanced RAG system with multiple document formats for better gameplay assistance

## 🔧 Prerequisites

- **Python 3.8+** - For running the main application
- **[Ollama](https://ollama.ai/)** - For Ollama-based LLM inference
- **[Dosemu2](https://github.com/dosemu2/dosemu2)** - DOS emulator to run Zork
- **Zork I: The Great Underground Empire** - DOS version of the game

### Python Dependencies

- **pydantic** - For data validation and structured output
- **llama-cpp-python** - For local model inference (optional)
- **colorama** - For colored terminal output
- **llama-index** - For the RAG system components:
  - llama-index-core - Core functionality
  - llama-index-llms-ollama - Ollama integration
  - llama-index-llms-llama-cpp - Local model integration
  - llama-index-embeddings-ollama - Ollama embeddings
  - llama-index-embeddings-huggingface - HuggingFace embeddings
- **sentence-transformers** - For embedding models (when using HuggingFace)

All dependencies can be installed via the provided `requirements.txt` file.

## 📁 Directory Structure

```
.
├── ZORK/           # Directory containing Zork game files
├── models/         # Directory for storing local GGUF models (for llama-cpp-python)
├── walkthroughs/   # Directory containing Zork walkthrough documents for RAG
│   ├── zork_walkthrough.md           # Markdown-based walkthrough
│   ├── zork_command_sequence.txt     # Linear command sequence
│   └── zork_location_guide.md        # Location-based reference guide
├── main.py         # Main application script
├── tools.py        # RAG system implementation
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

3. **RAG Helper**:
   - Enable the RAG helper to assist the AI with walkthrough information:
     ```bash
     python3 main.py --rag-helper
     ```
     This uses multiple document formats (markdown walkthrough, command sequence, and location guide) to provide context-aware suggestions to the AI.

## 📚 RAG System

The RAG (Retrieval-Augmented Generation) system enhances the AI's gameplay by providing context-aware suggestions based on a comprehensive Zork walkthrough. The system uses:

1. **Multiple Document Formats**:
   - **Markdown Walkthrough** (`zork_walkthrough.md`): A structured guide with sections and commands
   - **Command Sequence** (`zork_command_sequence.txt`): A linear list of commands to complete the game
   - **Location Guide** (`zork_location_guide.md`): A reference organized by game locations

2. **Tree Summarize Response Mode**:
   - Synthesizes information across multiple documents
   - Provides comprehensive answers by combining relevant chunks

3. **Embedding Model**:
   - Uses Ollama's `nomic-embed-text` model for document embedding
   - Creates a vector index for efficient retrieval

The RAG system helps the AI navigate complex areas, solve puzzles, and make better decisions during gameplay.