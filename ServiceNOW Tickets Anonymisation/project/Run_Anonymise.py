"""This module contains the code for the anonymisation process."""

import sys
from AnonymiseWithTransformers import anonymise_with_transformer
from AnonymiseWithREGEX import anonymize_text
import pandas as pd
import re

##########################
#  Function
##########################
def get_name_column(df, name_column):
    """
    Get the unique values in the specified column of the dataframe, clean and split them, and return as a list of lists.
    
    Parameters:
        df (DataFrame): The pandas DataFrame containing the data.
        name_column (str): The name of the column in the DataFrame.
    
    Returns:
        list: A list of lists containing the cleaned and split unique values from the specified column.
    """
    # parcoure the dataframe column "société" and build a list of all the index
    index = []
    for i in range(len(df)):
        index.append(df[name_column][i])
        
    # remove duplicates
    index = list(set(index))

    # remove nan values
    index = [x for x in index if str(x) != 'nan']

    # remove empty strings
    index = [x for x in index if str(x) != '']

    # split the index names if they contain a space or a dash but keep the original name
    index_split = []
    for i in index:
        if re.search(r'\s', i):
            index_split.append(i.split())
        elif re.search(r'-', i):
            index_split.append(i.split('-'))
        
        index_split.append([i])

    # in companies_split, remove words "du", "-", ...
    for i in index_split:
        for j in i:
            if j in ["du", "-", "le", "la", "les", "de", "des", "et", "en", "SARL", "La", "Le", "Les", "33", "2024", "L", "l", "2020", "SI", "GA", "CMA", "CGM", "GRT", "GAZ", "CD91", "EAU", "RMC", "IT", "NSOC"]:
                i.remove(j)
    
    # remove duplicates in index_split
    index_split = [list(x) for x in set(tuple(x) for x in index_split)]

    return index_split

def anonymise_column(df, companies_split, name_column):
    """
    Anonymise the given column in the dataframe by replacing potential personal information with placeholders.
    
    Parameters:
        df (DataFrame): The pandas DataFrame containing the data.
        companies_split (list): A list of lists containing the cleaned and split unique values from the specified column.
        name_column (str): The name of the column in the DataFrame.
    
    Returns:
        DataFrame: The DataFrame with the anonymized column.
    """
    # In the column "Element de configuration"
    # Anonymize URLs
    df[name_column] = df[name_column].apply(lambda x: re.sub(r'\b[\w.-]+\.[a-zA-Z]{2,}\b', '[URL]', str(x)))
    # Anonymize mac addresses
    df[name_column] = df[name_column].apply(lambda x: re.sub(r'([0-9A-Fa-f]{2}[:-]){5}([0-9A-Fa-f]{2})', '[MAC_ADDRESS]', x))
    # Anonymize email addresses
    df[name_column] = df[name_column].apply(lambda x: re.sub(r'\b[\w.-]+\s?@\s?[\w.-]+\.[a-zA-Z]{2,}\b', '[EMAIL_ADDRESS]', x))
    # Anonymize phone numbers
    df[name_column] = df[name_column].apply(lambda x: re.sub(r'0[1-9]\.\d{2}\.\d{2}\.\d{2}\.\d{2}', '[PHONE_NUMBER]', x))
    df[name_column] = df[name_column].apply(lambda x: re.sub(r'[0-9]{2}\s?[0-9]{2}\s?[0-9]{2}\s?[0-9]{2}\s?[0-9]{2}\s?', '[PHONE_NUMBER]', x))
    df[name_column] = df[name_column].apply(lambda x: re.sub(r'\+\d{2}\s\d{1,2}\s\d{2}\s\d{2}\s\d{2}\s\d{2}', '[PHONE_NUMBER]', x))
    df[name_column] = df[name_column].apply(lambda x: re.sub(r'\b\d{2,3}[-.\s]??\d{3}[-.\s]??\d{4}\b', '[PHONE_NUMBER]', x))
    # Anonymize IPs
    df[name_column] = df[name_column].apply(lambda x: re.sub(r'\b(?:\d{1,3}\.){3}\d{1,3}\b', '[IP]', x))

    # Anonymize text
    df[name_column] = df[name_column].apply(lambda x: anonymize_text(x) if pd.notnull(x) else x)

    # Anonymize companies
    for i in df.index:
        for company in companies_split:
            for word in company:
                if word in df.loc[i, name_column]:
                    df.loc[i, name_column] = df.loc[i, name_column].replace(word, "[ORGANIZATION]")
    return df
                    
