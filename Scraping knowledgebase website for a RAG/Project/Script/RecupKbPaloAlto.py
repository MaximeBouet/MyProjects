"""This module contains functions for retrieving the content of Palo Alto's knowledge base and saving it to a file."""

from typing import List
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
import re
import urllib.parse
from time import sleep
import uuid 
import os

###############
## Functions ##
###############
def save_knowledge_base(url: str, file_name: str) -> None:
    """
    Save the content of a webpage to a file.

    Args:
        url (str): The URL of the webpage to save.
        file_name (str): The name of the file to save the content to.

    Returns:
        None

    Raises:
        None

    This function sends a GET request to the specified URL and retrieves the HTML content of the webpage.
    It then uses BeautifulSoup to parse the HTML and prettify it. The prettified HTML is then written to the specified file.
    """
    # Send a GET request to the specified URL and retrieve the HTML content
    response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
    
    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Write the prettified HTML content to the specified file
    with open(file_name, 'w', encoding='utf-8') as file:
        file.write(soup.prettify())
        file.write(soup.prettify())

def get_urls(file_name):
    """
    Read an HTML file and extracts all URLs from anchor tags.

    Args:
        file_name (str): The path to the HTML file.

    Returns:
        List[str]: A list of URLs extracted from the HTML file.
                    Each URL is followed by a newline character.
    """
    # Open the HTML file and read its contents
    with open(file_name, 'r', encoding='utf-8') as file:
        # Parse the HTML content using BeautifulSoup
        soup = BeautifulSoup(file, 'html.parser')
    
    # Find all anchor tags
    # and extract their href attribute values
    # and append a newline character to each value
    return [
        f"{link.get('href')}\n"
        for link in soup.find_all('a')
    ]


def save_urls(urls: List[str], file_name: str) -> None:
    """
    Save a list of URLs to a file.

    Args:
        urls (List[str]): The list of URLs to save.
        file_name (str): The name of the file to save the URLs to.

    Returns:
        None
    """
    with open(file_name, 'w', encoding='utf-8') as file:
        for url in urls:
            file.write(url + '\n') # Add a newline character after each URL
            
def get_urls_from_page_source(file_name):
    """
    Read an HTML file and extracts all URLs from anchor tags.

    Args:
        file_name (str): The path to the HTML file.

    Returns:
        List[str]: A list of URLs extracted from the HTML file.
                    Each URL is followed by a newline character.
    """
    # Open the HTML file and read its contents
    with open(file_name, 'r', encoding='utf-8') as file:
        # Read the contents of the file
        page_source = file.read()
    
    # Use regular expressions to find all URLs in the HTML file
    # Urls are expected to start with 'https://knowledgebase' and end with '"'
    urls = re.findall(r'href="https://knowledgebase(.*?)\"', page_source)
    
    # Decode percent-encoded characters in each URL and append a newline character
    urls = [
        f"https://knowledgebase{urllib.parse.unquote(url)}" + '\n'
        for url in urls
    ]
    
    return urls

def selenium(url):
    """
    Use Selenium to open a URL in a headless browser.

    Args:
        url (str): The URL to open.

    Returns:
        str: The page source of the opened URL.
    """
    # Set the options for the Firefox browser
    options = webdriver.FirefoxOptions()
    options.add_argument("--headless")  # Run the browser in headless mode
    options.add_argument("--log-level=3")  # Set the log level to minimum
    options.add_argument("--disable-logging")  # Disable logging to reduce noise

    # Create an instance of the Firefox browser with the specified options
    driver = webdriver.Firefox(options=options)

    # Load the specified URL in the browser
    driver.get(url)

    # Wait for 3 seconds to allow the page to load
    sleep(3)
    
    # Get the page source of the loaded webpage
    page = driver.page_source
    
    # Quit the browser
    driver.quit()

    # Get the page source of the loaded webpage
    return page

