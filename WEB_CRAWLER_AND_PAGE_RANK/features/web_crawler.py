
from encryption.encode import encode_url
from collections import *  # queue
import re     # Regular Expression (RE)  => cleaned text
import requests

""" 
bs4 refers to the # Beautiful Soup #library ,
which is commonly used for web scraping tasks. 
It provides a convenient way to parse and extract data from HTML and XML documents.
Install =>  pip install beautifulsoup4
"""
import bs4
'''
html2text is a library that allows you to convert HTML content into plain text.
Install =>  pip install html2text
'''
import html2text



class WebCrawler:
    def __init__(self, max_links):
        self.queue = deque()
        self.visited = set()
        self.neighbours = []
        self.max_links = max_links  # Maximum number of links to retrieve
        self.datasetsPath = 'C:/Users/LAPTOP/OneDrive/Desktop/page_rank/datasets'

    def crawling(self, initial_links):
        self.queue.extend(initial_links)   # []
        self.get_all_links_in_page()       # max  [100] =>
        self.save_all_links_in_file()
        self.parse_pages_into_text()
        self.get_neighbours_urls()        # ??????
    def get_all_links_in_page(self):
        page_counter = 0
        links_counter = 1
        #           0           <     100 0               []
        while len(self.visited) < self.max_links and self.queue:
            print('####################### New page #################################', page_counter)
            try:
                current_link = self.queue.popleft()  #   BFS
                # Send an HTTP GET request
                res = requests.get(current_link)
                # Check the response status code
                if res.status_code == 200:   # HTTP status code, it means "OK"  =>  The server successfully answered the http request
                    # Create a BeautifulSoup object
                    soup = bs4.BeautifulSoup(res.text, 'html.parser')
                    self.visited.add(current_link)
                    # Find all hyperlinks in the page
                    for link in soup.find_all('a', href=True): # <a>
                        # The links Counter is not equal to Max Links.
                        # The href attribute of the link starts with "https://".
                        # Add unvisited pages found in hyperlinks to the List
                        if len(self.visited) < self.max_links and link['href'].startswith('https://') and link['href'] not in self.visited:
                            print('--------------- link number --------------', links_counter)
                            print(link['href'])   # link
                            self.queue.append(link['href'])
                            links_counter += 1
                    else:
                        page_counter += 1
                else:
                    print('Request failed with status code:', res.status_code)
                    page_counter += 1
            except Exception as e:
                print('Exception:', str(e))
                page_counter += 1

    def parse_pages_into_text(self):
        for link in self.visited:
            try:
                res = requests.get(link)
                if res.status_code == 200:
                    soup = bs4.BeautifulSoup(res.text, 'html.parser')
                    output = html2text.html2text(soup.text) # Convert HTML to plain text
                    cleaned_text = re.sub(r"[^a-zA-Z\s]", " ", output)
                    nameFile = encode_url(link)
                    self.save_the_text_to_a_file(nameFile, cleaned_text)
                else:
                    print('Request failed with status code:', res.status_code)
            except Exception as e:
                print('Exception:', str(e))

    def save_the_text_to_a_file(self, namefile, cleaned_text):
        try:
            with open(f"{self.datasetsPath}\\{namefile}.txt", 'w') as file:
                file.write(cleaned_text)
                print("----- Saved successfully -----")
        except IOError:
            print("--- An error occurred while saving the links to the file ---")

    def save_all_links_in_file(self):
        try:
            with open(f'{self.datasetsPath}\\test.txt', 'w') as file:
                file.write('\n'.join(self.visited))
            print("----- Links saved successfully -----")
        except IOError:
            print("--- An error occurred while saving the links to the file ---")

    def get_neighbours_urls(self):
        # Code for checking links
        page_counter = 0
        # [{0,2},set]
        self.neighbours = [set() for _ in range(len(self.visited))] # Create an empty sublist for each link
        links = list(self.visited)
        # Repeat until empty queue or reach the maximum number required
        for Link in links:
            try:
                # Send an HTTP GET request
                res = requests.get(Link)
                # Check the response status code
                if res.status_code == 200:  # HTTP status code, it means "OK"  =>  The server successfully answered the http request
                    # Create a BeautifulSoup object
                    soup = bs4.BeautifulSoup(res.text, 'html.parser')
                    # Find all hyperlinks in the page
                    for link in soup.find_all('a', href=True):
                        if link['href'].startswith('https://') and link['href'] in self.visited:
                            index_link_in_list = links.index(link['href'])  # 0  2
                            self.neighbours[page_counter].add(index_link_in_list)
                    page_counter += 1
                else:
                    # Request encountered an error
                    print('Request failed with status code:', res.status_code)
                    page_counter += 1
            except Exception as e:
                print('Exception:', str(e))
                page_counter += 1

        self.save_neighbours_urls()

    def save_neighbours_urls(self):
        try:
            with open(f'{self.datasetsPath}\\neighbours.txt', 'w') as file:
                for index, s in enumerate(self.neighbours):
                    neighbors_str = ', '.join(str(elem) for elem in s)
                    file.write(f"{index}: {neighbors_str}\n")
            print("File saved successfully.")
        except Exception as e:
            print(f"An error occurred while saving the file: {str(e)}")





# webCrawler = WebCrawler(max_links=10)
# initial = ['https://www.dailynewsegypt.com/', 'https://www.oracle.com/eg/big-data/what-is-big-data/' ]
# webCrawler.crawling(initial)