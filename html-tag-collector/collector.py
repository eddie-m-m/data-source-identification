import json
import requests
from bs4 import BeautifulSoup

# Open the input file and load the JSON data
with open('urls.json') as f:
    data = json.load(f)

# Define the list of header tags we want to extract
header_tags = ['h1', 'h2', 'h3', 'h4', 'h5', 'h6']

# Loop over each URL in the data
for d in data:
    url = d['url']
    # Make a GET request to the URL
    response = requests.get(url)

    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(response.content, 'html.parser')

    # Extract the title tag and its content
    html_title = soup.title.string

    # Extract the meta description tag and its content
    meta_tag = soup.find('meta', attrs={'name': 'description'})
    meta_description = meta_tag['content'] if meta_tag is not None else ""

    # Extract the header tags and their content
    html_headers = []
    for header_tag in header_tags:
        headers = soup.find_all(header_tag)
        header_content = [header.text for header in headers]
        html_headers.append({header_tag: header_content})

    # Add the new properties to the JSON object
    d['html_title'] = html_title
    d['meta_description'] = meta_description
    d['html_headers'] = html_headers

# Write the updated JSON data to a new file
with open('urls_and_headers.json', 'w') as f:
    json.dump(data, f, indent=4)