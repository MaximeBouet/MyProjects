"""This module retrieves the content of Zscaler's knowledge base and saves it to a file."""

from bs4 import BeautifulSoup
from time import sleep
import os
import uuid
from selenium import webdriver

###############
## Functions ##
###############

def getAllCategory(file):
    """
    Read a file, parses its content using BeautifulSoup, extracts all the links from the parsed content, and filters them to get single segment links. It then writes the filtered links to a new file, removes irrelevant links and writes the remaining links to a new file.

    Args:
        file (str): The path to the file to be read.

    Returns:
        None
    """
    # Read the file and parse its content
    with open(file, 'r', encoding='utf-8') as file:
        content = file.read()
    
    # Parse the content using BeautifulSoup
    soup = BeautifulSoup(content, 'html.parser')

    # Extract all the links from the parsed content
    links = soup.find_all('a', href=True)

    # Filter the links to get single segment links
    single_segment_links = [link['href'] for link in links if link['href'].count('/') == 1]

    # Write the filtered links to a new file
    with open('Temp/output_links.txt', 'w') as output_file:
        for link in single_segment_links:
            output_file.write(link.strip('/') + '\n')
    
    # Read the new file and get all the lines
    with open('Temp/output_links.txt', 'r') as f:
        urls = f.readlines()
    
    # Write the remaining links to a new file after removing irrelevant links
    with open('Temp/output_urls.txt', 'w') as output_file:
        for url in urls:
            if 'contact-support' not in url and 'support-offerings' not in url and 'submit-ticket' not in url and 'training-certification' not in url and 'tools' not in url and 'acceptable-use-policy' not in url:
                output_file.write(url)
    
    # Remove empty lines from the new file
    with open('Temp/output_urls.txt', 'r') as f:
        lines = f.readlines()
    with open('Temp/output_urls.txt', 'w') as f:
        for line in lines:
            if line.strip():
                f.write(line)

def getSourceCode(url: str, file: str) -> None:
    """
    Retrieve the source code of a webpage and saves it to a file.

    Args:
        url (str): The URL of the webpage to retrieve the source code from.
        file (str): The path to the file where the source code will be saved.

    Returns:
        None
    """
    # Set the options for the Firefox browser
    options = webdriver.FirefoxOptions()
    options.add_argument('--headless')  # Run the browser in headless mode
    options.add_argument('--log-level=3')  # Set the log level to minimum
    options.add_argument('--disable-logging')  # Disable logging to reduce noise

    # Create an instance of the Firefox browser with the specified options
    driver = webdriver.Firefox(options=options)

    # Load the specified URL in the browser
    driver.get(url)

    # Wait for 10 seconds to allow the page to load
    sleep(10)

    # Get the page source of the loaded webpage
    page = driver.page_source
    
    # Quit the browser
    driver.quit()

    # Save the page source to the specified file
    with open(file, 'w', encoding='utf-8') as file:
        file.write(page)

def getAllPagesUrls(file):
    """
    Read a file with URLs, retrieves the source code of each URL, extracts links from the source code, and writes the extracted links to a new file.

    Args:
        file (str): The path to the file containing URLs.

    Returns:
        None
    """
    # Initialize an empty list to store the extracted URLs
    URLs = []

    # Read the file and get all the lines
    with open(file, 'r') as f:
        category = f.readlines()

    # Iterate over each line in the file
    for cat in category:
        cat = cat.strip()  # Remove leading/trailing whitespace

        # Construct the URL using the current line
        url = f"https://help.zscaler.com/{cat}"

        # Retrieve the source code of the URL and save it to a temporary file
        getSourceCode(url, 'Temp/temp.html')

        # Read the content of the temporary file
        with open('Temp/temp.html', 'r', encoding='utf-8') as file:
            content = file.read()

        # Parse the content using BeautifulSoup
        soup = BeautifulSoup(content, 'html.parser')

        # Find all the links in the parsed content
        links = soup.find_all('a', href=True)

        # Write the extracted links to a new file
        with open('Temp/output_links.txt', 'a') as output_file:
            for link in links:
                # Check if the link starts with the current line and has more than one '/'
                if link['href'].startswith(f'/{cat}') and link['href'].count('/') > 1:
                    # Write the complete URL to the output file
                    output_file.write('https://help.zscaler.com' + link['href'] + '\n')

                    # Add the complete URL to the list of URLs
                    URLs.append('https://help.zscaler.com' + link['href'])

    # Write the list of URLs to a new file
    with open('Temp/FinalLinks.txt', 'w') as f:
        for url in URLs:
            f.write(url + '\n')
                
def save_page_content(url):
    """
    Save the content of a web page to a file in the local file system.

    Args:
        url (str): The URL of the web page.

    Returns:
        None
    """
    # The name of the main folder in the local file system
    firstFolderName = 'KbZscaler'
    
    # Get the name of the subfolder in the local file system
    directory_path = url.split('.com/')[1].split('/')[0]
    
    # Construct the path to the subfolder
    directory_path = f'KB/{firstFolderName}/{directory_path}'
    
    # Check if the subfolder does not exist and create it
    if not os.path.exists(directory_path):
        os.makedirs(directory_path)

    # Generate a unique file name
    file_name = f'{str(uuid.uuid4())}.html'
    
    # Construct the full file path
    file_path = os.path.join(directory_path, file_name)

    # Get the content of the web page
    getSourceCode(url, 'Temp/temp.html')

    # Write the content of the web page to the file
    with open(file_path, 'w', encoding='utf-8') as file:
        with open('Temp/temp.html', 'r', encoding='utf-8') as f:
            content = f.read()
        file.write(content)

def getContent(file):
    """
    Read URLs from a file, save their content to the local file system.

    Args:
        file (str): The path to the file containing the URLs.

    Returns:
        None
    """
    # Open the file and read its contents
    with open(file, 'r') as f:
        # Read the contents of the file
        urls = f.readlines()

    # For each URL, save its content to the local file system
    for url in urls:
        # Get the URL
        url = url.strip()
        # Save the content of the URL to the local file system
        save_page_content(url)
        
##########
## Main ##
##########
def main():
    """
    Execute the entire process of scraping the Zscaler knowledge base website.

    This function performs the following steps:
    1. Saves the HTML content of the main page to a file.
    2. Extracts all the categories from the parsed content.
    3. Generates all the pages URLs for each category.
    4. Scrapes all pages' content for each category.
    5. Removes all temporary files.

    This function does not take any parameters and does not return any values.
    """
    # Save the HTML content of the main page to a file
    url = "https://help.zscaler.com/zia"
    getSourceCode(url, 'Temp/knowledge.html')

    # Extract all the categories from the parsed content
    print('Getting all categories URLs . . .')
    getAllCategory('Temp/knowledge.html')

    # Generate all the pages URLs for each category
    print('Getting all URLs . . .')
    getAllPagesUrls('Temp/output_urls.txt')

    # Scrape all pages' content for each category
    print('Scraping all URLs . . .')
    getContent('Temp/FinalLinks.txt')

    # Remove all temporary files
    os.remove('Temp/knowledge.html')
    os.remove('Temp/output_urls.txt')
    os.remove('Temp/output_links.txt')
    os.remove('Temp/FinalLinks.txt')
    os.remove('Temp/temp.html')
    
if __name__ == '__main__':
    main()