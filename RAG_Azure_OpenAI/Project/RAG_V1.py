"""This module initializes and runs the Retrieval-Augmented Generation (RAG) system."""

import os
import sys
import threading
import time
import openai
import requests
from azure.identity import DefaultAzureCredential
from langchain_openai import AzureOpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_openai import AzureChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import RetrievalQA
from langchain.memory import ConversationBufferMemory
from flask import Flask, request, render_template_string, jsonify
from langchain_community.callbacks.manager import get_openai_callback

def set_openai_credentials():
    """
    Set OpenAI API credentials.

    This function initializes the OpenAI API credentials using Azure authentication.
    """
    credential = DefaultAzureCredential(exclude_managed_identity_credential=True)
    openai.api_type = 'azuread'
    openai.api_version = "2024-02-01" # change this to your endpoint
    openai.api_base = "https://obs-eu-swe-openai.openai.azure.com/" # change this to your endpoint
    openai.api_key = os.environ["AZURE_OPENAI_API_KEY"]
    os.environ["AZURE_OPENAI_API_KEY"] = openai.api_key
    os.environ["AZURE_OPENAI_ENDPOINT"] = openai.api_base

def initialize_embedding():
    """
    Initialize the embedding model using AzureOpenAIEmbeddings.

    Returns:
        AzureOpenAIEmbeddings: An instance of the AzureOpenAIEmbeddings class.
    """
    # Initialize AzureOpenAIEmbeddings with specific azure_deployment and openai_api_version
    return AzureOpenAIEmbeddings(
        azure_deployment="text-embedding-ada-002",
        openai_api_version=openai.api_version
    )

def initialize_document_store(embedding, persist_directory):
    """
    Initialize the document store using the embedding and persist directory.

    Args:
        embedding (AzureOpenAIEmbeddings): An instance of the AzureOpenAIEmbeddings class.
        persist_directory (str): The directory where the document store will persist its data.

    Returns:
        Chroma: An instance of the Chroma document store.
    """
    # Initialize the document store using the embedding and persist directory
    return Chroma(
        embedding_function=embedding,  # The embedding function to use
        persist_directory=persist_directory  # The directory to persist the data to
    )

def initialize_retriever(document_store):
    """
    Initialize the retriever using the document store and the query results number.

    Args:
        document_store (Chroma): An instance of the Chroma document store.

    Returns:
        Retriever: An instance of the retriever.
    """
    # Initialize the retriever using the document store and the query results number
    return document_store.as_retriever(
        return_source_documents=True,
        search_type="mmr",
        search_kwargs={"k": 3, "fetch_k": 20}
    )

def initialize_llm():
    """
    Initialize the AzureChatOpenAI model with the specified parameters.

    Returns:
        AzureChatOpenAI: An instance of the AzureChatOpenAI model.
    """
    return AzureChatOpenAI(
        azure_deployment="gpt-4",
        openai_api_version=openai.api_version,
        temperature=0
    )

def initialize_prompt_template() -> PromptTemplate:
    """
    Initialize the prompt template used for generating the QA chain prompt.

    The prompt template includes instructions for the assistant to follow,
    as well as a placeholder for the context and chat history.

    Returns:
        PromptTemplate: An instance of the PromptTemplate object.
    """
    # The prompt template includes instructions for the assistant to follow,
    # as well as a placeholder for the context and chat history.
    template = """ You are a technical assistant.
    If you don't know the answer, just say that you don't know, don't try to make up an answer. 
    Keep the answer as concise as possible. Say "thanks for asking!" or "thank you!" or something similar at the end of the answer.
    Answer step by step
    Use the following context (delimited by <ctx></ctx>) and the chat history (delimited by <hs></hs>) to answer the question. :
    ------
    <ctx>
    {context}
    </ctx>
    ------
    <hs>
    {history}
    </hs>
    ------
    {question}
    Answer:
    """
    return PromptTemplate(
        input_variables=["history", "context", "question"],
        template=template,
    )


def initialize_memory() -> ConversationBufferMemory:
    """
    Initialize the memory object for storing the conversation history.

    The memory object is a ConversationBufferMemory object, which stores the
    conversation history in memory. The memory_key is set to "history", which
    is the key used to store the conversation history in the memory object.
    The input_key is set to "question", which is the key used to store the
    question in the memory object.

    Returns:
        ConversationBufferMemory: The initialized memory object.
    """
    return ConversationBufferMemory(
        memory_key="history",  # The key used to store the conversation history
        input_key="question"   # The key used to store the question
    )

def initialize_qa_chain(llm, retriever, prompt_template, memory):
    """
    Initialize the QA chain.

    Args:
        llm (AzureChatOpenAI): The language model used for generating answers.
        retriever (ElasticsearchRetriever): The retriever used for retrieving relevant documents.
        prompt_template (PromptTemplate): The prompt template used for generating the QA chain prompt.
        memory (ConversationBufferMemory): The memory used for storing the conversation history.

    Returns:
        RetrievalQA: The initialized QA chain.
    """
    # Initialize the QA chain
    return RetrievalQA.from_chain_type(
        llm=llm,
        chain_type='stuff',
        retriever=retriever,
        verbose=False,
        chain_type_kwargs={
            # Set verbose to False to disable verbose logging
            "verbose": False,
            # Set the prompt template
            "prompt": prompt_template,
            # Set the memory to store the conversation history
            "memory": memory,
        }
    )


