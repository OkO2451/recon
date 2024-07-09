import requests
import pandas as pd
from bs4 import BeautifulSoup

    
def getNames(domain_name):
    url = f"https://crt.sh/?q={domain_name}&exclude=expired&group=none"
    response = requests.get(url)
    if response.status_code == 200:
        # Parse the HTML content
        soup = BeautifulSoup(response.text, 'lxml')
        
        return clean(soup)
    else:
        print(f"Failed to fetch {url}")
        return None
    
def clean(soup):
    tr = soup.find_all("tr")
    tr.pop(0)
    tr.pop(0)
    tr.pop(0)
    domains_dict = {}

    # Loop through each <tr> element
    for tr_element in tr:
        td_elements = tr_element.find_all("td")
        
        # Ensure there are enough <td> elements to avoid IndexError
        if len(td_elements) > 5:
            domain = td_elements[4].text
            # Manually handle <br> tags in the 5th <td>
            associated = extract_text_with_separator(td_elements[5], ", ")
            
            # Store the domain and associated domain in the dictionary
            domains_dict[domain] = associated
    df = pd.DataFrame(list(domains_dict.items()), columns=["Domain", "Associated Domains"])
    df.to_csv("data/crt.csv", index=False)
    return df
    
def extract_text_with_separator(element, separator=", "):
    html = str(element)
    # Replace <br> and <br/> with the separator
    html_replaced = html.replace("<br>", separator).replace("<br/>", separator)
    # Parse the modified HTML string
    soup = BeautifulSoup(html_replaced, "html.parser")
    # Extract and return the text
    return soup.get_text()


getNames("emi.ac.ma")
