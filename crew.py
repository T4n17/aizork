from crewai import Agent, Crew, Process, Task, LLM
from crewai.project import CrewBase, agent, crew, task
from tools import ZorkWalkthroughRAGTool
import os
import yaml


@CrewBase
class WalkthroughRAGCrew():
    """Walkthrough RAG crew"""

    def __init__(self) -> None:

         # Set up configuration paths
        config_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'config')
        
        # Load agents config
        agents_config_path = os.path.join(config_dir, 'agents.yaml')
        with open(agents_config_path, 'r') as f:
            self.agents_config = yaml.safe_load(f)
            
        # Load tasks config
        tasks_config_path = os.path.join(config_dir, 'tasks.yaml')
        with open(tasks_config_path, 'r') as f:
            self.tasks_config = yaml.safe_load(f)
        
        # Initialize LLM with correct provider format for LiteLLM
        self.llm = LLM(
            model="ollama/llama3.2:3B",
            base_url="http://localhost:11434",
            config={
                "temperature": 0.1
            }
        )
        
        # Create tool instances
        self.zork_walkthrough_tool = ZorkWalkthroughRAGTool()

    @agent
    def orchestrator(self) -> Agent:
        return Agent(
            role=self.agents_config['orchestrator']['role'],
            goal=self.agents_config['orchestrator']['goal'],
            backstory=self.agents_config['orchestrator']['backstory'],
            verbose=self.agents_config['orchestrator'].get('verbose', True),
            llm=self.llm,
            allow_delegation=False
        )

    @agent
    def walkthrough_retriever(self) -> Agent:
        return Agent(
            role=self.agents_config['walkthrough_retriever']['role'],
            goal=self.agents_config['walkthrough_retriever']['goal'],
            backstory=self.agents_config['walkthrough_retriever']['backstory'],
            verbose=self.agents_config['walkthrough_retriever'].get('verbose', True),
            tools=[self.zork_walkthrough_tool],
            llm=self.llm,
            max_iter=1,
            max_retry_limit=1,
            allow_delegation=False
        )

    @agent
    def command_finder(self) -> Agent:
        return Agent(
            role=self.agents_config['command_finder']['role'],
            goal=self.agents_config['command_finder']['goal'],
            backstory=self.agents_config['command_finder']['backstory'],
            verbose=self.agents_config['command_finder'].get('verbose', True),
            llm=self.llm,
            max_iter=1,
            max_retry_limit=1,
            allow_delegation=False
        )

    @task
    def extract_level_task(self, game_state: str = "") -> Task:
        return Task(
            description=self.tasks_config['extract_level_task']['description'],
            expected_output=self.tasks_config['extract_level_task']['expected_output'],
            agent=self.orchestrator(),
            async_execution=self.tasks_config['extract_level_task'].get('async_execution', False)
        )

    @task
    def retrieve_walkthrough_task(self, level_name: str = "") -> Task:
        return Task(
            description=self.tasks_config['retrieve_walkthrough_task']['description'],
            expected_output=self.tasks_config['retrieve_walkthrough_task']['expected_output'],
            agent=self.walkthrough_retriever(),
            async_execution=self.tasks_config['retrieve_walkthrough_task'].get('async_execution', False)
        )

    @task
    def integrate_solutions_task(self, walkthrough: str = "", level_name: str = "") -> Task:
        return Task(
            description=self.tasks_config['integrate_solutions_task']['description'],
            expected_output=self.tasks_config['integrate_solutions_task']['expected_output'],
            agent=self.orchestrator(),
            async_execution=self.tasks_config['integrate_solutions_task'].get('async_execution', False)
        )

    @task
    def command_finder_task(self, walkthrough: str = "", level_name: str = "") -> Task:
        return Task(
            description=self.tasks_config['command_finder_task']['description'],
            expected_output=self.tasks_config['command_finder_task']['expected_output'],
            agent=self.command_finder(),
            async_execution=self.tasks_config['command_finder_task'].get('async_execution', False)
        )

    @crew
    def crew(self) -> Crew:

        extract_task = self.extract_level_task()
        
        walkthrough_task = self.retrieve_walkthrough_task()
        walkthrough_task.context = [extract_task]
        
        integrate_task = self.integrate_solutions_task()
        integrate_task.context = [walkthrough_task, extract_task]
        
        command_finder_task = self.command_finder_task()
        command_finder_task.context = [integrate_task]
        
        # Define the task list with explicit ordering
        task_list = [
            extract_task,
            walkthrough_task,
            integrate_task,
            command_finder_task,
        ]
        
        return Crew(
            agents=self.agents,
            tasks=task_list,
            process=Process.sequential,
            verbose=True,
            share_tools=False
        )
