import requests
import csv
from bs4 import BeautifulSoup as bS

# vérifier l'installation pip -m pour requests et beautifulsoup4 #

image_urls = []

URL = "http://books.toscrape.com/"


def scrap_page(url_book):
    response = requests.get(url_book)

    if response.ok:

        soup = bS(response.text, "html.parser")

        product_description = soup.find("div", {"id", "content"}).findAll("p")[3].text

        title = soup.find("h1").text  # title scrap on product_page#

        upc = soup.findAll("td")[0].text  # universal_ product_code (upc) scrap on product_page#

        price_including_tax = soup.findAll("td")[3].text  # price_including_tax scrap on product_page#

        price_excluding_tax = soup.findAll("td")[2].text  # price_excluding_tax  scrap on product_page#

        availability = soup.findAll("td")[5].text  # Availability scrap on product_page#

        category = soup.find("ul", {"class": "breadcrumb"}).findAll("a")[2].text

        image = soup.find("div", {"class": "item active"}).find({"img": "src"})

        image_url = str("https://books.toscrape.com/" + image["src"])
        image_urls.append(image_url)

        rating = scrap_rating(url_book)
        with open("book_to_scrap.csv", "a", encoding="utf-8", newline="") as outf:
            writer = csv.writer(outf, delimiter=";", quoting=csv.QUOTE_MINIMAL)

            writer.writerow([url_book,
                             upc,
                             title,
                             price_including_tax,
                             price_excluding_tax,
                             availability,
                             product_description,
                             category,
                             rating,
                             image_url,
                             "\n"])

    else:
        print("p")


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
        print("c'est cassé")


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
        print("c'est cassé")


def scrap_rating(url_book):
    ratings = {"One": "1 étoile", "Two": "2 étoiles", "Three": "3 étoiles", "Four": "4 étoiles", "Five": "5 étoiles"}

    response = requests.get(url_book)
    if response.ok:

        soup = bS(response.text, "html.parser")
        p = soup.find("p", {"class", "star-rating"})
        rating = ratings[p["class"][1]]
        return rating

    else:
        print("erreur")


def scrap_url_books():
    url_books = []
    links_cat = scrap_cat()
    for link_cat in links_cat:
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


def download_pictures():
    for image_url in image_urls:
        print("téléchargement de ", image_url)
        r = requests.get(image_url)
        file_save = str("F:\\dossier script python\\projet_2_Scraping\\images\\" + image_url.split("/")[-1])

        with open(file_save, "wb") as outf:
            outf.write(r.content)


def read_csv():
    url_books = scrap_url_books()
    with open("book_to_scrap.csv", "w", newline="") as outf:
        writer = csv.writer(outf, delimiter=";", quoting=csv.QUOTE_MINIMAL)
        writer.writerow(["product_page_url",
                         "universal_ product_code (upc)",
                         "title",
                         "price_including_tax",
                         "price_excluding_tax",
                         "product_description",
                         "category",
                         "review_rating",
                         "image_url"
                         "\n"])
    for url_book in url_books:
        scrap_page(url_book)


def main():

    while True:
        command = input("souhaitez-vous lancer le programme o/n ?")
        if command == "o":
            print("on scrap !")

            read_csv()

            command = input("Souhaitez-vous télécharger les images o/n ?")
            if command == "o":
                download_pictures()

        elif command == "n":
            print("c'est vous qui voyez !")
            break

        else:
            print("j'ai pas compris votre demande ..")


if __name__ == "__main__":
    main()

# for save links in CSV ot txt
# with open("urls.txt or .csv","w") as file:
# for link in links:
# file.write(link +"\n")

# for import links in CSV ot txt
# with open("urls.txt or .csv","r") as file:
# for link in links:
# file.write(link +"\n")
