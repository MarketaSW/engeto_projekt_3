# engeto_projekt_3
Elections scraper

<h2>Popis projektu</h2>
Třetí projekt Engeto akademie slouží k extrahování výsledků [parlamentních voleb z roku 2017](https://volby.cz/pls/ps2017nss/ps3?xjazyk=CZ) za jednotlivé územní celky.

<h2>Instalace knihoven</h2>
Použité knihovny jsou vypsány v souboru requirements.txt. Pro instalaci doporučuji vytvořit nové virtuální prostředí a s nainstalovaným manažerem spustit následovně:
> $ pip --version #ověření verze manažeru
> $ pip install -r requirements.txt #instalace knihoven

<h2>Spuštění projektu</h2>
Spuštění souboru election_scraper.py v příkazovém řádku vyžaduje dva povinné argumenty:
1. url zvoleného územního celku (na webu získáme kliknutím na X ve sloupci výběr obce)
2. název výstupního CSV souboru
Celý příkaz vypadá takto:
> python election_scraper.py <argument-1> <argument-2>
Po spuštění se vytvoří CSV soubor s výsledky.

<h2>Ukázka projektu</h2>
Výsledky hlasování pro okres Benešov:
1. argument: https://volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=2&xnumnuts=2101
2. argument: vysledky_benesov.csv

<h3>Spuštění programu:</h3>
> python3 election_scraper.py "https://volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=2&xnumnuts=2101" vysledky_benesov.csv

<h3>Průběh stahování:</h3>
> Downloading data from given URL: https://volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=2&xnumnuts=2101
> Saving to file: output_benesov_2.csv
> Terminating the program.

<h3>Částečný výstup:</h3>
> code,location,registered,envelopes,valid,Občanská demokratická strana,...
> 529303,Benešov,13 104,8 485,8 437,1 052,10,2,624,3,802,597,109,35,112,6,11,948,3,6,414,2 577,3,21,314,5,58,17,16,682,10
> 532568,Bernartice,191,148,148,4,0,0,17,0,6,7,1,4,0,0,0,7,0,0,3,39,0,0,37,0,3,0,0,20,0
> 530743,Bílkovice,170,121,118,7,0,0,15,0,8,18,0,2,0,0,0,3,0,0,2,47,1,0,6,0,0,0,0,9,0
> 532380,Blažejovice,96,80,77,6,0,0,5,0,3,11,0,0,3,0,0,5,1,0,0,29,0,0,6,0,0,0,0,8,0
> 532096,Borovnice,73,54,53,2,0,0,2,0,4,4,1,0,1,0,0,3,0,0,1,29,0,0,5,0,0,0,0,1,0