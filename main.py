import requests
import os
import csv
from bs4 import BeautifulSoup as bS

# vérifier l'installation pip -m pour requests et beautifulsoup4 #


URL = "http://books.toscrape.com/"


def scrap_page(url_book):
    result = {}
    response = requests.get(url_book)

    if response.ok:

        soup = bS(response.text, "html.parser")
        result["product_page_url"] = url_book
        result["product_description"] = soup.find("div", {"id", "content"}).findAll("p")[3].text
        result["title"] = soup.find("h1").text  # title scrap on product_page#
        result["upc"] = soup.findAll("td")[0].text  # universal_ product_code (upc) scrap on product_page#
        result["price_including_tax"] = soup.findAll("td")[3].text  # price_including_tax scrap on product_page#
        result["price_excluding_tax"] = soup.findAll("td")[2].text  # price_excluding_tax  scrap on product_page#
        result["availability"] = soup.findAll("td")[5].text  # Availability scrap on product_page#
        result["category"] = soup.find("ul", {"class": "breadcrumb"}).findAll("a")[2].text
        image = soup.find("div", {"class": "item active"}).find({"img": "src"})
        result["image_url"] = str("https://books.toscrape.com/" + image["src"])
        result["rating"] = scrap_rating(response)

    else:
        print("Code Erreur sur'response'", response)
    return result


def scrap_cat():
    links_cat = []
    response = requests.get(URL)
    if response.ok:
        soup = bS(response.text, "html.parser")
        lis = soup.find("ul", {"class": "nav nav-list"}).find("ul").findAll("li")
        for li in lis:
            a = li.find("a")
            link_cat = str(URL) + a["href"]
            links_cat.append(link_cat)
        return links_cat
    else:
        print("Code Erreur sur'response'", response)


def scrap_url_book(link_cat):
    url_books = []
    response = requests.get(link_cat)
    if response.ok:
        soup = bS(response.text, "html.parser")
        h3s = soup.findAll("h3")
        for h3 in h3s:
            a = h3.find("a")
            url_book = "https://books.toscrape.com/catalogue" + a["href"].replace("../../..", "")
            # product_page_url scrap on category page#
            url_books.append(url_book)
        return url_books
    else:
        print("Code Erreur sur'response'", response)


def scrap_rating(response):
    ratings = {"One": "1 étoile", "Two": "2 étoiles", "Three": "3 étoiles", "Four": "4 étoiles", "Five": "5 étoiles"}
    soup = bS(response.text, "html.parser")
    p = soup.find("p", {"class", "star-rating"})
    rating = ratings[p["class"][1]]
    return rating


def scrap_url_books(link_cat):
    url_books = []
    url_books.extend(scrap_url_book(link_cat))
    p = 2
    link_cat_p = link_cat + "/../page-" + str(p) + ".html"
    response = requests.get(link_cat_p)
    while response.ok:
        url_books.extend(scrap_url_book(link_cat_p))
        p = p + 1
        link_cat_p = link_cat + "/../page-" + str(p) + ".html"
        response = requests.get(link_cat_p)
    return url_books


def download_pictures(image_urls, folder):
    path = os.path.join("BooksToScrape", folder, "images")
    os.makedirs(path, exist_ok=True)
    for image_url in image_urls:
        print("Téléchargement de ", image_url)
        r = requests.get(image_url)
        file_save = os.path.join(path, image_url.split("/")[-1])

        with open(file_save, "wb") as outf:
            outf.write(r.content)


def write_csv(book_data, repertoire):
    path = os.path.join("BooksToScrape", repertoire)
    os.makedirs(path, exist_ok=True)
    path_csv = os.path.join(path, "book_to_scrap.csv")
    with open(path_csv, "w", encoding="utf-8", newline="") as outf:
        writer = csv.writer(outf, delimiter=";", quoting=csv.QUOTE_MINIMAL)
        writer.writerow(["product_page_url",
                         "universal_ product_code (upc)",
                         "title",
                         "price_including_tax",
                         "price_excluding_tax",
                         "number_available",
                         "product_description",
                         "category",
                         "review_rating",
                         "image_url"
                         ])
        for data in book_data:
            writer.writerow([data["product_page_url"],
                             data["upc"],
                             data["title"],
                             data["price_including_tax"],
                             data["price_excluding_tax"],
                             data["availability"],
                             data["product_description"],
                             data["category"],
                             data["rating"],
                             data["image_url"],
                             ])


def main():
    while True:
        command = input("Souhaitez-vous lancer le programme o/n ?")
        if command == "o":
            print("On scrap !")

            links_cat = scrap_cat()
            for link_cat in links_cat:
                images_url = []
                url_books = []
                book_data = []
                url_books.extend(scrap_url_books(link_cat))
                for url_book in url_books:
                    data = (scrap_page(url_book))
                    book_data.append(data)
                    images_url.append(data["image_url"])
                folder = link_cat.split("/")[-2]
                print(folder)
                write_csv(book_data, folder)
                download_pictures(images_url, folder)
            break
        elif command == "n":
            print("C'est vous qui voyez !")
            break
        else:
            print("Je n'ai pas compris votre demande ..")


if __name__ == "__main__":
    main()
