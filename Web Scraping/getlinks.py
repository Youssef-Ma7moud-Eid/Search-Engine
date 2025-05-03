import requests
from bs4 import BeautifulSoup
import pandas as pd

URLs = ('https://www.geeksforgeeks.org/',
        'https://www.freecodecamp.org/news/',
        'https://www.coursera.org',
        'https://www.udemy.com/',
        'https://www.w3schools.com/',
        'https://edition.cnn.com/',
        'https://stackoverflow.com/questions',
        'https://www.nytimes.com/',
        'https://exercism.org/',
        'https://www.codingame.com/start',
        'https://weworkremotely.com/categories/remote-programming-jobs',
        'https://www.bbc.com/news/technology',
        'https://www.programiz.com',
        'https://www.npr.org',
        'https://www.edx.org',
        'https://en.wikipedia.org',
        'https://apnews.com',
        'https://www.nfl.com/',
        'https://wuzzuf.net/jobs/egypt'
        )

def Get_all_links(main_url , links , total_links):

    TLD = {'com','net','org','edu'}

    for i in links :
      href = i['href']
      if href and main_url:
        if " " in href :
          continue
        if href.startswith('https') :
          total_links.add(href)

        else:
          for i in TLD:
            if i in main_url :
              total_links.add(main_url[:main_url.find(i)] + i + href)
              break
            
            
def scrape(URLs):
  total_links = set()
  for url in URLs:
    try:
      respons = requests.get(url.strip())
      soup = BeautifulSoup(respons.content,'lxml')
      total_links.add(url)
      links = soup.find_all('a',href=True)
      Get_all_links(url , links , total_links)

    except :
      continue
  return total_links



def main():
    Total_Links = scrape(scrape(URLs))

    Links = pd.DataFrame(Total_Links, columns=['URLs'])

    Links.to_csv('Links.csv', index=False)
    Links.to_csv("Links.txt", index=False, sep='\n')

if __name__ == "__main__":
    main()
