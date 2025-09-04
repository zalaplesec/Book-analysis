from funkcije import scrape_pages, save_to_csv


def main():
    poizvedba = "b"
    st_strani = 600

    knjige_podatki = scrape_pages(poizvedba, st_strani)
    save_to_csv("knjige1.csv", knjige_podatki)

    print(f"Skupno število knjig: {len(knjige_podatki)}")
    print(knjige_podatki[:4])


if __name__ == "__main__":
    main()
