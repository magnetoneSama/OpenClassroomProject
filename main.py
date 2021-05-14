

import requests
from bs4 import BeautifulSoup as bs


##vérifier l'installation pip -m pour requests et beautifulsoup4##

def scrap_page():

    with open('book_to_scrap.csv','w', newline='') as outf:
        outf.writeraw('product_page_url ,universal_ product_code (upc), title, price_including_tax,price_excluding_tax, number_available,product_description,category,review_rating,image_url\n' )
        response = requests.get(url_book)
        if response.ok:
            soup = bs(response.text,'html.parser')

            product_Description = soup.find('div', {'id', 'content'}).findAll('p')[3].text

            title =soup.find('h1').text  #title scrap on product_page#

            upc = soup.findAll('td')[0].text  #universal_ product_code (upc) scrap on product_page#

            price_including_tax = soup.findAll('td')[3].text  #price_including_tax scrap on product_page#

            price_excluding_tax = soup.findAll('td')[2].text  # price_excluding_tax  scrap on product_page#

            Availability = soup.findAll('td')[5].text  #Availability scrap on product_page#


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
             #rewiew_rating scrap on product_page, i can optimize if and elif in dictionary#

            category = soup.find('ul', {'class': 'breadcrumb'}).findAll('a')[2].text

            image = soup.find('div', {'class': 'item active'}).find({'img': 'src'})

            image_url = str('https://books.toscrape.com/' + image['src'])

            outf.write(url_book +',' + upc + ',' + title.replace(',','.') +','+price_including_tax.replace(',','.')
                       + ',' + price_excluding_tax.replace(',','.') + ','+ Availability +','+product_Description.replace(',',';')
                       + ',' + rating + ',' + image_url +'\n' )
            print("boucle csv")



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
                url_book= 'https://books.toscrape.com/catalogue' + a['href'].replace('../../..','') # product_page_url scrap on category page#
                scrap_page()
            p=1
            response_P =requests.get(links_cat[i] + '/../page-' +str(p) +'.html' )
            while response_P.ok:
                soup = bs(response_P.text,'html.parser')
                h3s = soup.findAll('h3')
                for h3 in h3s:
                    a = h3.find('a')
                    url_book= 'https://books.toscrape.com/catalogue' + a['href'].replace('../../..','')
                    scrap_page()

        else :
            print("c'est cassé")
else:
    print("c'est cassé")