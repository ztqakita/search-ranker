# -*- encoding: utf-8
from bs4 import BeautifulSoup
from urllib.request import urlopen
from xml.sax.saxutils import unescape
import src.util as util
from urllib.parse import urljoin
from nltk.util import clean_html
import unicodedata
import os
import re
import json


class Crawler:
    def __init__(self, fid_base=0):
        self.fid_base = fid_base
        self.json_dict = {}

    def gather_links(self, root_link, basic_links, links_max=200):
        links = {}  # merge replicated link

        for basic_link in basic_links:
            topic = basic_link.split('/')[-1]
            try:
                response = urlopen(basic_link)
                page = BeautifulSoup(response.read(), 'html5lib')
                # page = BeautifulSoup(response.read(), 'lxml')
                href_elements = page.find_all(True, href=True)
                for href_element in href_elements:
                    link = href_element['href']
                    # print('Pre: ' + link)
                    link = link.split('#')[0]  # remove location portion

                    if re.match('/' + topic, link):
                        link = root_link + link

                    if re.match(root_link + '/' + topic + '/', link):
                        # print('In: ' + link)
                        links[link] = 1
                print('Sucess on solving. [link: %s]' % basic_link)
            except:
                print('Error on solving. [link: %s]' % basic_link)

        return links

    def clean_text(self, text):
        text = unescape(text)
        text = unicodedata.normalize('NFKC', text)
        return text

    def crawl(self, links):

        f_cnt = 1
        for link in links:
            article_description = {}
            link_dict = {}
            # fetch article
            try:
                response = urlopen(link)
                page = BeautifulSoup(response.read(), 'html5lib')

                article_description_str = page.find('script', type='application/ld+json').get_text()
                article_description = json.loads(article_description_str)

                # get article_body
                article_body = page.find('div', class_='article-body')
                # get article_text
                article_text = ''
                for p in article_body.find_all('p', recursive=False):
                    if p.find('strong'):  # remove image portion
                        continue
                    p_text = self.clean_text(p.get_text())
                    article_text += str(p_text) + '\n'
                if article_text == '':
                    print('Skip empty article. [link: %s]' % link)
                    continue
                # print('Success on article fetch. [link: %s]' % link)
            except:
                print('Error on article fetch. [link: %s]' % link)
                continue
            # save article
            try:
                fid = self.fid_base + f_cnt
                file_name = str(fid) + '.html'
                file_path = os.path.join('.', 'docs', file_name)
                print("Saving article to file_path '%s'" % file_path)
                with open(file_path, 'w', encoding='UTF-8') as fp:
                    fp.write(article_text)
                f_cnt += 1
                # print('Success on article saving. [link: %s]' % link)
            except:
                print('Error on article saving. [link: %s]' % link)
                continue

            link_dict['topic'] = link.split('/')[3]
            link_dict['headline'] = article_description['headline']
            link_dict['datePublished'] = article_description['datePublished']
            link_dict['url'] = link
            self.json_dict[fid] = link_dict
            print('Success on crawling. [link: %s]' % link)
        link_dict_path = os.path.join('.', 'linkInfo.json')
        util.write2JSON(self.json_dict, link_dict_path)

    def run(self, root_link, basic_links):
        links = self.gather_links(root_link, basic_links)
        print('Gathering finished.')

        print('[ Number of links: ' + str(len(links)) + ' ]')

        self.crawl(links)
        print('Crawling finished.')


if __name__ == '__main__':
    crawler = Crawler()
    root_link = 'https://www.foxnews.com'
    basic_links = [
        # 'https://www.foxnews.com/us',
        'https://www.foxnews.com/politics',
        'https://www.foxnews.com/entertainment',
        'https://www.foxnews.com/sports',
        'https://www.foxnews.com/lifestyle',
        'https://www.foxnews.com/world',
        'https://www.foxnews.com/food-drink',
        'https://www.foxnews.com/travel',
        'https://www.foxnews.com/family',
        'https://www.foxnews.com/science',
        'https://www.foxnews.com/tech',
        'https://www.foxnews.com/health',
        'https://www.foxnews.com/real-estate',
        'https://www.foxnews.com/great-outdoors',
    ]
    crawler.run(root_link, basic_links)