def get_template_path():
    """
    Get the absolute path of the template.html file.

    This function gets the absolute path of the current file and then builds the
    absolute path of the template.html file. It returns the path of the template
    file.

    Returns:
        str: The absolute path of the template.html file.
    """
    # Get the absolute path of the current file
    script_dir = os.path.dirname(os.path.abspath(__file__))
    # Build the absolute path of the template.html file
    template_path = os.path.join(script_dir, 'RAGchatTemplate.html')
    return template_path

def create_flask_app(qa_chain, memory):
    """
    Create and configure a Flask app for the chatbot.
    
    This function creates a Flask app, sets up routes for handling user requests, and returns the configured app.
    
    Args:
        qa_chain (RetrievalQA): The RetrievalQA object for question answering.
        memory (ConversationBufferMemory): The memory object for storing conversation history.
    
    Returns:
        Flask: The configured Flask application.
    """
    app = Flask(__name__)
    
    store = {"chat_history":[]}

    # Use the get_template_path function to get the absolute path of the template.html file
    template_path = get_template_path()
    with open(template_path, 'r') as file:
        template = file.read()

    @app.route('/', methods=['GET', 'POST'])
    def index():
        """
        Handle GET and POST requests to the root URL.

        This function handles GET and POST requests to the root URL.
        If the request is a POST request and the 'question' key is present in the request form,
        it appends a new user message to the chat history, invokes the QA chain with the question,
        and appends the result to the chat history along with the runtime and cost.
        It then renders the template with the chat history.

        Returns:
            The rendered template with the chat history.
        """
        # Handle GET and POST requests
        if request.method == 'POST' and 'question' in request.form:
            # Get the callback for OpenAI API usage
            with get_openai_callback() as cb:
                # Start the timer
                start_time = time.time()
                # Get the question from the request form
                question = request.form['question']
                # Append the user message to the chat history
                store["chat_history"].append({"type": "user", "text": question})
                # Invoke the QA chain with the question
                result = qa_chain.invoke({"query": question})
                # Stop the timer
                end_time = time.time()
                # Calculate the runtime
                runtime = end_time - start_time
                # Calculate the cost
                cost = cb.total_cost 
                # Append the result to the chat history along with the runtime and cost
                store["chat_history"].append({"type": "bot", "text": result['result'], 
                                    "runtime": f"{runtime:.2f} seconds", 
                                    "cost": f"${cost:.5f}"})
        # Render the template with the chat history
        return render_template_string(template, chat=store["chat_history"])

    @app.route('/clear', methods=['POST'])
    def clear():
        """
        Clear the chat history and memory.

        This function clears the chat history and memory by setting the chat_history
        list to an empty list and calling the clear() method on the memory object.
        It returns a JSON response with the 'success' key set to True.

        Returns:
            JSON: A JSON object with the 'success' key set to True.
        """
        # Clear the chat history
        store["chat_history"] = []
        
        # Clear the memory
        memory.clear()
        
        # Return a success response
        return jsonify(success=True)

    @app.route('/shutdown', methods=['POST'])
    def shutdown():
        """
        Shut down the application gracefully by exiting the program.

        Returns:
            None
        """
        os._exit(0) # Exit the program

    return app

def run_app(app):
    """
    Run the Flask application on all interfaces of the host machine, listening on port 5000.

    Args:
        app (Flask): The Flask application to run.

    Returns:
        None
    """
    # Run the Flask application on all interfaces of the host machine
    # listening on port 5000
    app.run(host='0.0.0.0', port=5000)

def main(persist_directory):
    """
    Set up the OpenAI credentials, initialize the embedding, document store, retriever, LLM, prompt template, memory, and QA chain. Then, create a Flask app and run it in a separate thread.

    Args:
        persist_directory (str): The directory where the document store will persist its data.
    """
    # Set up the OpenAI credentials
    set_openai_credentials()

    # Initialize the embedding
    embedding = initialize_embedding()

    # Initialize the document store
    document_store = initialize_document_store(embedding, persist_directory)

    # Initialize the retriever
    retriever = initialize_retriever(document_store)

    # Initialize the LLM
    llm = initialize_llm()

    # Initialize the prompt template
    prompt_template = initialize_prompt_template()

    # Initialize the memory
    memory = initialize_memory()

    # Initialize the QA chain
    qa_chain = initialize_qa_chain(llm, retriever, prompt_template, memory)

    # Create a Flask app and run it in a separate thread
    app = create_flask_app(qa_chain, memory)
    t = threading.Thread(target=run_app, args=(app,))
    t.start()

    # Wait for the server to start
    time.sleep(2)

    t.join()

##########
#  main  #
##########

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Use python RAG_V1.py <persist_directory>")
        sys.exit(1)
    persist_directory = sys.argv[1]
    main(persist_directory)
