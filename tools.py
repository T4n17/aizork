#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
AIZork Tools: Retrieval-Augmented Generation (RAG) system for Zork I.
This module provides tools for retrieving relevant information from Zork walkthroughs
to assist the AI in making better decisions during gameplay.
"""

from llama_index.llms.llama_cpp import LlamaCPP
from llama_index.llms.ollama import Ollama
from llama_index.embeddings.ollama import OllamaEmbedding
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.core import SimpleDirectoryReader, VectorStoreIndex
from llama_index.core.memory import ChatMemoryBuffer

class RAG:
    """
    Retrieval-Augmented Generation (RAG) system for Zork I.
    Loads walkthrough documents, creates vector embeddings, and provides
    context-aware responses to queries about the game.
    """
    def __init__(self, llm, embed):
        """
        Initialize the RAG system with specified LLM and embedding models.
        
        Args:
            llm (str): LLM backend to use ('llama-cpp' or 'ollama')
            embed (str): Embedding model to use ('ollama' or 'huggingface')
        """
        # Initialize the language model based on the specified backend
        if llm == "llama-cpp":
            self.llm = LlamaCPP(
                model_path='./models/Qwen_Qwen2.5-7B-Instruct-GGUF_qwen2.5-7b-instruct-q2_k.gguf',
                temperature=0.1,
                context_window=4096,
                verbose=False
            )
        elif llm == "ollama":
            self.llm = Ollama(base_url="192.168.0.115:11434", model="llama3.1:8B", request_timeout=500.0)

        # Initialize the embedding model based on the specified backend
        if embed == "ollama":
            self.embed_model = OllamaEmbedding(base_url="192.168.0.115:11434", model_name="nomic-embed-text", ollama_additional_kwargs={"mirostat": 0})
        elif embed == "huggingface":
            self.embed_model = HuggingFaceEmbedding(model_name="BAAI/bge-small-en-v1.5")

        # Initialize the RAG system
        self.initRAG()

    def initRAG(self):
        """
        Initialize the RAG system by loading documents, creating embeddings,
        and setting up the chat engine with appropriate system prompt.
        """
        # Create a memory buffer for chat history
        memory = ChatMemoryBuffer.from_defaults(token_limit=3000)

        # Define the system prompt for the chat engine
        self.system_prompt = """
        You are a helpful assistant expert in ZORK I: The Great Underground Empire game.
        The user is starting a new game and you have to guide him to win.
        You are given a walkthrough guide of the game below:
        ------------------------------
        {context_str}
        ------------------------------
        Instruction: Use both previous chat history and the walkthrough guide to answer the user questions about the game:
        """

        # Load walkthrough documents from the walkthroughs directory
        self.documents = SimpleDirectoryReader('./walkthroughs').load_data()
        
        # Create vector index from documents with tree_summarize response mode
        # This mode provides better context synthesis across multiple documents
        self.index = VectorStoreIndex.from_documents(self.documents, embed_model=self.embed_model, response_mode="tree_summarize")
        
        # Initialize the chat engine with the LLM, memory, and system prompt
        self.chat_engine = self.index.as_chat_engine(llm=self.llm, memory=memory, system_prompt=self.system_prompt, chat_mode="condense_plus_context")

    def query(self, query_str):
        """
        Query the RAG system with a question about Zork.
        
        Args:
            query_str (str): Question about Zork
            
        Returns:
            Response: Response from the chat engine
        """
        return self.chat_engine.chat(query_str)



class Tools:
    """
    Tools for interacting with the RAG system.
    Provides methods for getting suggestions from the RAG system
    based on the current game context.
    """
    def __init__(self):
        """
        Initialize the Tools class with default LLM and embedding backends.
        """
        self.llm_backend = "ollama"
        self.embed_backend = "ollama"
        # Create a RAG instance with the specified backends
        self.rag = RAG(self.llm_backend, self.embed_backend)

    def ask_suggestion(self, query):
        """
        Ask the RAG system for a suggestion based on the current game context.
        
        Args:
            query (str): Current game context
            
        Returns:
            str: Suggested command from the RAG system
        """
        question = f"""
        What command should i use now, given the following context?:
        -----------------
        {query}
        -----------------

        Respond with the command that allows me to proceed correctly in the game.
        """
        return str(self.rag.query(question))

    def get_suggestion_from_rag(self, query):
        """
        Format the suggestion from the RAG system with a helpful prefix.
        
        Args:
            query (str): Current game context
            
        Returns:
            str: Formatted suggestion
        """
        suggestion = "This should help to continue the game: " + self.ask_suggestion(query)
        return suggestion