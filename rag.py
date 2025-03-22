#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
AIZork RAG: Retrieval-Augmented Generation (RAG) system for Zork I.
This module provides tools for retrieving relevant information from Zork walkthroughs
to assist the AI in making better decisions during gameplay.

The RAG system uses ChromaDB to store and retrieve walkthrough documents, with intelligent
chunking strategies for different document types to ensure high-quality retrieval results.
"""

import chromadb
import os
import uuid
import re
from chromadb.config import Settings

class Document:
    """
    Simple document class for representing text documents with metadata.
    Replaces the need for external document handling libraries.
    """
    def __init__(self, text, metadata=None):
        """
        Initialize a document with text content and optional metadata.
        
        Args:
            text (str): The document text content
            metadata (dict, optional): Metadata associated with the document
        """
        self.text = text
        self.metadata = metadata or {}

class ChromaDB:
    """
    ChromaDB integration for Zork I walkthrough documents.
    Handles loading, processing, chunking, and storing documents in ChromaDB.
    """
    def __init__(self, persist_directory="./chroma_db"):
        """
        Initialize the ChromaDB client.
        
        Args:
            persist_directory (str): Directory to persist the ChromaDB data
        """
        self.persist_directory = persist_directory
        self.walkthrough_collection_name = "zork_walkthroughs"
        
        # Create the ChromaDB client
        self.chroma_client = chromadb.Client(Settings(
            persist_directory=persist_directory,
            anonymized_telemetry=False
        ))
        
        # Create the walkthrough collection if it doesn't exist
        try:
            collections = self.chroma_client.list_collections()
            collection_names = [collection.name for collection in collections]
            
            if self.walkthrough_collection_name not in collection_names:
                self.chroma_client.create_collection(name=self.walkthrough_collection_name)
        except Exception as e:
            print(f"Error checking collection existence: {e}")
            
        self.save_walkthroughs_to_chroma()

    def save_walkthroughs_to_chroma(self, directory_path="./walkthroughs", overwrite=False):
        """
        Load walkthrough documents and save them to ChromaDB.
        
        Args:
            directory_path (str): Path to the directory containing walkthrough documents
            overwrite (bool): Whether to overwrite existing documents
        """
        # Load walkthrough documents
        documents = self.load_walkthrough_documents(directory_path)
        
        if not documents:
            print(f"No walkthrough documents found in {directory_path}")
            return
        
        # Process documents for ChromaDB
        chroma_data = self.process_documents_for_chroma(documents)
        
        # Get or create the collection
        collection = self.chroma_client.get_or_create_collection(name=self.walkthrough_collection_name)
        
        # If overwrite, delete existing documents
        if overwrite:
            collection.delete()
            collection = self.chroma_client.create_collection(name=self.walkthrough_collection_name)
        
        # Add documents to the collection
        collection.add(
            ids=chroma_data["ids"],
            documents=chroma_data["documents"],
            metadatas=chroma_data["metadatas"]
        )
        
        print(f"Successfully saved {len(documents)} walkthrough documents to ChromaDB collection '{self.walkthrough_collection_name}'")

    def save_data_to_chroma(self, data, collection_name):
        """
        Save data to a Chroma collection.
        
        Args:
            data (dict): Dictionary with ids, documents, metadatas for ChromaDB
            collection_name (str): Name of the collection
        """
        collection = self.chroma_client.get_or_create_collection(name=collection_name)
        collection.add(
            ids=data["ids"],
            documents=data["documents"],
            metadatas=data["metadatas"]
        )

    def load_walkthrough_documents(self, directory_path="./walkthroughs"):
        """
        Load walkthrough documents from a directory.
        
        Args:
            directory_path (str): Path to the directory containing walkthrough documents
            
        Returns:
            List[Document]: List of loaded documents
        """
        if not os.path.exists(directory_path):
            raise FileNotFoundError(f"Directory {directory_path} does not exist")
        
        documents = []
        
        # Get all files in the directory
        for filename in os.listdir(directory_path):
            file_path = os.path.join(directory_path, filename)
            
            # Skip directories
            if os.path.isdir(file_path):
                continue
            
            # Read the file
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    text = f.read()
                
                # Create a document
                doc = Document(
                    text=text,
                    metadata={
                        "filename": filename,
                        "created_at": os.path.getctime(file_path),
                        "source": "walkthrough"
                    }
                )
                
                documents.append(doc)
            except Exception as e:
                print(f"Error loading document {file_path}: {e}")
        
        return documents
    
    def process_documents_for_chroma(self, documents):
        """
        Process documents for storage in ChromaDB.
        Splits documents into smaller chunks for better retrieval.
        
        Args:
            documents (List[Document]): List of documents to process
        
        Returns:
            Dict[str, List[Any]]: Dictionary with ids, documents, metadatas for ChromaDB
        """
        ids = []
        texts = []
        metadatas = []
        
        for doc in documents:
            # Split document into smaller chunks for better retrieval
            chunks = self.split_document_into_chunks(doc)
            
            for i, chunk in enumerate(chunks):
                doc_id = str(uuid.uuid4())
                ids.append(doc_id)
                texts.append(chunk)
                
                # Extract metadata from document
                metadata = {
                    "filename": doc.metadata.get("filename", "unknown"),
                    "source": "walkthrough",
                    "chunk_index": i,
                    "created_at": doc.metadata.get("created_at", ""),
                }
                metadatas.append(metadata)
        
        return {
            "ids": ids,
            "documents": texts,
            "metadatas": metadatas
        }
    
    def split_document_into_chunks(self, doc):
        """
        Split a document into smaller chunks for better retrieval.
        Uses different strategies based on document type.
        
        Args:
            doc (Document): Document to split
            
        Returns:
            List[str]: List of text chunks
        """
        # For markdown files, try to split by headers
        if doc.metadata.get("filename", "").endswith((".md", ".markdown")):
            return self.split_markdown_by_sections(doc.text)
        
        # For text files, split by lines with a reasonable chunk size
        return self.split_text_by_chunks(doc.text)
    
    def split_markdown_by_sections(self, text):
        """
        Split markdown text by sections (headers).
        This preserves the logical structure of the document.
        
        Args:
            text (str): Markdown text
            
        Returns:
            List[str]: List of sections
        """
        # Split by headers (## or ###)
        header_pattern = re.compile(r'^#{1,3}\s+', re.MULTILINE)
        
        # Find all header positions
        header_matches = list(header_pattern.finditer(text))
        
        if not header_matches:
            # If no headers found, fall back to chunk-based splitting
            return self.split_text_by_chunks(text)
        
        # Extract sections based on header positions
        sections = []
        
        # Add the document title or introduction if it exists before the first header
        if header_matches[0].start() > 0:
            intro = text[:header_matches[0].start()].strip()
            if intro:
                sections.append(intro)
        
        for i, match in enumerate(header_matches):
            start_pos = match.start()
            
            # If this is the last header, the section extends to the end of the text
            if i == len(header_matches) - 1:
                section_text = text[start_pos:]
            else:
                # Otherwise, the section extends to the start of the next header
                end_pos = header_matches[i + 1].start()
                section_text = text[start_pos:end_pos]
            
            sections.append(section_text.strip())
        
        return sections
    
    def split_text_by_chunks(self, text, chunk_size=1000, overlap=200):
        """
        Split text into overlapping chunks of approximately equal size.
        Tries to find natural break points like paragraph breaks or sentences.
        
        Args:
            text (str): Text to split
            chunk_size (int): Target size of each chunk
            overlap (int): Number of characters to overlap between chunks
            
        Returns:
            List[str]: List of text chunks
        """
        # If text is shorter than chunk_size, return it as is
        if len(text) <= chunk_size:
            return [text]
        
        chunks = []
        start = 0
        
        while start < len(text):
            # Calculate end position for this chunk
            end = start + chunk_size
            
            # If we're at the end of the text, just take the rest
            if end >= len(text):
                chunks.append(text[start:])
                break
            
            # Try to find a good break point (newline or period)
            break_point = text.rfind("\n\n", start + chunk_size // 2, end)
            
            if break_point == -1:
                # If no paragraph break, try to find a sentence break
                break_point = text.rfind(". ", start + chunk_size // 2, end)
            
            if break_point == -1:
                # If no good break point found, just use the chunk size
                break_point = end
            else:
                # Include the period or newline in this chunk
                break_point += 1
            
            # Add the chunk to our list
            chunks.append(text[start:break_point])
            
            # Start the next chunk with some overlap
            start = max(start, break_point - overlap)
        
        return chunks
    
    def query_walkthrough_collection(self, query_text, n_results=4):
        """
        Query the walkthrough collection with the given text.
        
        Args:
            query_text (str): Text to query with
            n_results (int): Number of results to return
            
        Returns:
            List[Dict]: List of results
        """
        try:
            # Get the collection
            collection = self.chroma_client.get_or_create_collection(name=self.walkthrough_collection_name)
            
            # Query the collection
            results = collection.query(
                query_texts=[query_text],
                n_results=n_results
            )
            
            # Format the results
            formatted_results = []
            for i in range(len(results["ids"][0])):
                formatted_results.append({
                    "id": results["ids"][0][i],
                    "text": results["documents"][0][i],
                    "metadata": results["metadatas"][0][i],
                    "distance": results["distances"][0][i] if "distances" in results else 0.0
                })
            
            # Sort by distance (lower is better)
            formatted_results.sort(key=lambda x: x["distance"])
            
            return formatted_results
        except Exception as e:
            print(f"Error querying walkthrough collection: {e}")
            return []
    
    def _preprocess_query(self, query_text):
        """
        Simple pass-through for the query text.
        
        Args:
            query_text (str): Original query text
            
        Returns:
            str: The same query text
        """
        return query_text

class RAG:
    """
    Retrieval-Augmented Generation (RAG) system for Zork I.
    Loads walkthrough documents, creates vector embeddings, and provides
    context-aware responses to queries about the game.
    """
    def __init__(self):
        """
        Initialize the RAG system with ChromaDB for document retrieval.
        """
        self.chromadb = ChromaDB()

    def query_chromadb(self, query_str):
        """
        Query the ChromaDB for relevant walkthrough information.
        
        Args:
            query_str (str): Query string representing the current game state
            
        Returns:
            List[Dict]: List of relevant document chunks
        """
        return self.chromadb.query_walkthrough_collection(query_str)

    def get_suggestion_from_rag(self, query_str):
        """
        Get suggestions from the RAG system based on the query.
        Formats the results into a readable format for the user.
        
        Args:
            query_str (str): Query string representing the current game state
            
        Returns:
            str: Formatted suggestion
        """
        results = self.query_chromadb(query_str)
        
        if not results:
            return "This should help to continue the game: No relevant suggestions found."
        
        # Format the results into a clean, readable format
        formatted_results = []
        seen_content = set()
        
        # Process each result
        for result in results:
            text = result["text"]
            
            # Skip if we've seen similar content
            content_signature = text[:50]
            if content_signature in seen_content:
                continue
                
            seen_content.add(content_signature)
            
            # Truncate if too long
            if len(text) > 500:
                text = text[:497] + "..."
                
            formatted_results.append(text)
            
            # Limit to 2 results
            if len(formatted_results) >= 2:
                break
        
        formatted_text = "\n\n".join(formatted_results)
        
        suggestion = f"This should help to continue the game:\n\n{formatted_text}"
        return suggestion

if __name__ == "__main__":
    # Test the RAG system with a sample query
    rag = RAG()
    print(rag.get_suggestion_from_rag("There is a small mailbox in front of you."))