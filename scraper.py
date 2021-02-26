import requests
from bs4 import BeautifulSoup
import re
def get_links(url, articles = []):
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    for link in soup.findAll('a', attrs={'href': re.compile("^http://")}):
        if 'title' in link.attrs:
            if link.get('class')[0] == 'blog-pager-older-link':
                _ = get_links(link.get('href'), articles)
                continue
            if link.get('class')[0] == 'timestamp-link':
                articles.append(extract_text_from_page(link.get('href')))
    return articles

def extract_text_from_page(url):
    data = []
    paragraphs = []  # a list that containts each paragprah of text 
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    title = soup.title.text
    data.append(title[title.find(':')+2:])
    #ne uzimaj u obzir komentare
    post = soup.find_all("div", {"class:", "post hentry"})
    for element in post[0].stripped_strings:
        #ako je tekst duzi od 100 karaktera onda je paragraf iz teksta kojeg trazimo ka amo rec
        if(len(element) > 100):
            paragraphs.append(element)
    data.append(" ".join(paragraphs))
    return data

artikli = get_links("http://www.atlanteanconspiracy.com/search/label/Flat%20Earth?updated-max=2020-11-17T22:07:00-08:00&max-results=20&start=2&by-date=false")
