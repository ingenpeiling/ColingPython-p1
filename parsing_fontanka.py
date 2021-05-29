import requests
from bs4 import BeautifulSoup as bs
import re
import csv
import datetime

base_link = "https://www.fontanka.ru/"

base = datetime.date.today()
numdays = 365
date_list = [(base - datetime.timedelta(days=x)).strftime("%Y/%m/%d") for x in range(numdays)]

for item in date_list:
    date = item
    print_date = ''.join([char for char in date if char != "/"])
    
    link = f'{base_link}{date}/all.html'
    page = requests.get(link)
    soup = bs(page.content)
    news = soup.findAll('a', {'class':'CFhf'})

    for num, item in enumerate(news):

        news_link = item['href']
        future_text = requests.get(base_link + news_link)
        text_soup = bs(future_text.content)

        text = text_soup.findAll('section', {'itemprop':'articleBody'})
        sect = re.findall('[a-zA-Z]+(?=" property="fnt:rubric"/>)', str(text_soup))
        try:
            b = text[0]
        except:
            pass
        parags = b.findAll('p')

        final_text = ''.join([str(par.get_text()) for par in parags])

        with open(f'C:\\Users\\Asus\\corp\\art{print_date}{num}.tsv', 'wt', encoding='utf8') as file:
            tsv_writer = csv.writer(file, delimiter='\t')
            tsv_writer.writerow(['date', 'section', 'link', 'text'])
            tsv_writer.writerow([date, sect, news_link, final_text])
