import pandas as pd
from bs4 import BeautifulSoup
import requests
import os


df = pd.read_excel("/content/drive/MyDrive/Colab Notebooks/Data/Output Data Structure.xlsx")

# Function to scrape article title and text
# Website structure was analyzed and classes were identified accordingly to extract the title and article text

def scrape_title_article(link):
    response = requests.get(link)
    # print(response.status_code)
    soup = BeautifulSoup(response.text, 'html.parser')

    if soup.find('div', class_='td-post-content') and soup.find('h1', class_='entry-title'):
        title = soup.find('h1', class_='entry-title').text
        article = soup.find('div', class_='td-post-content').text
    elif soup.find('div', class_='td-post-content') and soup.find('h1', class_='tdb-title-text'):
        title = soup.find('h1', class_='tdb-title-text').text
        article = soup.find('div', class_='td-post-content').text
    elif response.status_code == 404:
        title = 'response.status_code == 404'
        article = 'content was not found'
    return title, article


#function to create the text files and save on the specified directory
def create_txt_and_save(filename, title, article):
  output_dir="/content/drive/MyDrive/Colab Notebooks/Data/BlackcofferDataExtraction_Analysis/Articles_txt_files"
  filename = f"{filename}.txt"
  file_path = os.path.join(output_dir, filename)
  with open(file_path, 'w') as file:
      file.write(f"{title}\n\n")
      file.write(article)


# Lopp to go ver each row in df, scrape the data, and save the text file
for url_id, url in zip(df['URL_ID'],df['URL']):
  print(url_id,url)
  filename = url_id

  #scrape the web
  title,article = scrape_title_article(url)

  #write and save the text file
  create_txt_and_save(filename,title,article)
  print(f"file {filename} is created successfully")




