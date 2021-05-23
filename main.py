import requests
from bs4 import BeautifulSoup as bs
##vérifier l'installation pip -m pour requests et beautifulsoup4##

links_cat =[]
urlBooks=[]
image_urls =['https://books.toscrape.com/../../media/cache/6d/41/6d418a73cc7d4ecfd75ca11d854041db.jpg','https://books.toscrape.com/media/cache/fe/72/fe72f0532301ec28892ae79a629a293c.jpg']
url = 'http://books.toscrape.com/'


def scrapPage():
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
        image_urls.append(image_url)


        rating = scrapRating()





        outf.write(url_book +',' +
                   upc + ',' +
                   title.replace(',','.') +','+
                   price_including_tax.replace(',','.') + ',' +
                   price_excluding_tax.replace(',','.') + ','+
                   Availability +','+
                   product_Description.replace(',',';')+ ',' +
                   category + ',' +
                   rating + ',' +
                   image_url +'\n' )

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


def scrapRating():
    ratings = {'One':'1 étoile','Two':'2 étoiles','Three':'3 étoiles','Four':'4 étoiles','Five':'5 étoiles',}

    response = requests.get(url_book)
    if response.ok:

        soup = bs(response.text, 'html.parser')
        p=soup.find('p', {'class', 'star-rating'})
        rating = ratings[p['class'][1]]
        return rating

    else:
        print('erreur')





def scrapUrlBooks():
    scrapCat()
    for link_cat in links_cat:
        scrapUrlBook(link_cat)
        p = 2
        link_cat_P = link_cat + '/../page-' + str(p) + '.html'
        response = requests.get(link_cat_P)
        while response.ok:

            scrapUrlBook(link_cat_P)
            p = p + 1
            link_cat_P = link_cat + '/../page-' + str(p) + '.html'
            response = requests.get(link_cat_P)









while True:
    command = input( 'souhaitez-vous lancer le programme o/n ?' )
    if command == str('o'):
        print('on scrap !')
        scrapUrlBooks()
        with open('book_to_scrap.csv', 'w',encoding="utf-8") as outf:

            outf.write(
                'product_page_url,'
                'universal_ product_code (upc),'
                'title,'
                'price_including_tax,price_excluding_tax,'
                'number_available,product_description,'
                'category,'
                'review_rating,'
                'image_url'
                '\n')
            for url_book in urlBooks:
                scrapPage()
        command = input( 'Souhaitez-vous télécharger les images o/n ?' )
        if command == str('o'):
            for image_url in image_urls:
                print('téléchargement de ',image_url)
                r= requests.get(image_url)

                with open('/images','wb') as outf:
                    outf.write(r.content)












    elif command == str('n'):
        print ("c'est vous qui voyez !")
        for image_url in image_urls:
            print('téléchargement de ', image_url)
            r = requests.get(image_url)
            file_save ='F:\dossier script python\projet_2_Scraping\images\\'+ image_url.split('/')[-1]


            with open(file_save, 'wb') as outf:
                outf.write(r.content)

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