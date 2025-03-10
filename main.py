import pty
import os
import time
import subprocess
import ollama
import pydantic

class CommandSchema(pydantic.BaseModel):
    command: str

class LLMmodel:

    SYSTEM_CONTEXT = """
    You have to play ZORK I: The Great Underground Empire game.
    You are given the contextual information of the game (about environment and actions), and you have respond with the command to be executed.
    You have to explore the game and try to win reaching the end.
    Examples: "There is a mailbox in front of you." -> "open mailbox"
    "It's dark in here. You may be eaten by a grue." -> "turn on lamp"
    """

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
        return self.client.chat(
            model=self.model, 
            messages=self.messages,
            format=format_schema,
            stream=False
        )

class AIZork:
    def __init__(self):
        self.name = "AIZork"
        self.version = "0.1.0"
        self.author = "Tani"
        self.model = LLMmodel()
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
        return CommandSchema.model_validate_json(response.message.content).command

    def close(self):
        self.process.terminate()

def main():
    aizork = AIZork()
    aizork.init_process()
    try:
        while True:
            time.sleep(2)
            context = aizork.read_text()
            print(context)
            command = aizork.process_command(context)
            aizork.send_command(command)
            aizork.send_command("\n")
    except KeyboardInterrupt:
        aizork.close()
    except Exception as e:
        print(f"Error: {e}")
        aizork.close()
        
if __name__ == "__main__":
    main()
    
