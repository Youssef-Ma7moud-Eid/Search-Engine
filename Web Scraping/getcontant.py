import requests
from bs4 import BeautifulSoup
from urllib.parse import quote
from urllib.parse import unquote
import re
import subprocess

def url_to_filename(url):
    return quote(url, safe='') + ".txt"

def filename_to_url(filename):
    return unquote(filename.replace(".txt", ""))


def read_file(path):
  with open(path) as f:
    urls = [line.strip() for line in f]
  return urls

def data_cleaning(raw_text):
  # Delete blank lines
  lines = [line.strip() for line in raw_text.splitlines()]
  clean_lines = [line for line in lines if line]

  clean_text = "\n".join(clean_lines)
  # words = re.findall(r'\b\w+\b', clean_text)
  return clean_text

def get_contant(url):
  response = requests.get(url)
  soup = BeautifulSoup(response.content, "html.parser")

  # Delete unimportant elements such as => script and style.
  for tag in soup(['script', 'style']):
      tag.decompose()

  # Extract text and divide it into lines
  raw_text = soup.get_text(separator="\n")
  return raw_text


def main():
  urls = read_file('/home/hadoop/Links.txt')
  for i in range(len(urls)):
    try:
      Raw_text = get_contant(urls[i])
      Clean_text = data_cleaning(Raw_text)
      filename = url_to_filename(urls[i])
      hdfs_path = f"/user/hadoop/scraped_data/{filename}"

      proc = subprocess.run(
          ["hdfs", "dfs", "-put", "-", hdfs_path],
          input=Clean_text.encode("utf-8"),
          stdout=subprocess.PIPE,
          stderr=subprocess.PIPE)

      if proc.returncode != 0:
          print(f"Error in ({i})-> {urls[i]}: {proc.stderr.decode()}")


    except Exception as e:
        print(f"Error in ({i}): {urls[i]} -> {e}")


if __name__ == "__main__":
    main()

# hdfs dfs -mkdir -p /user/hadoop/scraped_data     <=  create folder in hdfs (scraped_data)
