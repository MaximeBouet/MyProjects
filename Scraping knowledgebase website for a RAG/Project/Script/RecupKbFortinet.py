"""This script retrieves the content of Fortinet's knowledge base and saves it to a file."""

import requests
from bs4 import BeautifulSoup
from selenium import webdriver
import re
from time import sleep
import urllib.request as r
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

    Example usage:
        save_knowledge_base('https://www.example.com', 'knowledge_base.html')
    """
    # Send a GET request to the specified URL and retrieve the HTML content
    response = requests.get(url)
    
    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Write the prettified HTML content to the specified file
    with open(file_name, 'w', encoding='utf-8') as file:
        file.write(soup.prettify())
        
def selenium(url):
    """
    Open a Firefox browser in headless mode and retrieves the page source of the specified URL.

    Args:
        url (str): The URL of the webpage to load.

    Returns:
        str: The page source of the loaded webpage.
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
    
    # Wait for 1 second to allow the page to load
    sleep(1)
    
    # Retrieve the page source of the loaded webpage
    return driver.page_source
    
def generateAllPagesUrls(url):
    """
    Generate all the URLs for the pages related to a specific knowledge base on the Fortinet community website.

    Args:
        url (str): The URL of the main page of the knowledge base.

    Returns:
        None

    This function first saves the HTML content of the main page of the knowledge base to a file named 'Temp/knowledge_base.html'.
    It then reads the content of the file and extracts the URLs of the individual pages using regular expressions.
    The extracted URLs are stored in the list 'FirstUrls'.

    Next, the function iterates over each URL in 'FirstUrls' and retrieves the page source using the 'selenium' function.
    The page source is saved to a file named 'Temp/knowledge.html'.
    The function then extracts the maximum number of pages from the page source using regular expressions and stores it in 'max_pages'.
    If 'max_pages' is greater than 0, the function generates additional URLs for each page number from 2 to 'max_pages' and stores them in the list 'tempsURLs'.

    Finally, the function appends all the URLs in 'FirstUrls' and 'tempsURLs' to a file named 'Temp/FirstURLs.txt'.
    """
    # Save the HTML content of the main page to a file
    save_knowledge_base(url, 'Temp/knowledge_base.html')
    
    # Read the content of the file and extract the URLs using regular expressions
    with open('Temp/knowledge_base.html', 'r', encoding='utf-8') as file:
        page_source = file.read()

    # Extract the URLs using regular expressions
    tempURLs = re.findall(r'/t5/(.*?)/tkb-p(.*?)\"', page_source)

    # Create the list of URLs
    FirstUrls = [f'https://community.fortinet.com/t5/{i[0]}/tkb-p{i[1]}' for i in tempURLs]
    
    # Remove duplicates from the list
    FirstUrls = list(set(FirstUrls))

    # Create a list to store the additional URLs
    tempsURLs = []

    # Iterate over each URL and retrieve the page source
    for url in FirstUrls:
        page_source = selenium(url)

        # Save the page source to a file
        with open('Temp/knowledge.html', 'w', encoding='utf-8') as file:
            file.write(str(page_source))
        
        # Extract the maximum number of pages from the page source
        max_pages = re.findall(r'pagination.setPage\((\d+)\)', page_source)
        
        # Generate additional URLs for each page number
        if max_pages:
            max_pages = max(int(i) for i in max_pages)
            for i in range(2, max_pages + 1):
                tempsURLs.append(f'{url}?pageNum={str(i)}')

    # Append the URLs to the file
    with open('Temp/FirstURLs.txt', 'a', encoding='utf-8') as file:
        for url in FirstUrls:
            file.write(url + '\n')
    
    # Append the additional URLs to the file
    with open('Temp/FirstURLs.txt', 'a', encoding='utf-8') as file:
        for url in tempsURLs:
            file.write(url + '\n')
            
