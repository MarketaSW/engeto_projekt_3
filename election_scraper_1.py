import requests
from bs4 import BeautifulSoup as bs

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
        "kod_obce": tr[0].get_text(),
        "nazev_obce": tr[1].get_text(),
    }

def select_data_municipality(soup: bs) -> list:
    """Return a list of numbers and names of municipalities.
    Parameters:
    - soup: bs object"""
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

def get_subpage_url(soup) -> list:
    """Returns a list of strings with subpage url addresses.
    Parameters:
    - soup: bs object with url addresses"""

    subpages = list()
    tds = soup.find_all("td", {"class": "cislo"})
    for td in tds:
        for link in td.children:
            subpages.append(link['href'])
    return subpages              
                


def scrape_subpage(subpage_url) -> bs:
    #url -> find all hrefs -> for href in hrefs: scrape_page(href)
    """Scrape all links from given bs4 object.
    Parameters:
    - soup: bs object"""
   




def main():
    url = "https://volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=2&xnumnuts=2102"
    soup = scrape_page(url)
    subpage_url = get_subpage_url(soup)
    subpage_soup = scrape_subpage(soup)
    results = select_data_municipality(soup)
    
    print(results)
    print(subpage_url)
    # save_to_csv(results, output_file)

if __name__ == "__main__":
    main()    