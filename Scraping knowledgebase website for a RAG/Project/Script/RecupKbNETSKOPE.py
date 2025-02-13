"""This module retrieves the content of NetSkope's knowledge base and saves it to a file."""

from bs4 import BeautifulSoup
import requests as r
import os
import uuid

###############
## Functions ##
###############
def extract_urls(element):
    """
    Extract the URL from an HTML element if it exists.

    Args:
        element (bs4.element.Tag): The HTML element to extract the URL from.

    Returns:
        str or None: The extracted URL if it exists, None otherwise.
    """
    # Check if the element does not contain a dropdown navigation
    if not element.find('ul', class_='dropdown_nav'):
        # Find the anchor tag within the element
        link = element.find('a')
        # Check if the link exists and has a href attribute
        if link and link.get('href'):
            # Return the href attribute value
            return link.get('href')
    # Return None if the conditions are not met
    return None

def save_page_content(url):
    """
    Save the content of a web page to a file in the local file system.

    Args:
        url (str): The URL of the web page.

    Returns:
        None
    """
    # The name of the main folder in the local file system
    firstFolderName = 'KbNetskope'
    # Get the name of the subfolder in the local file system
    directory_path = url.split('netskope-help/')[1].split('/')[0]
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
    response = r.get(url, headers={'User-Agent': 'Mozilla/5.0'})
    # Check if the request was successful
    if response.status_code == 200:
        # Write the content of the web page to the file
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(response.text)

def generateAllPagesUrls(file):
    """
    Extract URLs from the given HTML file and writes them to an output file.

    Args:
        file (str): The path to the HTML file.

    Returns:
        None
    """
    # Read the content of the HTML file
    with open(file, 'r', encoding='utf-8') as file:
        content = file.read()

    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(content, 'html.parser')

    # Find all list items with class 'nav-item'
    li_elements = soup.find_all('li', class_='nav-item')

    # Extract URLs from list items that have valid URLs
    urls = [extract_urls(li) for li in li_elements if extract_urls(li) is not None]

    # Write the extracted URLs to the output file
    with open('Temp/output_urls.txt', 'w') as output_file:
        for url in urls:
            output_file.write(url + '\n')

def getContent(file_path: str) -> None:
    """
    Read URLs from the given file and saves their content to the local file system.

    Args:
        file_path (str): The path to the file containing the URLs.

    Returns:
        None
    """
    # Open the file and read its contents
    with open(file_path, 'r') as file:
        # Read the contents of the file
        urls = file.readlines()

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
    Execute the entire process of saving the main page's content to a local file, generating all the pages URLs, and scraping all pages' content.

    This function performs the following steps:
    1. Saves the HTML content of the main page to a file named 'Temp/knowledge.html'.
    2. Generates all the pages URLs using the 'generateAllPagesUrls' function.
    3. Scrapes all pages' content using the 'getContent' function.
    4. Removes all temporary files.

    This function does not take any parameters and does not return any values.
    """
    # Save the HTML content of the main page to a file
    url = "https://docs.netskope.com/en/netskope-help/netskope-release-notes"
    page = r.get(url, headers={'User-Agent': 'Mozilla/5.0'})

    with open('Temp/knowledge.html', 'w', encoding='utf-8') as file:
        file.write(page.text)

    print('Getting all URLs . . .')
    generateAllPagesUrls('Temp/knowledge.html')
    print('Scraping all URLs . . .')
    getContent('Temp/output_urls.txt')

    # Remove all temporary files
    os.remove('Temp/knowledge.html')
    os.remove('Temp/output_urls.txt')
    
if __name__ == '__main__':
    main()