def generateAllArticleUrls():
    """
    Generate all the article URLs for the Fortinet community website.

    This function reads the URLs from the 'Temp/FirstURLs.txt' file, retrieves the page source for each URL using the 'selenium' function,
    and extracts the article URLs from the page source. The extracted URLs are saved in the 'FirstUrls' list.

    The function then removes any duplicate URLs from the 'FirstUrls' list and saves the remaining URLs in the 'Temp/SecondURLs.txt' file,
    each URL followed by a newline character.

    Parameters:
        None

    Returns:
        None
    """
    # Initialize variable
    first_urls = []

    # Read URLs from file
    with open('Temp/FirstURLs.txt', 'r', encoding='utf-8') as file:
        urls = file.readlines()

        # For each URL, retrieve page source and extract article URLs
        for url in urls:
            page_source = selenium(url)

            # Save page source to file
            with open('Temp/knowledge.html', 'w', encoding='utf-8') as file:
                file.write(str(page_source))

            # Extract article URLs using regular expressions
            temp_urls = re.findall(r'/t5/(.*?)/(.*?)/ta-p(.*?)\"', page_source)

            # Append article URLs to list
            for i in temp_urls:
                first_urls.append(f'https://community.fortinet.com/t5/{i[0]}/{i[1]}/ta-p{i[2]}')

        # Remove duplicates from list
        first_urls = list(set(first_urls))

    # Save article URLs to file
    with open('Temp/SecondURLs.txt', 'w', encoding='utf-8') as file:
        for url in first_urls:
            file.write(url + '\n')
    
def curlAllArticles():
    """
    Download the content of each URL from 'Temp/SecondURLs.txt' and saves it to a folder named after the article title.
    
    Parameters:
    None
    
    Returns:
        None
    """
    # Read the URLs from the file
    with open('Temp/SecondURLs.txt', 'r', encoding='utf-8') as file:
        urls_2 = file.readlines()
        # For each URL, download the content and save it to a file
        for url in urls_2:
            # Download the content of the URL
            page = r.urlopen(url)
            
            # Extract the folder name and article title from the URL
            folder_name = re.findall(r'/t5/(.*?)/(.*?)/ta-p/(.*?)\n', url)
            folder = folder_name[0][0]
            title = folder_name[0][2]
            
            # Create the folder if it doesn't exist
            firstFolderName = 'KbFortinet'
            if not os.path.exists(f'KB/{firstFolderName}/{folder}'):
                os.makedirs(f'KB/{firstFolderName}/{folder}')
            
            # Save the content to a file named after the article title
            with open(f'KB/{firstFolderName}/{folder}/{title}.html', 'w', encoding='utf-8') as file:
                file.write(str(page.read().decode('utf8')))

##########
## Main ##
##########

def main():
    """
    Execute the entire process of generating all pages URLs, generating all article URLs, and scraping all articles for the Fortinet community website.

    This function performs the following steps:
    1. Sets the initial URL to 'https://community.fortinet.com/t5/Knowledge-Base/ct-p/knowledgebase'.
    2. Calls the 'generateAllPagesUrls' function to generate all the pages URLs.
    3. Prints 'Getting all URLs . . .' to indicate the process of generating URLs.
    4. Calls the 'generateAllArticleUrls' function to generate all the article URLs.
    5. Prints 'Scraping all URLs . . .' to indicate the process of scraping URLs.
    6. Calls the 'curlAllArticles' function to scrape all the articles.
    7. Removes all temporary files 'Temp/knowledge.html', 'Temp/FirstURLs.txt', Temp/SecondURLs.txt', and 'Temp/knowledge_base.html'.

    This function does not take any parameters and does not return any values.
    """
    # Set the initial URL
    url = 'https://community.fortinet.com/t5/Knowledge-Base/ct-p/knowledgebase'

    # Generate all the pages URLs
    generateAllPagesUrls(url)
    print('Getting all URLs . . .')

    # Generate all the article URLs
    generateAllArticleUrls()
    print('Scraping all URLs . . .')

    # Scrape all the articles
    curlAllArticles()

    # Remove all temporary files
    os.remove('Temp/knowledge.html')
    os.remove('Temp/FirstURLs.txt')
    os.remove('Temp/SecondURLs.txt')
    os.remove('Temp/knowledge_base.html')

if __name__ == '__main__':
    main()