def anonymise_description(df, names):
    """
    Anonymize the names in the "Description" column of the dataframe.
    
    Parameters:
        df (DataFrame): The pandas DataFrame containing the data.
        names (list): A list of lists containing the cleaned and split unique values from the specified column.
    
    Returns:
        DataFrame: The DataFrame with the anonymized "Description" column.
    """
    # Anonymize the names in the "Description" column
    for i in df.index:
        for name in names:
            for word in name:
                description = df.loc[i, 'Description']
                if isinstance(description, str) and word in description:
                    # Replace the name in the description by [PERSON]
                    df.loc[i, 'Description'] = description.replace(word, "[PERSON]")
    return df

def main(filenameCSV, filenameXLSX):
    """
    Anonymise tickets.
    
    Parameters:
        filenameCSV (str): The path of the CSV file to anonymize.
        filenameXLSX (str): The path of the Excel file to save the anonymized data.
        
    Returns:
        None
    """
    # read the csv file
    print("### Openning the csv file and save it as dataframe 'df'... ###")
    df = pd.read_csv(filenameCSV, encoding='ISO-8859-1', sep=';', on_bad_lines='skip', header=0, low_memory=False)
    
    # check that the column name Description is in the dataframe
    if 'Description' not in df.columns:
        print('The file does not contain the required columns.')
        return
    
    # Anonymize the 'Description' column using the anonymize_with_transformer function
    print("### Anonymize the 'Description' column using the anonymize_with_transformer function... ###")
    df['Description'] = df['Description'].apply(lambda x: anonymise_with_transformer(anonymize_text(x)) if pd.notnull(x) else x)
    
    # Get the split names from the "Société" column
    companies_split = get_name_column(df, "Société")
    
    # Anonymize the columns 'Titre', 'Élément de configuration', and 'Branche'
    print("### Anonymize the columns 'Titre', 'Élément de configuration', and 'Branche'... ###")
    for column in ['Titre', 'Élément de configuration', 'Branche']:
        df = anonymise_column(df, companies_split, column)

    # Get the split names from the "Ouvert par" column
    names_split = get_name_column(df, "Ouvert par")
    
    # Anonymize the names in the "Description" column
    print("### Anonymize the names in the 'Description' column... ###")
    df = anonymise_description(df, names_split)
    
    # Clear the columns 'Site', 'Société', 'Lien CMDB', 'Ouvert par', 'Solliciteur', and 'Affecté à' 
    for i in ['Site', 'Société', 'Lien CMDB', 'Ouvert par', 'Solliciteur', 'Affecté à']:
        df[i] = ""
    
    # Export the DataFrame to an Excel file
    print("### Export the DataFrame to an Excel file... ###")
    
    # Get the path of the CSV file and add the filenameXLSX to it
    path = filenameCSV.rsplit('/', 1)[0]
    filenameXLSX = path + '/' + filenameXLSX
    
    df.to_excel(filenameXLSX, index=False) # Export the DataFrame to an Excel file

if __name__ == "__main__":
    # get the parameters from the command line
    if len(sys.argv) > 2:
        filenameXLSX = sys.argv[2]
        filenameCSV = sys.argv[1]
    else:
        print("Usage: python Run_Anonymise.py <filenameXLSX> <filenameCSV>")
        sys.exit(1)
    main(filenameCSV, filenameXLSX)