def save_page_source(url, firstFolderName, folder, file_name):
    """
    Save the page source of a given URL to a file.

    Args:
        url (str): The URL of the page.
        firstFolderName (str): The name of the top-level folder.
        folder (str): The name of the subfolder.
        file_name (str): The name of the file to save the page source to.

    Returns:
        None
    """
    page_source = selenium(url)

    # Save the page source to a file
    with open(f'KB/{firstFolderName}/{folder}/{file_name}', 'w', encoding='utf-8') as file:
        file.write(str(page_source))
        
def scrapPages(FirstUrls):
    """
    Scrap pages based on the list of URLs provided in FirstUrls.

    Check page source for search results and append URLs accordingly.
    Save page sources and extract URLs for further processing. 

    Args:
        FirstUrls (list): List of URLs to scrape pages from

    Returns:
        None
    """
    for url in FirstUrls:
        # Get the page source of the URL
        page_source = selenium(url)

        # Check if the page contains search results
        if re.findall(r'Results (\d+)-(\d+)', str(page_source)):
            # Get the number of results from the page source
            xx = re.findall(r'Results (\d+)-(\d+)', str(page_source))[0][1]

            # If the number of results is a multiple of 100 or 1000, append the URL to FirstUrls
            if int(xx) % 100 == 0 or int(xx) % 1000 == 0:
                FirstUrls.append(url.replace('search#', f'search#first={str(xx)}&'))
        
        # Save the URLs to a file
        save_urls(FirstUrls, 'Temp/FirstURLs.txt')
        
        # Extract the folder name from the URL
        folder = url.split('[')[-1].split(']')[0]
        firstFolderName = 'KbPaloalto'
        
        # Create the folder if it doesn't exist
        if not os.path.exists(f'KB/{firstFolderName}/{folder}'):
            os.makedirs(f'KB/{firstFolderName}/{folder}')
        
        # Save the page source to a file
        with open('Temp/knowledge_base_page_source.html', 'w', encoding='utf-8') as file:
            file.write(str(page_source))

        # Get the URLs from the page source
        SecondURLs = get_urls_from_page_source('Temp/knowledge_base_page_source.html')
        save_urls(SecondURLs, 'Temp/SecondURLs.txt')

        counter = 0
        with open('Temp/SecondURLs.txt', 'r', encoding='utf-8') as file:
            urls_2 = file.readlines()
            for url in urls_2:
                # Generate a unique title for each file
                title = uuid.uuid4()
                # Save the page source to a file named after the unique title
                save_page_source(url, firstFolderName, folder, f'{str(title)}.html')
                counter += 1

#############
## Main ##
#############
def main():
    """
    Execute the entire process of scraping the Palo Alto knowledge base website.

    This function performs the following steps:
    1. Saves the HTML content of the main page to a file named 'Temp/knowledge_base.html'.
    2. Extracts the URLs of the individual pages using regular expressions.
    3. Generates additional URLs for each page number from 2 to the maximum number of pages.
    4. Saves the URLs to a file named 'Temp/FirstURLs.txt'.
    5. Calls the 'scrapPages' function to scrape the pages and their URLs.
    6. Removes all temporary files.

    This function does not take any parameters and does not return any values.
    """
    # Save the HTML content of the main page to a file
    url = 'https://knowledgebase.paloaltonetworks.com/'
    save_knowledge_base(url, 'Temp/knowledge_base.html')

    # Extract the URLs using regular expressions
    tempURLs = get_urls('Temp/knowledge_base.html')

    # Generate the additional URLs for each page number
    FirstUrls = [
        url.replace('search#', 'search#sort=relevancy&numberOfResults=100&')
        for url in tempURLs
    ]

    # Save the URLs to a file
    print('Getting all URLs . . .')
    save_urls(FirstUrls, 'Temp/FirstURLs.txt')

    # Scrape the pages and their URLs
    print('Scraping all URLs . . .')
    scrapPages(FirstUrls)

    # Remove all temporary files
    os.remove('Temp/knowledge_base_page_source.html')
    os.remove('Temp/knowledge_base.html')
    os.remove('Temp/FirstURLs.txt')
    os.remove('Temp/SecondURLs.txt')
    
if __name__ == '__main__':
    main()