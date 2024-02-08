import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse

### Settings ###
path = r"D:\Downloads\imageDownloader"  # Directory to save the images
url = ""  # URL of the website to download images from
min_image_width = 600  # Minimum image width in px
min_image_height = 600  # Minimum image height in px

### Script ###
def download_image(url, filename):
    try: 
        response = requests.get(url)
        if response.status_code == 200:
            with open(filename, "wb") as f:
                f.write(response.content)
                print(f"Image '{filename}' downloaded.")
        else:
            print(f"Error downloading from '{url}', status code: {response.status_code}")
    except Exception as e:
        print(f"Error downloading from '{url}': {e}")

def make_absolute_url(base_url, url):
    return urljoin(base_url, url)

def remove_suffix_if_present(filename, suffix):
    if filename.endswith(suffix):
        return filename[:-len(suffix)]
    return filename

def main(url, path, min_image_width, min_image_height):
    if not os.path.exists(path):
        os.makedirs(path)
        print(f"Directory '{path}' created.")

    try:
        response = requests.get(url)
        response.raise_for_status()
    except Exception as e:
        print(f"Error fetching website '{url}': {e}")
        return
    
    base_url = response.url
    soup = BeautifulSoup(response.content, "html.parser")
    img_tags = soup.find_all("img")

    for img in img_tags:
        img_url = img.get("src")
        if not img_url:
            continue
        img_url = make_absolute_url(base_url, img_url)

        filename = os.path.join(path, os.path.basename(urlparse(img_url).path))
        filename = remove_suffix_if_present(filename, "_")
        download_image(img_url, filename)

if __name__ == "__main__":
    main(url, path, min_image_width, min_image_height)
