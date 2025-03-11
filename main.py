import pty
import os
import time
import subprocess
import ollama
import pydantic
import argparse
from llama_cpp import Llama

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
    command: str

class LlamaCppModel:
    def __init__(self, model_path='./models/Qwen_Qwen2.5-7B-Instruct-GGUF_qwen2.5-7b-instruct-q2_k.gguf'):
        
        llm = Llama(
            model_path=model_path,
            chat_format="chatml",
            n_ctx=4096,
        )

        self.model = llm
        self.messages = []
        self.set_system_context()
        
    def set_system_context(self, system_context=SYSTEM_CONTEXT):

        self.messages.append({
            'role': 'system', 
            'content': system_context
        })
    
    def process_user_input(self, user_input):

        self.messages.append({
            'role': 'user', 
            'content': user_input
        })
    
    def get_ai_response(self, format_schema):
        response =self.model.create_chat_completion(
            messages=self.messages,
            response_format={
                "type": "json_object",
                "schema": format_schema
            },
            temperature=0.1,
            max_tokens=256
        )
        json_response = response["choices"][0]["message"]["content"]
        return json_response

class OllamaModel:

    def __init__(self, host='localhost:11434', model='llama3.1:8B'):

        self.client = ollama.Client(host=host)
        self.model = model
        self.messages = []
        self.set_system_context()
        
    def set_system_context(self, system_context=SYSTEM_CONTEXT):

        self.messages.append({
            'role': 'system', 
            'content': system_context
        })
    
    def process_user_input(self, user_input):

        self.messages.append({
            'role': 'user', 
            'content': user_input
        })
    
    def get_ai_response(self, format_schema):
        response = self.client.chat(
            model=self.model, 
            messages=self.messages,
            format=format_schema,
            stream=False
        )
        return response.message.content

class AIZork:
    def __init__(self, model_type):
        if model_type == "ollama":
            self.model = OllamaModel()
        elif model_type == "llama-cpp":
            self.model = LlamaCppModel()
        self.process = None

    def init_process(self):
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
        os.write(self.master, (command + '\n').encode())

    def read_text(self):
        return os.read(self.master, 2048).decode()

    def process_command(self, context):
        self.model.process_user_input(context)
        response = self.model.get_ai_response(CommandSchema.model_json_schema())
        return CommandSchema.model_validate_json(response).command
    
    def suggest_command(self):
        suggestion = input("Suggest: ")
        if suggestion:
            self.model.process_user_input("Suggestion:"+ suggestion)

    def close(self):
        self.process.terminate()

class GameModes:
    def __init__(self, model_type):
        self.aizork = AIZork(model_type)

    def autoplay(self):
        self.aizork.init_process()
        try:
            while True:
                time.sleep(2)
                context = self.aizork.read_text()
                print(context)
                command = self.aizork.process_command(context)
                self.aizork.send_command(command)
                self.aizork.send_command("\n")
        except KeyboardInterrupt:
            self.aizork.close()
        except Exception as e:
            print(f"Error: {e}")
            self.aizork.close()
            
    def suggestion(self):
        self.aizork.init_process()
        try:
            while True:
                time.sleep(2)
                context = self.aizork.read_text()
                print(context)
                self.aizork.suggest_command()
                command = self.aizork.process_command(context)
                self.aizork.send_command(command)
                self.aizork.send_command("\n")
        except KeyboardInterrupt:
            self.aizork.close()
        except Exception as e:
            print(f"Error: {e}")
            self.aizork.close()
        
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", type=str, default="autoplay", help="Choose the game mode (autoplay or suggestion)")
    parser.add_argument("--model-type", type=str, default="ollama", help="Choose the model type (ollama or llama-cpp)")
    args = parser.parse_args()
    game = GameModes(args.model_type)
    if args.mode == "autoplay":
        game.autoplay()
    elif args.mode == "suggestion":
        game.suggestion()
