"""This module provides a GUI for running the anonymization script."""

import tkinter as tk
from tkinter import filedialog, messagebox
import subprocess
import Run_Anonymise

def select_csv_file():
    """Open a file dialog to select a CSV file and sets the file path to a StringVar."""
    # Open a file dialog to select a CSV file
    file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
    
    # If a file path is selected, set it to the StringVar
    if file_path:
        csv_file_path.set(file_path)

def run_anonymization_script():
    """
    Run the anonymization script with the selected parameters.

    This function checks if the CSV file path and Excel file name have been selected.
    If not, it displays an error message.

    If the Excel file name does not end with ".xlsx", it also displays an error message.

    If all the checks pass, it runs the anonymization script using the selected parameters.
    If the script runs successfully, it displays a success message and closes the window.

    If an error occurs while running the script, it displays an error message with the error details.
    """
    # Check if CSV file path and Excel file name have been selected
    if not csv_file_path.get() or not excel_file_name.get():
        messagebox.showerror("Error", "Please select a CSV file and specify the Excel file name.")
        return
    
    # Check if Excel file name ends with ".xlsx"
    if not excel_file_name.get().endswith(".xlsx"):
        messagebox.showerror("Error", "Please specify a valid Excel file name.")
        return
    
    try:
        # Run the anonymization script with the selected parameters, 
        ###### Change path accordingly #####
        Run_Anonymise.main(csv_file_path.get(), excel_file_name.get())
        
        # Display success message
        messagebox.showinfo("Success", "Anonymization completed successfully!")
        
        # Close the window
        root.destroy()
        
    except subprocess.CalledProcessError as e:
        # Display error message with error details
        messagebox.showerror("Error", f"An error occurred while running the script: {e}")

def main():
    """
    Run the GUI for the anonymization script.

    This function creates the main window, creates and places the widgets,
    and runs the main loop to handle the user interaction.

    """
    global csv_file_path, excel_file_name, root

    # Create the main window
    root = tk.Tk()
    root.title("Anonymization Script Runner")

    # Variables to store file paths
    csv_file_path = tk.StringVar()
    excel_file_name = tk.StringVar()

    # Create and place the widgets
    tk.Label(root, text="Select CSV File:").grid(row=0, column=0, padx=10, pady=10)
    # Entry widget to display the selected CSV file path
    tk.Entry(root, textvariable=csv_file_path, width=50).grid(row=0, column=1, padx=10, pady=10)
    # Button to open the file dialog to select the CSV file
    tk.Button(root, text="Browse", command=select_csv_file).grid(row=0, column=2, padx=10, pady=10)

    tk.Label(root, text="Excel File Name:").grid(row=1, column=0, padx=10, pady=10)
    # Entry widget to display the Excel file name
    tk.Entry(root, textvariable=excel_file_name, width=50).grid(row=1, column=1, padx=10, pady=10)

    # Button to run the anonymization script
    tk.Button(root, text="Run Anonymization", command=run_anonymization_script).grid(row=2, column=0, columnspan=3, pady=20)

    # Run the main loop to handle user interaction
    root.mainloop()

if __name__ == "__main__":
    main()