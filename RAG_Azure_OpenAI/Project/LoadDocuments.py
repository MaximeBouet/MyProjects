"""This module loads documents from HTML files and stores them in a vector database."""

import os
import sys
import time
import openai
from langchain_community.vectorstores import Chroma
from concurrent.futures import ThreadPoolExecutor
from azure.identity import DefaultAzureCredential
from concurrent.futures import ThreadPoolExecutor
from langchain_openai import AzureOpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import UnstructuredHTMLLoader

#########################
####    functions    ####
#########################

def process_html_batch(html_file_paths):
    """
    Process a batch of HTML files and load their contents into a list of documents.

    Args:
        html_file_paths (list): List of file paths for HTML files to process.

    Returns:
        list: List of documents loaded from the HTML files.
    """
    # Initialize an empty list to store documents
    documents = []

    # Iterate through each HTML file path
    for file_path in html_file_paths:
        # Load the HTML file and extend the documents list with the loaded documents
        loader = UnstructuredHTMLLoader(file_path)
        documents.extend(loader.load())

    # Return the list of documents
    return documents

# Function to process documents in batches
def process_in_batches(documents, batch_size, delay_time,embedding, persist_directory):
    """
    Process documents in batches to avoid rate limit.

    Args:
        documents (list): List of documents to process
        batch_size (int): Number of documents to process in each batch
        delay_time (int): Time to pause between batches in seconds

    Returns:
        doc (Chroma): Chroma object containing processed documents
    """
    for i in range(0, len(documents), batch_size):
        batch = documents[i:i + batch_size]
        ids = [str(j) for j in range(i, i+batch_size)]
        # Create a Chroma object from the batch of documents
        try:
            doc = Chroma.from_documents(batch,embedding,ids=ids,persist_directory=persist_directory)
        except Exception as error:
            # Handle any exceptions that occur during processing
            print(f"Handling request: {error}")
            exit()
        time.sleep(delay_time)  # Pause between batches to avoid rate limit 
    return doc

def main(root_directory, persist_directory):
    """
    Load documents from HTML files and store them in a vector database.

    Args:
        root_directory (str): Root directory containing HTML files.
        persist_directory (str): Directory to persist processed documents.
    """
    # Set OpenAI API credentials
    credential = DefaultAzureCredential(exclude_managed_identity_credential=True)
    
    openai.api_type = 'azuread'
    openai.api_version = "2024-02-01" # change this to your version
    openai.api_base = "https://obs-eu-swe-openai.openai.azure.com/" # change this to your endpoint
    openai.api_key = os.environ["AZURE_OPENAI_API_KEY"]

    # Set deployment name and embedding model that you want to use for your RAG
    AZURE_OPENAI_EMBEDDING_MODEL_NAME = "text-embedding-ada-002"

    # Set environment variables
    os.environ["AZURE_OPENAI_API_KEY"] = openai.api_key
    os.environ["AZURE_OPENAI_ENDPOINT"] = openai.api_base

    # Set the chunk size and overlap
    splits_chunk_size = 1000
    splits_chunk_overlap = 100
    query_results_number = 3

    # ## define the embeddings to use
    embedding = AzureOpenAIEmbeddings(
        azure_deployment=AZURE_OPENAI_EMBEDDING_MODEL_NAME, 
    #    client="azure", 
    #    chunk_size=1, 
        openai_api_version=openai.api_version
    )

    # Set the batch size (number of files to process in each batch)
    batch_size = 10
    
    # Get the list of HTML files to process
    html_files_to_process = []
    for root, dirs, files in os.walk(root_directory):
        html_files_to_process.extend([os.path.join(root, file) for file in files if file.lower().endswith(".html")])

    # Initialize an empty list to store loaded documents
    docs = []
    
    # Create a ThreadPoolExecutor for parallel processing
    # Use `ThreadPoolExecutor` to process a batch of HTML files concurrently.
    with ThreadPoolExecutor() as executor:
        # Get the total number of HTML files
        total_files = len(html_files_to_process)
        processed_files = 0
        time_start = time.time()
        
        # Iterate through the HTML files in batches
        for i in range(0, total_files, batch_size):
            batch = html_files_to_process[i:i+batch_size] # Process a batch of HTML files
            batch_docs = list(executor.map(process_html_batch, [batch])) # Use `ThreadPoolExecutor` to process a batch of HTML files concurrently.
            
            # Extend the docs list with the loaded documents from the batch
            for batch_result in batch_docs:
                docs.extend(batch_result)
                processed_files += len(batch)
                print(f"Processed {processed_files} / {total_files} files")
                print(f"Time elapsed: {time.time() - time_start} seconds")

    # ## Split the text of the document into chunks of 1000 characters with 200 characters overlap.
    # others posibilities to try, we advise RecursiveCharacterTextSplitter for PoC but also consider CharacterTextSplitter, TokenTextSplitter, or RecursiveJsonSplitter (nested)
    # Define the text splitter to split the documents into chunks
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size = splits_chunk_size,
        chunk_overlap = splits_chunk_overlap,
        separators=[r"\n\n", r"\n", r"(?<=\. )", " ", ""],
        length_function = len,
        add_start_index=True
    )

    # Split the documents into chunks
    documents = text_splitter.split_documents(docs)

    # Set the batch size and delay time
    batch_size = 99  # Adjust this based on your rate limit
    delay_time = 10  # Adjust the delay time in seconds
    
    # Call the batch processing function
    document_store = process_in_batches(documents, batch_size, delay_time, embedding, persist_directory)

    # Define the retriever using the document store and the query results number
    retriever = document_store.as_retriever(return_source_documents = True, search_type="mmr", search_kwargs={"k" : query_results_number, "fetch_k" : 3})

###############################
##########  main  #############
###############################

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Use python LoadDocuments.py <documents_folder> <persist_directory>")
        sys.exit(1)
    # Set the persist directory and root directory
    root_directory = sys.argv[1]
    persist_directory = sys.argv[2]
    main(root_directory, persist_directory)
