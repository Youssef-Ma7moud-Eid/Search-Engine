from WEB_CRAWLER_AND_PAGE_RANK.features.pagerank import PageRank
from WEB_CRAWLER_AND_PAGE_RANK.features.web_crawler import WebCrawler


initial_links = ['https://www.dailynewsegypt.com/', 'https://www.geeksforgeeks.org/']


if __name__ == '__main__':

    Crawler = WebCrawler(max_links=1000)
    Crawler.crawling(initial_links)

    page = PageRank()
    print(page.page_rank())