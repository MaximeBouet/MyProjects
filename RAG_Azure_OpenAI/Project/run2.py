"""This module contains the code for the main window of the application."""

from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QFileDialog, QLabel, QLineEdit, QMessageBox
import sys
import subprocess
import RAG_V1
import LoadDocuments

# Variables globales pour stocker les chemins des dossiers
documents_folder = ''
persist_directory = ''

def browse_documents():
    """
    Open a folder selection dialog and set the global documents_folder variable to the selected folder.

    This function opens a folder selection dialog and sets the global documents_folder variable to the selected folder.
    The selected folder is then set as the text of the documents_entry QLineEdit widget.

    Parameters:
        None
    """
    global documents_folder  # Declare the global variable

    # Open a folder selection dialog and get the selected folder path
    documents_folder = QFileDialog.getExistingDirectory(None, 'Select a folder')

    # Set the selected folder path in the documents_entry QLineEdit widget
    documents_entry.setText(documents_folder)

def browse_persist():
    """
    Open a folder selection dialog and set the global persist_directory variable to the selected folder.

    This function opens a folder selection dialog and sets the global persist_directory variable to the selected folder.
    The selected folder is then set as the text of the persist_entry QLineEdit widget.

    Parameters:
        None

    Returns:
        None
    """
    global persist_directory
    persist_directory = QFileDialog.getExistingDirectory(None, 'Select a folder')
    persist_entry.setText(persist_directory)

def process_documents():
    """
    Execute the LoadDocuments.py script with the selected documents and persist directory.

    This function takes the selected documents folder and persist directory from the GUI and passes them as arguments
    to the LoadDocuments.py script. It then checks if both the documents folder and persist directory are selected. If not,
    it displays a warning message. If the script executes successfully, it displays a success message. If an error occurs,
    it displays an error message.

    This function does not take any parameters and does not return anything.
    """
    # Get the selected documents folder and persist directory from the GUI
    global documents_folder, persist_directory

    # Check if both the documents folder and persist directory are selected
    if not documents_folder or not persist_directory:
        # Display a warning message if either field is missing
        QMessageBox.warning(None, "Missing fields", "Please select a folder and a persist directory.")
        return

    try:
        # Execute the LoadDocuments.py script with the selected documents folder and persist directory
        LoadDocuments.main(documents_folder, persist_directory)
        # Display a success message if the script executes successfully
        QMessageBox.information(None, "Success", "Documents processed successfully.")
    except subprocess.CalledProcessError as e:
        # Display an error message if an error occurs during the execution of the script
        QMessageBox.critical(None, "Error", f"Error while processing documents: {e}")

def run_rag():
    """
    Execute the RAG_V1.py script with the selected persist directory.
    
    Raises:
        subprocess.CalledProcessError: If an error occurs during the execution of the script.
    """
    global persist_directory

    if not persist_directory:
        # Display a warning message if the persist directory is missing
        QMessageBox.warning(None, "Missing field", "Please select a persist directory.")
        return

    try:
        # Execute the RAG_V1.py script
        RAG_V1.main(persist_directory)
        app.quit()
    except subprocess.CalledProcessError as e:
        # Display an error message if an error occurs during the execution of the script
        QMessageBox.critical(None, "Error", f"Error while running RAG: {e}")

def main():
    """
    Configure and display the main window of the application.

    This function creates a QApplication and a QWidget window and configures
    the layout of the window. It sets up various widgets for selecting
    the root documents directory and the persist directory. It also
    sets up buttons for processing the documents and running the RAG.

    Returns:
        None.
    """
    global documents_entry, persist_entry, app

    # Create the QApplication and the QWidget window
    app = QApplication(sys.argv)
    window = QWidget()
    window.setWindowTitle("RAG")

    # Set up the layout of the window
    layout = QVBoxLayout()
    window.setLayout(layout)

    # Set up the "Root documents directory" section
    documents_label = QLabel("Root documents directory (HTML):")
    documents_entry = QLineEdit()
    browse_documents_button = QPushButton("Explorer")
    browse_documents_button.clicked.connect(browse_documents)

    # Set up the "Persist directory" section
    persist_label = QLabel("Persist directory (ChromaDB):")
    persist_entry = QLineEdit()
    browse_persist_button = QPushButton("Explorer")
    browse_persist_button.clicked.connect(browse_persist)

    # Set up the "Process documents" button
    process_button = QPushButton("Process documents")
    process_button.clicked.connect(process_documents)

    # Set up the "Run the RAG" button
    run_rag_button = QPushButton("Run the RAG")
    run_rag_button.clicked.connect(run_rag)

    # Add all the widgets to the layout
    layout.addWidget(documents_label)
    layout.addWidget(documents_entry)
    layout.addWidget(browse_documents_button)
    layout.addWidget(persist_label)
    layout.addWidget(persist_entry)
    layout.addWidget(browse_persist_button)
    layout.addWidget(process_button)
    layout.addWidget(run_rag_button)

    # Show the window and start the application event loop
    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
