import csv
import requests
from bs4 import BeautifulSoup as bs
##vérifier l'installation pip -m pour requests et beautifulsoup4##

links_cat =[]
urlBooks=[]
url = 'http://books.toscrape.com/'
url_book ='https://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html'

def scrapPage():

    with open('book_to_scrap.csv','w') as outf:

        outf.write('product_page_url ,universal_ product_code (upc), title, price_including_tax,price_excluding_tax, number_available,product_description,category,review_rating,image_url\n' )

        response = requests.get(url_book)
        if response.ok:
            soup = bs(response.text,'html.parser')

            product_Description = soup.find('div', {'id', 'content'}).findAll('p')[3].text

            title =soup.find('h1').text  #title scrap on product_page#

            upc = soup.findAll('td')[0].text  #universal_ product_code (upc) scrap on product_page#

            price_including_tax = soup.findAll('td')[3].text  #price_including_tax scrap on product_page#

            price_excluding_tax = soup.findAll('td')[2].text  # price_excluding_tax  scrap on product_page#

            Availability = soup.findAll('td')[5].text  #Availability scrap on product_page#

            category = soup.find('ul', {'class': 'breadcrumb'}).findAll('a')[2].text

            image = soup.find('div', {'class': 'item active'}).find({'img': 'src'})

            image_url = str('https://books.toscrape.com/' + image['src'])

            outf.write(url_book +',' + upc + ',' + title.replace(',','.') +','+price_including_tax.replace(',','.')
                       + ',' + price_excluding_tax.replace(',','.') + ','+ Availability +','+product_Description.replace(',',';')
                       + ',' + rating + ',' + image_url +'\n' )
            print("boucle csv")
        else:
            print('p')

def scrapCat():
    response = requests.get(url)
    if response.ok:
        soup = bs(response.text, 'html.parser')
        lis = soup.find('ul', {'class': 'nav nav-list'}).find('ul').findAll('li')
        for li in lis:
            a = li.find('a')
            link_cat = str(url) + a['href']
            links_cat.append(link_cat)
    else:
        print("c'est cassé")

def scrapUrlBook(link_cat):
    response = requests.get(link_cat)
    if response.ok:
        soup = bs(response.text,'html.parser')
        h3s = soup.findAll('h3')
        for h3 in h3s:
            a = h3.find('a')
            url_book= 'https://books.toscrape.com/catalogue' + a['href'].replace('../../..','') # product_page_url scrap on category page#
            urlBooks.append(url_book)

    else:
        print("c'est cassé")


def scrapRating(url_book):
    ratings = {'One':'1 étoile','Two':'2 étoiles','Three':'3 étoiles','Four':'4 étoiles','Five':'5 étoiles',}
    html_rating=['One','two','Three','Four','Five']
    response = requests.get(url_book)
    if response.ok:

        soup = bs(response.text, 'html.parser')
        p=soup.find('p', {'class', 'star-rating'})
        rating= ratings[p['class'][1]]
        print(rating)

    else:
        print('erreur')

def inutile():
    response_P =requests.get(links_cat[i] + '/../page-' +str(p) +'.html' )
    while response_P.ok:
                soup = bs(response_P.text,'html.parser')
                h3s = soup.findAll('h3')
                for h3 in h3s:
                    a = h3.find('a')
                    url_book= 'https://books.toscrape.com/catalogue' + a['href'].replace('../../..','')



def scrapUrlBooks():
    scrapCat()
    for link_cat in links_cat:
        scrapUrlBook(link_cat)
        p = 2
        link_cat_P = link_cat + '/../page-' + str(p) + '.html'
        response = requests.get(link_cat_P)
        if response.ok:
            scrapUrlBook(link_cat_P)
            p = p + 1
            link_cat_P = link_cat + '/../page-' + str(p) + '.html'








while True:
    command = input( 'Voulez-vous lancer le programme o/n ?' )
    if command == str('o'):
        print('on scrap !')
        scrapCat()
        for link_cat in links_cat:
            scrapUrlBook(link_cat)
            p = 2
            link_cat_P = link_cat + '/../page-' + str(p) + '.html'
            response = requests.get(link_cat_P)
            if response.ok:
                scrapUrlBook(link_cat_P)
                p = p + 1
                link_cat_P = link_cat + '/../page-' + str(p) + '.html'







    elif command == str('n'):
        print ("c'est vous qui voyez !")

    else:
        print("j'ai pas compris votre demande ..")










# for save links in CSV ot txt
#with open('urls.txt or .csv','w') as file:
    #for link in links:
    #file.write(link +'\n')

# for import links in CSV ot txt
#with open('urls.txt or .csv','r') as file:
    #for link in links:
    #file.write(link +'\n')