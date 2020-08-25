import requests
from bs4 import BeautifulSoup
import re
from word2number import w2n
import pandas as pd

def scrap_catalogue(csv_file):
    data = []
    for i in range(1, 51): 
        raw = BeautifulSoup(requests.get('http://books.toscrape.com/catalogue/page-'+str(i)+'.html').content, 'html.parser').find('ol', {'class', 'row'}).findAll('li')
        [data.append([j.find('h3').find('a')['title'], j.find('p', {'class':'price_color'}).text, w2n.word_to_num(re.search('<p class=\"star-rating \w+\">', str(j)).group().replace('<p class=\"star-rating ', '').replace('\">', '')), j.find('p', {'class':'instock availability'}).text.strip()]) for j in raw]
        print(i, '/50 scrapped')
    dataframe = pd.DataFrame(data, columns =['book name', 'price', 'rating', 'instock availability']) 
    dataframe.to_csv(csv_file, index=False, header=True)

def scrap_details(csv_file):
    data = []

    for i in range(1, 51): 
        raw = BeautifulSoup(requests.get('http://books.toscrape.com/catalogue/page-'+str(i)+'.html').content, 'html.parser').find('ol', {'class', 'row'}).findAll('li')
        for k in ['http://books.toscrape.com/catalogue/'+j.find('a')['href'] for j in raw]:
            d_raw = BeautifulSoup(requests.get(k).content, 'html.parser').find('div', {'class': 'content'})
            title = d_raw.find('h1').text
            rating = w2n.word_to_num(re.search('<p class=\"star-rating \w+\">', str(d_raw)).group().replace('<p class=\"star-rating ', '').replace('\">', ''))
            UPC, product_type, price_excl_tax, price_incl_tax, tax, availability, number_of_reviews = [l.find('td').text for l in  d_raw.find('table', {'class': 'table table-striped'}).findAll('tr')]
            data.append([title, rating, UPC, product_type, price_excl_tax, price_incl_tax, tax, availability, number_of_reviews])
            print(title)
        print(i, ' / 50')

    dataframe = pd.DataFrame(data, columns =['book name', 'rating', 'UPC', 'product type', 'price exclude tax', 'price include tax', 'tax', 'availability', 'number of reviews']) 
    dataframe.to_csv(csv_file, index=False, header=True)
