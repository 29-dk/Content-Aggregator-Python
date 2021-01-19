import re
import requests
import os
from bs4 import BeautifulSoup
import threading
import concurrent.futures

class Scraper:

    def __init__(self,urls,action=0):
        self.scrapedData = []
        self.urls = urls
        self.action = int(action)
        self.action_mapper = {
            0 : self.thread1(),
            1 : self.thread2(),
            2 : self.thread3()
        }

    def html_parser(self,url):
        """
        Function to parse a html page as per the given url using beautifulsoup
        :param url: path to the html file
        :return: dictionary object containing url and scraped data
        """
        page = requests.get(url)
        soup = BeautifulSoup(page.content, 'html.parser')
        rtag_elements = soup.find('a', class_='articlekicker')
        rtitle_elements = soup.find('h1', class_='headline')
        if None in (rtag_elements, rtitle_elements):
            return None
        rtag_text = rtag_elements.text.strip()
        rtitle_text = rtitle_elements.text.strip()
        if not rtag_text.upper() == 'REAL ESTATE':      #To filter article related to real estate
            return None
        self.scrapedData.append({'url': url, 'title': rtitle_text})

    def thread1(self):
        for url in self.urls:
            t = threading.Thread(target=self.html_parser, args=[url])
            t.start()
        return self.scrapedData

    def thread2(self):
        with concurrent.futures.ThreadPoolExecutor() as executor:
            # Result will store the return value of the function
            result = [executor.submit(self.html_parser, url) for url in self.urls]

        for f in concurrent.futures.as_completed(result):
            print(f.result())
        return self.scrapedData

    def thread3(self):
        with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
            # map will take values from url and pass it in the func html_parser and will automatically yield result
            result = executor.map(self.html_parser, self.urls)

        # Result will store the return value of the function
        for r in result:
            print(r)
        return self.scrapedData

    def fetch_result(self):
        return self.action_mapper[self.action]


if __name__ == '__main__':
    path = os.path.abspath('sitemap_file')
    with open(path, 'r') as reader:
        line = reader.readline()

    #The base url has been extracted from sitemap_file by observing the pattern of the url
    base_url = "https://www.entrepreneur.com/article/"
    urls = re.findall(r""+base_url+"[0-9]+", line)
    scraper = Scraper(urls,2)
    print(scraper.fetch_result())  #Gives the desired result


