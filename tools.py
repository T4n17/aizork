from typing import Optional
from pydantic import BaseModel, Field
from rag import RAG
from crewai.tools import BaseTool

class ZorkWalkthroughRAGToolInput(BaseModel):
    """Input schema for ZorkWalkthroughRAGTool."""
    query: str = Field(..., description="The query to search for in the Zork walkthroughs")
    level_name: Optional[str] = Field(None, description="The level name to filter by")

class ZorkWalkthroughRAGTool(BaseTool):
    """Tool for retrieving information from the Zork walkthroughs using RAG techniques"""
    name: str = "zork_walkthrough_rag"
    description: str = "Tool for retrieving information from the Zork walkthroughs using RAG techniques"
    args_schema = ZorkWalkthroughRAGToolInput

    def _run(self, **kwargs) -> str:
        try:
            # Extract query and level_name from kwargs
            query = kwargs.get('query', '')
            level_name = kwargs.get('level_name', None)
            
            # Handle case where inputs might be dictionaries
            if isinstance(query, dict) and 'description' in query:
                query = query.get('description', '')
            
            if isinstance(level_name, dict) and 'description' in level_name:
                level_name = level_name.get('description', '')
                
            # Ensure we have string values
            query = str(query) if query else ""
            level_name = str(level_name) if level_name else None
            
            return RAG().get_suggestion_from_rag(query, level_name)
        except Exception as e:
            return f"Error querying Zork walkthroughs: {str(e)}"
    
    def _arun(self, **kwargs):
        raise NotImplementedError("Async version not implemented")
