# -*- encoding: utf-8 -*-
import os
import re
from bs4 import BeautifulSoup
from urllib.request import urlopen
from xml.sax.saxutils import unescape
from urllib.parse import urljoin
import unicodedata
import pickle


class Crawler:
    def __init__(self):
        pass

    def gather_links(self, links_base, links_num=200, depth=1):
        links = {}  # merge replicated link
        
        # while (len(links) < links_num):
            # new_links_base = {}
        for link_base in links_base:
            try:
                response = urlopen(link_base)
                page_elements = BeautifulSoup(response.read(), 'html5lib')
                # a_all = page_elements.find_all('a', href=True)
                a_all = page_elements.find_all(True, href=True)
                # page_elements = BeautifulSoup(response.read(), 'lxml')
                # a_all = page_elements.find_all('a', href=True)
                for a in a_all:
                    link = a['href']
                    link = link.split('#')[0]  # remove location portion

                    prefix = 'https://www.fox'
                    if re.match(prefix, link):
                        link_parts = link.split('/')
                        if (len(link_parts) > 4 and link_parts[3] != "category"):
                            if len(link_parts[-1]) > 15:
                                links[link] = 1
                            # else:
                            #     new_links_base[link] = 1
                print('Sucess on solving: %s' % link_base)
            except:
                print('Error on solving: %s' % link_base)
            # links_base = new_links_base

        return links

    def crawl(self, links, lid_base = 0):
        cnt = 1
        for (lid, link) in enumerate(links):
            try:
                # get article_body
                response = urlopen(link)
                page = BeautifulSoup(response.read(), 'html5lib')
                article_body = page.find('div', class_='article-body')

                # get article_text
                article_text = ""
                for p in article_body.find_all('p', recursive=False):
                    if p.find('strong'): continue
                    p_text = p.get_text()
                    p_clear_text = unescape(p_text)
                    article_text += str(p_clear_text) + "\n"
                    article_clean_text = unicodedata.normalize('NFKC', article_text)
                    # article_clean_text = article_text.replace('\xa0', " ")
                    # print(article_clean_text[:10])
                    # article_clean_text = article_clean_text.replace('\u3000', " ").encode()
                    # print(article_clean_text[:10])

            except:
                # info
                print("Error on link: %s" % link)

            try:
                # save article_text
                file_path = os.path.join('docs', (str(lid_base + cnt) + '.html'))
                print(file_path)
                # print(article_clean_text[:10])
                with open(file_path, 'w', encoding='UTF-8') as fp:
                    fp.write(article_clean_text)
                    cnt += 1

                # info
                print("Sucess on link: %s" % link)
            except:
                # print(article_clean_text)
                print('Second except')



if __name__ == "__main__":
    crawler = Crawler()
    # links_base = ['https://www.foxnews.com']
    links_base = [
        "https://www.foxnews.com",
        # "https://www.foxnews.com/us",
        # "https://www.foxnews.com/politics",
        # "https://www.foxnews.com/media",
        # "https://www.foxnews.com/opinion",
        # "https://www.foxnews.com/entertainment",
        # "https://www.foxnews.com/sports",
        # "https://www.foxnews.com/lifestyle",
        # "https://www.foxnews.com/shows",
        # "https://www.foxnews.com/world",
        # "https://www.foxnews.com/official-polls",
        # "https://www.foxnews.com/food-drink",
        # "https://www.foxnews.com/auto",
        # "https://www.foxnews.com/travel",
        # "https://www.foxnews.com/family",
        # "https://www.foxnews.com/science",
        # "https://www.foxnews.com/tech",
        # "https://www.foxnews.com/health",
        # "https://www.foxnews.com/compliance",
        # "https://www.foxnews.com/real-estate",
        # "https://www.foxnews.com/great-outdoors",
        ]
    links = crawler.gather_links(links_base)
    for link in links:
        print(link)
    print('Number of links: ' + str(len(links)))
    # links = ['https://www.foxnews.com/us/self-identified-antifa-members-arrive-in-twin-cities-area-as-brooklyn-center-protests-continue']
    crawler.crawl(links)
