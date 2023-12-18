import requests
from bs4 import BeautifulSoup
import webbrowser

# Function to get href links from a webpage
def get_links(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    links = [a['href'] for a in soup.find_all('a', href=True)]
    return links

# Function to open link based on user input index
def open_link(links):
    try:
        index = int(input("Enter the index of the link you want to open (0 to {}): ".format(len(links) - 1)))
        if 0 <= index < len(links):
            selected_link = links[index]
            print("Opening link:", selected_link)
            # You can add your code here to open the link in a browser or perform other actions.
        else:
            print("Invalid index. Please enter a valid index.")
    except ValueError:
        print("Invalid input. Please enter a valid integer.")

# Example usage
url = 'https://www.jobsnepal.com/category'
links = get_links(url)

if links:
    print("List of links:")
    for i, link in enumerate(links):
        print(f"{i}. {link}")

    webbrowser(link)
else:
    print("No links found on the webpage.")
