#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
AIZork: An AI-powered player for the classic text adventure game Zork I.
This module contains the main application logic for running different game modes
and handling the interaction between AI models and the Zork game.
"""

import pty
import os
import time
import subprocess
import ollama
import pydantic
import argparse
from colorama import Fore, Style
from llama_cpp import Llama
from tools import Tools

# System prompt that guides the AI on how to play Zork
SYSTEM_CONTEXT = """
    You have to play ZORK I: The Great Underground Empire game.
    You are given the contextual information of the game (about environment and actions), and you have respond with the command to be executed.
    You have to explore the game and try to win reaching the end.
    Occasionally, the user will give you suggestions to proceed in the right direction or take the right action, after a proper statement "Suggestion :".
    Examples: "There is a mailbox in front of you." -> "open mailbox"
    "It's dark in here. You may be eaten by a grue." -> "turn on lamp"
    "Suggestion : You should try to reach the south of the house" -> "go south"
    """

class CommandSchema(pydantic.BaseModel):
    """
    Pydantic schema for structured command output from the AI.
    Ensures that the AI response is properly formatted as a command.
    """
    command: str

class LlamaCppModel:
    """
    Wrapper for local LLM inference using llama-cpp-python.
    Handles chat history, system context, and response generation.
    """
    def __init__(self, model_path='./models/Qwen_Qwen2.5-7B-Instruct-GGUF_qwen2.5-7b-instruct-q2_k.gguf'):
        """
        Initialize the LlamaCpp model with the specified model path.
        
        Args:
            model_path (str): Path to the GGUF model file
        """
        llm = Llama(
            model_path=model_path,
            chat_format="chatml",  # Use ChatML format for structured chat
            n_ctx=4096,  # Context window size
        )

        self.model = llm
        self.messages = []  # Chat history
        self.set_system_context()
        
    def set_system_context(self, system_context=SYSTEM_CONTEXT):
        """
        Set the system context/prompt for the model.
        
        Args:
            system_context (str): System instructions for the model
        """
        self.messages.append({
            'role': 'system', 
            'content': system_context
        })
    
    def process_user_input(self, user_input):
        """
        Add user input to the chat history.
        
        Args:
            user_input (str): Game context or user suggestion
        """
        self.messages.append({
            'role': 'user', 
            'content': user_input
        })
    
    def get_ai_response(self, format_schema):
        """
        Generate a response from the AI model using the chat history.
        
        Args:
            format_schema (dict): JSON schema for structured output
            
        Returns:
            str: JSON-formatted response from the model
        """
        response = self.model.create_chat_completion(
            messages=self.messages,
            response_format={
                "type": "json_object",
                "schema": format_schema
            },
            temperature=0.1,  # Low temperature for more deterministic outputs
            max_tokens=256
        )
        json_response = response["choices"][0]["message"]["content"]
        return json_response

class OllamaModel:
    """
    Wrapper for Ollama-based LLM inference.
    Handles chat history, system context, and response generation.
    """
    def __init__(self, host='192.168.0.115:11434', model='llama3.1:8B'):
        """
        Initialize the Ollama model with the specified host and model.
        
        Args:
            host (str): Ollama API host address
            model (str): Name of the model to use
        """
        self.client = ollama.Client(host=host)
        self.model = model
        self.messages = []  # Chat history
        self.set_system_context()
        
    def set_system_context(self, system_context=SYSTEM_CONTEXT):
        """
        Set the system context/prompt for the model.
        
        Args:
            system_context (str): System instructions for the model
        """
        self.messages.append({
            'role': 'system', 
            'content': system_context
        })
    
    def process_user_input(self, user_input):
        """
        Add user input to the chat history.
        
        Args:
            user_input (str): Game context or user suggestion
        """
        self.messages.append({
            'role': 'user', 
            'content': user_input
        })
    
    def get_ai_response(self, format_schema):
        """
        Generate a response from the Ollama model using the chat history.
        
        Args:
            format_schema (dict): JSON schema for structured output
            
        Returns:
            str: JSON-formatted response from the model
        """
        response = self.client.chat(
            model=self.model, 
            messages=self.messages,
            format=format_schema,
            stream=False
        )
        return response.message.content

class AIZork:
    """
    Main class for handling the interaction between AI models and the Zork game.
    Sets up the pseudo-terminal, processes game output, and sends AI commands.
    """
    def __init__(self, model_type):
        """
        Initialize AIZork with the specified model type.
        
        Args:
            model_type (str): Type of model to use ('ollama' or 'llama-cpp')
        """
        if model_type == "ollama":
            self.model = OllamaModel()
        elif model_type == "llama-cpp":
            self.model = LlamaCppModel()
        self.process = None

    def init_process(self):
        """
        Initialize the pseudo-terminal and start the Zork game process.
        Uses dosemu to run the DOS version of Zork I.
        """
        master, slave = pty.openpty()
        self.process = subprocess.Popen('/usr/bin/dosemu -K ./ZORK -E "_ZORK1" -dumb', 
                                    shell=True, 
                                    stdin=slave, 
                                    stdout=slave, 
                                    stderr=subprocess.PIPE, 
                                    close_fds=True)
        os.close(slave)
        self.master = master

    def send_command(self, command):
        """
        Send a command to the Zork game.
        
        Args:
            command (str): Command to send to the game
        """
        os.write(self.master, (command + '\n').encode())

    def read_text(self):
        """
        Read the current game output from the pseudo-terminal.
        
        Returns:
            str: Current game output/context
        """
        return os.read(self.master, 2048).decode()

    def process_command(self, context):
        """
        Process the game context and generate a command using the AI model.
        
        Args:
            context (str): Current game output/context
            
        Returns:
            str: Command generated by the AI
        """
        self.model.process_user_input(context)
        response = self.model.get_ai_response(CommandSchema.model_json_schema())
        return CommandSchema.model_validate_json(response).command
    
    def suggest_command(self):
        """
        Get a command suggestion from the user and add it to the model's context.
        """
        suggestion = input("Suggest: ")
        if suggestion:
            self.model.process_user_input("Suggestion:"+ suggestion)

    def close(self):
        """
        Terminate the game process and clean up resources.
        """
        self.process.terminate()

class GameModes:
    """
    Class containing different game modes for AIZork.
    Includes autoplay, autoplay with RAG assistance, and suggestion mode.
    """
    def __init__(self, model_type):
        """
        Initialize GameModes with the specified model type.
        
        Args:
            model_type (str): Type of model to use ('ollama' or 'llama-cpp')
        """
        self.aizork = AIZork(model_type)

    def autoplay(self):
        """
        Run the game in autoplay mode where the AI plays completely autonomously.
        """
        self.aizork.init_process()
        try:
            while True:
                time.sleep(2)  # Wait for game output
                context = self.aizork.read_text()
                print(context)
                command = self.aizork.process_command(context)
                print(f"{Fore.RED}{command}{Style.RESET_ALL}")  # Display command in red
                self.aizork.send_command(command)
                self.aizork.send_command("\n")
        except KeyboardInterrupt:
            self.aizork.close()
        except Exception as e:
            print(f"Error: {e}")
            self.aizork.close()

    def autoplay_with_rag(self):
        """
        Run the game in autoplay mode with RAG (Retrieval-Augmented Generation) assistance.
        Uses a walkthrough guide to help the AI make better decisions.
        """
        self.aizork.init_process()
        tools = Tools()  # Initialize RAG tools
        try:
            while True:
                time.sleep(2)  # Wait for game output
                context = self.aizork.read_text()
                print(f"{context}")
                suggestion = tools.get_suggestion_from_rag(context)  # Get suggestion from RAG
                print(f"{Fore.GREEN}{suggestion}{Style.RESET_ALL}")  # Display suggestion in green
                command = self.aizork.process_command(context + "\n" + suggestion)
                print(f"{Fore.RED}{command}{Style.RESET_ALL}")  # Display command in red
                self.aizork.send_command(command)
                self.aizork.send_command("\n")
        except KeyboardInterrupt:
            self.aizork.close()
        except Exception as e:
            print(f"Error: {e}")
            self.aizork.close()
            
    def suggestion(self):
        """
        Run the game in suggestion mode where the user can provide suggestions to the AI.
        """
        self.aizork.init_process()
        try:
            while True:
                time.sleep(2)  # Wait for game output
                context = self.aizork.read_text()
                print(context)
                self.aizork.suggest_command()  # Get suggestion from user
                command = self.aizork.process_command(context)
                print(f"{Fore.RED}{command}{Style.RESET_ALL}")  # Display command in red
                self.aizork.send_command(command)
                self.aizork.send_command("\n")
        except KeyboardInterrupt:
            self.aizork.close()
        except Exception as e:
            print(f"Error: {e}")
            self.aizork.close()
        
if __name__ == "__main__":
    # Parse command-line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", type=str, default="autoplay", help="Choose the game mode (autoplay or suggestion)")
    parser.add_argument("--model-type", type=str, default="ollama", help="Choose the model type (ollama or llama-cpp)")
    parser.add_argument("--rag-helper", action=argparse.BooleanOptionalAction, default=False, help="Enable RAG helper")
    args = parser.parse_args()
    
    # Initialize game with specified model type
    game = GameModes(args.model_type)
    
    # Run the appropriate game mode
    if args.rag_helper:
        game.autoplay_with_rag()
    else:
        if args.mode == "autoplay":
            game.autoplay()
        elif args.mode == "suggestion":
            game.suggestion()
