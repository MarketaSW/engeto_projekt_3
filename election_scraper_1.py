"""
election_scraper_1.py: třetí projekt do Engeto Online Python Akademie
author: Markéta Svěráková Wallo
email: marketa.wallo@gmail.com
discord: marketasverakova_37252
"""
import requests
import csv
from bs4 import BeautifulSoup as bs
from pathlib import Path

def scrape_page(url) -> bs:
    """Return BeautifulSoup object from given url address.
    Parameters:
    - url: given url address"""

    response = requests.get(url)
    if response.status_code == 200:
        soup = bs(response.content, "html.parser")
        return soup
    else:
       print("Error: Unable to retrieve webpage") 

def select_attributes(tr) -> dict:
    """Select attributes from each line."""
    return {
        "code": tr[0].get_text(), 
        "location": tr[1].get_text(),
    }

def get_district_data(soup: bs) -> list:
    """Return a list of dictionaries with code and name of location
    from district page.
    Parameters:
    - soup: bs object representing district page"""

    tables = soup.find_all("table", {"class": "table"})
    results = list()
    for table in tables:
        all_tr = table.find_all("tr")
        for tr in all_tr[2:]:
            results.append(select_attributes(tr.find_all("td")))
    results = [
        item for item in results
        if any(value != "-" for value in item.values())
        ]
    return results
    
def get_subpage_urls(url: str, soup: bs) -> list:
    """Returns a list of subpage url addresses.
    Parameters:
    - soup: bs object with url addresses"""

    base_url = url[:url.rfind("/")]
    subpages = list()
    tds = soup.find_all("td", {"class": "cislo"})
    for td in tds:
        for link in td.find_all("a", href=True):
            full_url = base_url + "/" + link["href"]
            subpages.append(full_url)
    return subpages         

def append_location_data(results: list, subpages: list) -> list:
    """ Append location data scraped from subpages to data from district page.
    Registered voters, envelopes issued and valid votes from each location.
    Parameters:
    - results: a list of dictionaries with data from district page
    - subpages: a list with links to subpages of a district page"""

    for url in subpages:
        code_from_url = url.split("xobec=")[1].split("&")[0]
        soup = scrape_page(url)
        for location in results:
            if location["code"] == code_from_url:
                location["registered"] = soup.find(attrs={"headers": "sa2"}).get_text()
                location["envelopes"] = soup.find(attrs={"headers": "sa3"}).get_text()
                location["valid"] = soup.find(attrs={"headers": "sa6"}).get_text()
                break
    return results        

def append_party_data(results: list, subpages: list) -> list:
    """ Append party data scraped from subpages to data from district page.
   Name of each party and count of votes.
    Parameters:
    - results: a list of dictionaries with data from district page
    - subpages: a list with links to subpages of a district page"""
    
    for url in subpages:
        code_from_url = url.split("xobec=")[1].split("&")[0]
        soup = scrape_page(url)
        tables = soup.find_all("table", {"class": "table"})
        for table in tables[1:]:
            all_tr = table.find_all("tr")
            for tr in all_tr[2:]:
                tds = tr.find_all("td")
                party_name = tds[1].get_text()
                votes = tds[2].get_text()
                for location in results:
                    if location["code"] == code_from_url:
                        location[party_name] = votes
    return results

def write_to_csv(data, output_file):
    """Write the selected data to a CSV file.
    Parameters:
    - data: list of lists containing the selected data.
    - output_file: name of the CSV file to create."""
    path = Path(output_file)
    with path.open('w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(data[0].keys())
        for item in data:
            writer.writerow(item.values())





def main():
    url = "https://www.volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=2&xnumnuts=2102"
    soup = scrape_page(url)
    subpages = get_subpage_urls(url, soup)
    district_results = get_district_data(soup)
    location_results = append_location_data(district_results, subpages)
    results = append_party_data(location_results, subpages)
    write_to_csv(results, "selected_data.csv")
   

if __name__ == "__main__":
    main()    