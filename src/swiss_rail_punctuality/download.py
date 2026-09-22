import re 
import sys 
import urllib.request 
from pathlib import Path 
import shutil 

HEADERS = {"User-Agent": "swiss-rail-punctuality/0.1"} 
def fetch(url: str): 
    return urllib.request.urlopen(urllib.request.Request(url, headers=HEADERS)) 



PAGE_URL = "https://data.opentransportdata.swiss/dataset/ist-daten-v2"
RAW_DIR = Path("data/raw") 

def download_day(day: str) -> Path: 
    dest = RAW_DIR / f"{day}.csv" 

    if dest.exists(): 
        return dest 

    html = fetch(PAGE_URL).read().decode() 

    match = re.search(rf'https[^"]*{day}_istdaten\.csv', html)  

    if match is None: 
       raise ValueError(f"Pas de fichier pour {day}") 
    url = match.group(0) 


    RAW_DIR.mkdir(parents=True, exist_ok=True) 
    tmp = dest.with_suffix(".csv.part") 
    with fetch(url) as resp, open(tmp, "wb") as f: 
        shutil.copyfileobj(resp, f)  
    tmp.rename(dest) 

    return dest 

    

if __name__ == "__main__": 
    print(download_day(sys.argv[1])) 


