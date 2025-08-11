import requests
from bs4 import BeautifulSoup
import time
import csv

knjige_podatki = []
poizvedba = "b"
st_strani = 600

for stran in range(1, st_strani + 1):
    url = f"https://openlibrary.org/search?q={poizvedba.replace(' ', '+')}&page={stran}"
    print(f"Scraping page {stran}...")

    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        knjige = soup.find_all('li', class_="searchResultItem")

        for knjiga in knjige:

            #naslov
            naslov_tag = knjiga.find("h3", class_ = "booktitle")
            naslov = naslov_tag.get_text(strip=True) if naslov_tag else None
            
            #avtor
            avtor_tag = knjiga.find("span", itemprop="author")
            if avtor_tag:
                avtor = avtor_tag.get_text(strip=True)
                if avtor.lower().startswith("by"):
                    avtor = avtor[2:].strip()

            #ocena
            ocena_tag = knjiga.find("meta", itemprop="ratingValue")
            ocena = ocena_tag["content"] if ocena_tag else None

            #stevilo ocen
            stevilo_ocen_tag = knjiga.find("meta", itemprop="ratingCount")
            stevilo_ocen = stevilo_ocen_tag["content"] if stevilo_ocen_tag else None

            #"Want to read"
            want_to_read_tag = knjiga.find("span",itemprop="reviewCount")
            want_to_read = want_to_read_tag.get_text(strip=True).replace("Want to read", "").strip() if want_to_read_tag else None

            #Leto objave
            podrobnosti_tag = knjiga.find("span", class_="resultDetails")
            prva_izdaja = None
            stevilo_izdaj = None
            if podrobnosti_tag:
                spans = podrobnosti_tag.find_all("span")
                if spans:
                    prva_izdaja = spans[0].get_text(strip=True).replace("First published in ", "")
                    if len(spans) > 1:
                        stevilo_izdaj = spans[1].get_text(strip=True).replace("editions", "")
    
            knjige_podatki.append({
                "naslov": naslov,
                "avtor": avtor,
                "ocena": ocena,
                "stevilo_ocen": stevilo_ocen,
                "want_to_read": want_to_read,
                "prva_izdaja": prva_izdaja,
                "stevilo_izdaj": stevilo_izdaj
            })
        print(f" Zajeto_knjig: {len(knjige_podatki)}")
    
    except Exception as e: 
        print(f"Napaka na strani {stran}: {e}")

    time.sleep(1)

                
with open("knjige.csv", "w", newline="", encoding="utf-8") as f:
    polja = ["naslov", "avtor", "ocena", "stevilo_ocen", "want_to_read", "prva_izdaja", "stevilo_izdaj"]
    pisec = csv.DictWriter(f, fieldnames=polja)
    pisec.writeheader()
    pisec.writerows(knjige_podatki)

print(f"Skupno število knjig: {len(knjige_podatki)}")
print(knjige_podatki[:4])



