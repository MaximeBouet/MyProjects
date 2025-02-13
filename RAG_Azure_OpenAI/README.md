# Projet RAG avec l'API d'Azure OpenAI

## Prerequisites

- Python 3.12.2

## Installation Guide

To use the script, follow these steps:

1. Clone the project from the git repository:
    ```sh
    git clone <repository_url>
    ```

2. Navigate to the project directory:
    ```sh
    cd Project
    ```

3. Install the required dependencies:
    ```sh
    pip install -r requirements.txt
    ```

4. Set the environment variable `AZURE_OPENAI_API_KEY` to your Azure OpenAI API key:
    ```sh
    export AZURE_OPENAI_API_KEY=<your_api_key>
    ```

5. Update the `openai.api_base` value in the `LoadDocuments.py` and `RAG_V1.py` files to your Azure OpenAI endpoint:
    ```python
    openai.api_base = "https://your-azure-openai-endpoint.openai.azure.com/"
    ```

6. Documentation is available in `docs/_build/html/index.html`.

## Usage Guide

1. Navigate to the `Project` directory:
    ```sh
    cd Project
    ```

2. You have two options to run the scripts:
    - Manually execute the scripts `LoadDocuments.py <documents_folder> <persist_directory>` and `RAG_V1.py <persist_directory>` from the terminal:
        ```sh
        python LoadDocuments.py <documents_folder> <persist_directory>
        python RAG_V1.py <persist_directory>
        ```
    - Alternatively, launch the script `run.py` or `run2.py` to open an interface. The only difference between them is the graphical interface:
        ```sh
        python run.py
        # or
        python run2.py
        ```

## Potential Issues

- Verify that you are using the correct version of Python (3.12.2).
- If you encounter any issues with dependencies, make sure to install them using:
    ```sh
    pip install -r requirements.txt
    ```

## Additional Information

- For more detailed documentation, refer to `docs/_build/html/index.html`.
