"""This module contains the GUI and event handlers for the RAG project."""

import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
import RAG_V1
import LoadDocuments
import subprocess

def browse_folder(entry_var):
    """
    Open a file dialog to select a folder and set the selected path in the entry variable.

    Args:
        entry_var (tkinter.StringVar): The variable that holds the path of the selected folder.
    """
    # Open a file dialog to select a folder
    folder_path = filedialog.askdirectory()
    
    # Set the selected path in the entry variable
    entry_var.set(folder_path)

def process_documents():
    """
    Execute the LoadDocuments.py script with the selected documents and persist directory.

    This function takes the selected documents folder and persist directory from the GUI and passes them as arguments
    to the LoadDocuments.py script. It then checks if both the documents folder and persist directory are selected. If not,
    it displays a warning message. If the script executes successfully, it displays a success message. If an error occurs,
    it displays an error message.
    """
    # Get the selected documents folder and persist directory from the GUI
    documents_folder = documents_entry.get()
    persist_directory = persist_entry.get()

    # Check if both the documents folder and persist directory are selected
    if not documents_folder or not persist_directory:
        # Display a warning message if either field is missing
        messagebox.showwarning("Missing fields", "Please select a folder and a persist directory.")
        return

    try:
        # Execute the LoadDocuments.py script with the selected documents folder and persist directory
        LoadDocuments.main(documents_folder, persist_directory)
        # Display a success message if the script executes successfully
        messagebox.showinfo("Success", "Documents processed successfully.")
    except subprocess.CalledProcessError as e:
        # Display an error message if an error occurs during the execution of the script
        messagebox.showerror("Error", f"Error while processing documents: {e}")

def run_rag():
    """
    Execute the RAG_V1.py script with the selected persist directory.

    This function takes the selected persist directory from the GUI and passes it as an argument
    to the RAG_V1.py script. It then checks if the persist directory is selected. If not,
    it displays a warning message. If the script executes successfully, it closes the window.
    If an error occurs during the execution of the script, it displays an error message.
    """
    persist_directory = persist_entry.get()

    if not persist_directory:
        # Display a warning message if the persist directory is missing
        messagebox.showwarning("Missing field", "Please select a persist directory.")
        return

    try:
        # Replace with the path to the RAG_V1.py script
        RAG_V1.main(persist_directory)
        # close the window
        root.destroy()
    except subprocess.CalledProcessError as e:
        # Display an error message if an error occurs during the execution of the script
        messagebox.showerror("Error", f"Error while running RAG: {e}")

def main():
    """
    Create the main window and initialize the GUI.

    This function creates the main window using tkinter and initializes the GUI
    by adding labels, entry boxes, and buttons. It also sets up the event handlers
    for the buttons.
    """
    global root, documents_entry, persist_entry

    # Create the main window
    root = tk.Tk()
    root.title("RAG")

    # --- Section "Process documents" ---
    # Add a label for the documents directory
    documents_label = tk.Label(root, text="Root documents directory (HTML):")
    documents_label.grid(row=0, column=0, padx=10, pady=10)

    # Create an entry box for the documents directory
    documents_entry = tk.StringVar()
    documents_entry_box = tk.Entry(root, textvariable=documents_entry, width=50)
    documents_entry_box.grid(row=0, column=1, padx=10, pady=10)

    # Add a button to browse for the documents directory
    browse_documents_button = tk.Button(root, text="Explorer", 
                                        command=lambda: browse_folder(documents_entry))
    browse_documents_button.grid(row=0, column=2, padx=10, pady=10)

    # --- Section "Persist directory" (commune) ---
    # Add a label for the persist directory
    persist_label = tk.Label(root, text="Persist directory (ChromaDB):")
    persist_label.grid(row=1, column=0, padx=10, pady=10)

    # Create an entry box for the persist directory
    persist_entry = tk.StringVar()
    persist_entry_box = tk.Entry(root, textvariable=persist_entry, width=50)
    persist_entry_box.grid(row=1, column=1, padx=10, pady=10)

    # Add a button to browse for the persist directory
    browse_persist_button = tk.Button(root, text="Explorer", command=lambda: browse_folder(persist_entry))
    browse_persist_button.grid(row=1, column=2, padx=10, pady=10)

    # --- Boutons d'action ---
    # Add a button to process the documents
    process_button = tk.Button(root, text="Process documents", command=process_documents)
    process_button.grid(row=2, column=0, columnspan=2, pady=20)

    # Add a button to run the RAG
    run_rag_button = tk.Button(root, text="Run the RAG", command=run_rag)
    run_rag_button.grid(row=3, column=0, columnspan=2, pady=10)

    # Start the main event loop
    root.mainloop()

if __name__ == "__main__":
    main()
