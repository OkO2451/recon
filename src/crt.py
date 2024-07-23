import socket
import requests
import pandas as pd
from bs4 import BeautifulSoup

def getNames(domain_name):
    url = f"https://crt.sh/?q={domain_name}&exclude=expired&group=none"
    response = requests.get(url)
    if response.status_code == 200:
        # Parse the HTML content
        soup = BeautifulSoup(response.text, 'lxml')
        return soup  # Return BeautifulSoup object for further processing
    else:
        print(f"Failed to fetch {url}")
        return None


def clean(soup):
    if soup is None:
        return pd.DataFrame()  # Return an empty DataFrame if soup is None

    # Navigate through the layers to find the correct table
    tables = soup.find_all("table")
    if len(tables) < 2:
        print("Expected table not found")
        return pd.DataFrame()  # Return an empty DataFrame if the expected table is not present

    # Assuming the second table is the correct one
    # /html/body/table[2]/tbody/tr/td/table/tbody/tr[${row_numb}]/td[5]
    inner_table = tables[1].find("tr")

    rows = inner_table.find_all("tr")[1:] 

    domains_dict = {}

    for i, row in enumerate(rows):
        td_elements = row.find_all("td")
        if len(td_elements) > 5:
            domain = td_elements[4].text.strip()  # Get the text from the 5th td element (index 4)

            # Filtering based on domain
            if domain.split(".")[0] == "*":
                continue
            
            try:
                associated = socket.gethostbyname(domain)
                # print(f"domain: {domain} associated: {associated}")
                domains_dict[domain] = associated
            except socket.gaierror:
                print(f"Failed to get IP address for domain: {domain}")

    return pd.DataFrame(list(domains_dict.items()), columns=["Domain", "IP Address"]) 


def extract_text_with_separator(element, separator=", "):
    html = str(element)
    html_replaced = html.replace("<br>", separator).replace("<br/>", separator)
    soup = BeautifulSoup(html_replaced, "html.parser")
    return soup.get_text() 

def getCRT(domaine):
    soup = getNames(domaine)  # Get the BeautifulSoup object
    df = clean(soup)  # Clean and process the data
    # to string without including the index
    return df


# getCRT("emi.ac.ma")