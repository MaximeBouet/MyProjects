# ServiceNOW Ticket Anonymization Project

## Description

This project anonymizes ServiceNOW support tickets to train an AI on this data.

## Prerequisites

- Python 3.12.2

## Installation Guide

1. Clone the project:
    ```sh
    git clone https://github.com/...
    cd ...
    ```

2. Documentation is available at `docs/_build/html/index.html`.

3. Place the CSV file containing all non-anonymized tickets in the `data` folder.

4. Install the dependencies:
    ```sh
    pip install -r requirements.txt
    ```

## Usage Guide

1. Verify that you are using the correct version of Python (3.12.2).

2. To run the anonymization script, you have two options:
    - Execute the `Run_Anonymise.py` file:
        ```sh
        python Run_Anonymise.py <filenameXLSX> <filenameCSV>
        ```
    - Use the graphical interface by launching the `Run_with_GUI.py` file:
        ```sh
        python Run_with_GUI.py
        ```

## Potential Issues

- Verify that all dependencies are installed using the command `pip install -r requirements.txt`.
- If you encounter Python version issues, ensure you are using Python 3.12.2.

## Additional Information

- For more detailed documentation, refer to `docs/_build/html/index.html`.
