"""This module contains a function that replaces personal information in a text with placeholders."""

import re

def anonymize_text(text: str) -> str:
    """
    Replace personal information in the given text with anonymized placeholders.
    
    Args:
        text (str): The text to be anonymized.
    
    Returns:
        str: The anonymized text.
    """
    # Anonymizer les adresses IP
    anonymized_text = re.sub(r'\b(?:\d{1,3}\.){3}\d{1,3}\b', '[IP]', text)

    # Anonymizer les numéros de téléphone (format simple)
    anonymized_text = re.sub(r'\b\d{2,3}[-.\s]??\d{3}[-.\s]??\d{4}\b', '[PHONE_NUMBER]', anonymized_text)
    
    # Anonymizer les numéros de téléphone (format français) même quand il y a des espaces entre les chiffres
    anonymized_text = re.sub(r'\+\d{2}\s\d{1,2}\s\d{2}\s\d{2}\s\d{2}\s\d{2}', '[PHONE_NUMBER]', anonymized_text)
    
    # Anonymizer les numéros de téléphone (format français)
    anonymized_text = re.sub(r'[0-9]{2}\s?[0-9]{2}\s?[0-9]{2}\s?[0-9]{2}\s?[0-9]{2}\s?', '[PHONE_NUMBER]', anonymized_text)
    
    # Anonymizer les numéros de téléphone (format français) comme 06.06.06.06.06
    anonymized_text = re.sub(r'0[1-9]\.\d{2}\.\d{2}\.\d{2}\.\d{2}', '[PHONE_NUMBER]', anonymized_text)

    # Anonymizer les adresses e-mail
    anonymized_text = re.sub(r'\b[\w.-]+\s?@\s?[\w.-]+\.[a-zA-Z]{2,}\b', '[EMAIL_ADDRESS]', anonymized_text)
    
    # anonymizer les adresses mac
    anonymized_text = re.sub(r'([0-9A-Fa-f]{2}[:-]){5}([0-9A-Fa-f]{2})', '[MAC_ADDRESS]', anonymized_text)
    
    # anonymizer les ulrs
    anonymized_text = re.sub(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', '[URL]', anonymized_text)
    
    # anonymizer les url like mon-espace-adherent.lamutuellegenerale.fr
    anonymized_text = re.sub(r'\b[\w.-]+\.[a-zA-Z]{2,}\b', '[URL]', anonymized_text)
    
    return anonymized_text
