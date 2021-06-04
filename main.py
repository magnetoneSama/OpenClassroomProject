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
        result["rating"] = scrap_rating(url_book)

    else:
        print("p")
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


def download_pictures(image_urls):
    os.makedirs("images", exist_ok=True)
    for image_url in image_urls:
        print("téléchargement de ", image_url)
        r = requests.get(image_url)
        file_save = str("images\\" + image_url.split("/")[-1])

        with open(file_save, "wb") as outf:
            outf.write(r.content)


def write_csv(book_data, repertoire):
    os.makedirs(repertoire, exist_ok=True)
    path = repertoire + "\\book_to_scrap.csv"

    with open(path, "w", encoding="utf-8", newline="") as outf:
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
        command = input("souhaitez-vous lancer le programme o/n ?")
        if command == "o":
            print("on scrap !")
            images_url = []
            links_cat = scrap_cat()
            for link_cat in links_cat:
                url_books = []
                book_data = []
                url_books.extend(scrap_url_books(link_cat))
                for url_book in url_books:
                    data = (scrap_page(url_book))
                    book_data.append(data)
                    images_url.append(data["image_url"])
                print(link_cat.split("/")[-2])
                write_csv(book_data, link_cat.split("/")[-2])
            download_pictures(images_url)
            break
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
