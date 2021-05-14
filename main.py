# This is a sample Python script.

import requests
from bs4 import BeautifulSoup as bs


##vérifier l'installation pip -m pour requests et beautifulsoup4##

def scrap_page():

    url_book = 'http://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html'  # product_page_url#
    response = requests.get(url_book)
    if response.ok:
        soup = bs(response.text)

        product_Description = soup.find('div', {'id', 'content'}).findAll('p')[3]

        upc = soup.findAll('td')[0]

        if soup.find('p', {'class', 'star-rating One'}):
            rating = "1 étoile"

        elif soup.find('p', {'class', 'star-rating Two'}):
            rating = "2 étoiles"

        elif soup.find('p', {'class', 'star-rating Three'}):
            rating = "3 étoiles"

        elif soup.find('p', {'class', 'star-rating Four'}):
            rating = "4 étoiles"

        elif soup.find('p', {'class', 'star-rating Five'}):
            rating = "5 étoiles"

        category = soup.find('ul', {'class': 'breadcrumb'}).findAll('a')[2].text

        image = soup.find('div', {'class': 'item active'}).find({'img': 'src'})

        image_Link = str('https://books.toscrape.com/' + image['src'])

        print(category)


    else:
        print(str("c'est cassé"))
# for save links in CSV ot txt
#with open('urls.txt or .csv','w') as file:
    #for link in links:
    #file.write(link +'\n')

# for import links in CSV ot txt
#with open('urls.txt or .csv','r') as file:
    #for link in links:
    #file.write(link +'\n')

url = 'http://books.toscrape.com/'                                                                 
links_cat =[]
response = requests.get(url)
if response.ok:
    soup = bs(response.text,'html.parser')
    lis = soup.find('ul', {'class': 'nav nav-list'}).find('ul').findAll('li')
    for li in lis:
        a = li.find('a')
        link_cat=a['href']
        links_cat.append(str(url + link_cat))
    print(links_cat)
    for i in range(len(links_cat)):
        response = requests.get(links_cat[i])
        if response.ok:
            soup = bs(response.text,'html.parser')
            h3s = soup.findAll('h3')
            for h3 in h3s:
                a = h3.find('a')
                url_book='https://books.toscrape.com/catalogue/' + a['href']

        else :
            print("c'est cassé")
else:
    print("c'est cassé")