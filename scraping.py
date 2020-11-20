import re
import requests
from bs4 import BeautifulSoup

path = 'C:/Users/dk291/Study Material/entrepreneur_xml_file.txt'

with open(path,'r') as reader:
    line = reader.readline()

urls = re.findall(r"https://www.entrepreneur.com/article/[0-9]+",line)
scrapedData = []

for url in urls:
    page = requests.get(url)
    soup = BeautifulSoup(page.content,'html.parser')
    rtag_elements = soup.find('a',class_='articlekicker')
    rtitle_elements = soup.find('h1',class_='headline')
    if None in (rtag_elements,rtitle_elements):
        continue
    rtag_text = rtag_elements.text.strip()
    rtitle_text = rtitle_elements.text.strip()
    if not rtag_text.upper() == 'REAL ESTATE':
        continue
    scrapedData.append({'url':url,'title':rtitle_text})
