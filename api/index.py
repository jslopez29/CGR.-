import requests
from bs4 import BeautifulSoup

# Replace 'your_url_here' with the actual URL of the webpage you want to scrape
url = 'uexternado.edu.co'

# Send a GET request to the URL
response = requests.get(url)

# Check if the request was successful (status code 200)
if response.status_code == 200:
    # Parse the HTML content of the page
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find all the links on the page
    links = soup.find_all('a')

    # Extract the href attribute from each link
    hrefs = [link.get('href') for link in links]

    # Print the list of all links
    print("All links on the page:")
    for href in hrefs:
        print(href)

    # If you want the newest link, you can select the first one in the list
    newest_link = hrefs[0]
    print("\nThe newest link on the page is:", newest_link)

    # Now, you can open this link using a web browser or perform further actions

else:
    print(f"Failed to retrieve the webpage. Status code: {response.status_code}")