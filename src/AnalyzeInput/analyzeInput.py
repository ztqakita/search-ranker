import re
import urllib.request

from bs4 import BeautifulSoup
from urllib.parse import urljoin


class crawler:
    def __init__(self):
        self.doclist = {}
        self.doc_number = 0

    def get_entry_id(self):
        return None

    def seperate_words(self, text):
        splitter = re.compile('\\W*')
        return [s.lower() for s in splitter.split(text) if s != '']

    def add2index(self, url, soup):
        if self.is_indexed(url): return
        print('Indexing ' + url)

        # Get the individual words
        text = self.get_text(soup)
        return text
        # words = self.seperate_words(text)
        # print(words)
        # # Get the URL id
        # urlid = self.get_entry_id('urllist', 'url', url)
        #
        # # Link each word to this url
        # for i in range(len(words)):
        #     word = words[i]
        #     wordid = self.get_entry_id('wordlist', 'word', word)
        #     self.con.execute("insert into wordlocation(urlid,wordid,location) values (%d,%d,%d)" % (urlid, wordid, i))

    def get_text(self, soup):
        v = soup.find_all('p')

        if v == None:
            c = soup
            result_text = ''
            for t in c:
                subtext = self.get_text(t)
                result_text += subtext + '\n'
            return result_text
        else:
            return v.strip()

    def is_indexed(self, url):
        # for doc in self.doclist:
        #     if url == self.doclist[doc]['url']:
        #         return False
        # return True
        return False

    def add_link_ref(self, url_from, url_to, link_text):
        pass

    def crawl(self, pages, depth=100):
        for i in range(depth):
            newpages = {}
            for page in pages:
                try:
                    c = urllib.request.urlopen(page)
                except:
                    print('Cannot open %s' % page)
                    continue
                try:
                    print(1)
                    soup = BeautifulSoup(c.read(), 'html.parser')
                    print(soup.find_all('p').get_text())
                    link_text = self.add2index(page, soup)
                    doc = {'url': page, 'text': link_text}
                    print(link_text)
                    self.doclist[self.doc_number] = doc
                    # print(soup.a)
                    links = soup.find_all('a')
                    for link in links:
                        # print(dict(link.attrs))
                        if 'href' in dict(link.attrs):
                            url = link['href']
                            if url.find("'") != -1:
                                continue
                            url = url.split('#')[0]  # remove location portion
                            if url[24:28] != 'cate' and url[0:24] == 'https://www.foxnews.com/' and len(
                                    url) >= 50 and not self.is_indexed(url):
                                newpages[url] = 1
                            # self.addlinkref(page, url, linkText)
                except:
                    print("Could not parse page %s" % page)
            pages = newpages


page_list = ['https://www.foxnews.com/us/live-updates-minnesota-police-and-protesters-clash-following-daunte-wright-fatal-shooting']
crawler = crawler()
crawler.crawl(page_list)
