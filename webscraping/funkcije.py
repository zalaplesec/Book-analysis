import requests
from bs4 import BeautifulSoup
import time
import csv


def fetch_html(url):
    """Fetch HTML content from a given URL."""
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.text
    except Exception as e:
        print(f"Napaka pri pridobivanju HTML: {e}")
        return None


def extract_title(knjiga):
    naslov_tag = knjiga.find("h3", class_="booktitle")
    return naslov_tag.get_text(strip=True) if naslov_tag else None


def extract_author(knjiga):
    avtor_tag = knjiga.find("span", itemprop="author")
    if avtor_tag:
        avtor = avtor_tag.get_text(strip=True)
        if avtor.lower().startswith("by"):
            avtor = avtor[2:].strip()
        return avtor
    return None


def extract_rating(knjiga):
    ocena_tag = knjiga.find("meta", itemprop="ratingValue")
    return ocena_tag["content"] if ocena_tag else None


def extract_rating_count(knjiga):
    stevilo_ocen_tag = knjiga.find("meta", itemprop="ratingCount")
    return stevilo_ocen_tag["content"] if stevilo_ocen_tag else None


def extract_want_to_read(knjiga):
    want_to_read_tag = knjiga.find("span", itemprop="reviewCount")
    return want_to_read_tag.get_text(strip=True).replace("Want to read", "").strip() if want_to_read_tag else None


def extract_publication_details(knjiga):
    podrobnosti_tag = knjiga.find("span", class_="resultDetails")
    prva_izdaja = None
    stevilo_izdaj = None
    if podrobnosti_tag:
        spans = podrobnosti_tag.find_all("span")
        if spans:
            prva_izdaja = spans[0].get_text(strip=True).replace("First published in ", "")
            if len(spans) > 1:
                stevilo_izdaj = spans[1].get_text(strip=True).replace("editions", "")
    return prva_izdaja, stevilo_izdaj


def parse_html(html):
    """Parse HTML and extract book data."""
    soup = BeautifulSoup(html, "html.parser")
    knjige = soup.find_all("li", class_="searchResultItem")

    knjige_podatki = []
    for knjiga in knjige:
        naslov = extract_title(knjiga)
        avtor = extract_author(knjiga)
        ocena = extract_rating(knjiga)
        stevilo_ocen = extract_rating_count(knjiga)
        want_to_read = extract_want_to_read(knjiga)
        prva_izdaja, stevilo_izdaj = extract_publication_details(knjiga)

        knjige_podatki.append({
            "naslov": naslov,
            "avtor": avtor,
            "ocena": ocena,
            "stevilo_ocen": stevilo_ocen,
            "want_to_read": want_to_read,
            "prva_izdaja": prva_izdaja,
            "stevilo_izdaj": stevilo_izdaj
        })

    return knjige_podatki


def scrape_pages(poizvedba, st_strani):
    """Scrape multiple pages and return all book data."""
    knjige_podatki = []
    for stran in range(1, st_strani + 1):
        url = f"https://openlibrary.org/search?q={poizvedba.replace(' ', '+')}&page={stran}"
        print(f"Scraping page {stran}...")

        html = fetch_html(url)
        if html:
            podatki = parse_html(html)
            knjige_podatki.extend(podatki)
            print(f" Zajeto knjig: {len(knjige_podatki)}")
        else:
            print(f"Napaka na strani {stran}")

        time.sleep(1)

    return knjige_podatki


def save_to_csv(filename, knjige_podatki):
    polja = ["naslov", "avtor", "ocena", "stevilo_ocen", "want_to_read", "prva_izdaja", "stevilo_izdaj"]
    with open(filename, "w", newline="", encoding="utf-8") as f:
        pisec = csv.DictWriter(f, fieldnames=polja)
        pisec.writeheader()
        pisec.writerows(knjige_podatki)