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
        for tr in all_tr[3:]:
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
            full_url = base_url + "/" + link['href']
            subpages.append(full_url)
    return subpages         

def scrape_subpages(subpages: list) -> list:
    """Scrape all links from given list. Return a list with
    data from all links.
    Parameters:
    - subpages: list of url links to scrape"""

    subpage_soup = list()
    for url in subpages:
        subpage_soup.append(scrape_page(url))
    return subpage_soup    
        
def select_subpage_attributes(tr) -> dict:
    """Select attributes from each line."""
    return {
        "kod_obce": tr[0].get_text(), 
        "nazev_obce": tr[1].get_text(),
    }

def get_first_table_data(subpage_soup: bs) -> list:
    """Return a count of voters in a list, envelopes issued and 
    valid votes.
    Parameters:
    - subpage_soup: bs object representing the subpage """
    
    volici = subpage_soup.find(attrs={"headers": "sa2"})
    obalky = subpage_soup.find(attrs={"headers": "sa3"})
    platne_hlasy = subpage_soup.find(attrs={"headers":"sa6"})
    return [volici, obalky, platne_hlasy]

def select_subpage_data(subpage_soup: bs) -> list:
    """Return a list of voters, envelopes issued, valid votes
    and parties running for election (with number of votes).
    Parameters:
    - subpage_soup: bs object representing the subpage"""
    
    tables = subpage_soup.find_all("table", {"class": "table"})
    results = list()
    for table in tables:
        all_tr = table.find_all("tr")
        for tr in all_tr[3:]:
            results.append(select_subpage_attributes(tr.find_all("td")))
    results = [
        item for item in results
        if any(value != "-" for value in item.values())
        ]
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
    results = get_district_data(soup) #list se slovniky pro vsechny obce na strance (kod a nazev obce)
    # subpages = get_subpage_urls(url, soup)
    # subpage_soup = scrape_subpage(subpages)
    # subpage_first_table = get_first_table_data(subpage_soup)
    # subpage_results = select_subpage_data(subpage_soup) # v select_data upravit použití 
    #funkce select_attributes - budou tam jiné atributy než v main page 
   
    write_to_csv(results, "selected_data.csv")
    #-> zadat jako parametry
    # save_to_csv(results, output_file)

if __name__ == "__main__":
    main()    