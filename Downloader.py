from bs4 import BeautifulSoup
from urllib import parse
import urllib.request as req
import sys

opener = req.build_opener()
opener.addheaders = [('User-Agent',
                      'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1941.0 Safari/537.36')]
req.install_opener(opener)


class HtmlMp3Parser:

    def __init__(self, web_page):

        self.web_page_url = req.Request(web_page)

    def get_links(self):
        links = []
        html_page = req.urlopen(self.web_page_url)
        soup = BeautifulSoup(html_page, "lxml")

        for link in soup.findAll('a'):
            href = link.get('href')
            if href is not None and href.endswith(".mp3"):
                links.append(href)
        return links


class Downloader:

    def __init__(self, link):
        self.link = link

    @staticmethod
    def extract_file_name(encoded_url):
        if not encoded_url:
            return None
        last_slash_index = encoded_url.rfind("/") + 1
        encoded_file_name = encoded_url[last_slash_index:]
        return parse.unquote(encoded_file_name)

    def save_file(self):
        file_name = self.extract_file_name(self.link)
        print("Downloading... " + file_name)
        try:
            req.urlretrieve(self.link, file_name)
        except req.HTTPError as e:
            print("Could not download file " + file_name + " Reason " + str(e.code))
            pass


if __name__ == '__main__':
    web_page = sys.argv[1]
    print("Downloading from")
    print(web_page)
    html_parser = HtmlMp3Parser(web_page)
    links = html_parser.get_links()
    for link in links:
        downloader = Downloader(link)
        downloader.save_file()
    print("Completed all your downloads....")
