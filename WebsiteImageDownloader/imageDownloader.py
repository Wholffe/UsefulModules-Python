import os
import requests
from bs4 import BeautifulSoup

###Settings###
path = r"A:\your\path"
url = ""
min_image_width = 600
min_image_height = 600

###Script###
def makeHomeUrl(url:str):
    https = "https://"
    home_url = url.removeprefix(https).split("/", 1)[0]
    return https + home_url

def download_image(url:str, filename:str):
    try: 
        response = requests.get(url)
        if response.status_code == 200:
            with open(filename, "wb") as f:
                f.write(response.content)
                print(f"Picture '{filename}' downloaded.")
        else:
            print(f"Error downloading from '{url}', statuscode: {response.status_code}")
    except Exception as e:
        print(f"Error downloading from '{url}': {e}")

def remove_suffix_if_present(filename:str, suffix:str):
    if filename.endswith(suffix):
        return filename[:-len(suffix)]
    return filename

def main(path:str, url:str, min_image_width:int,min_image_height:int):
    if not os.path.exists(path):
        print('Error: Path does not exist')
        return

    try:
        response = requests.get(url)
    except Exception as e:
        print(e)
        return
    soup = BeautifulSoup(response.text, "html.parser")
    img_tags = soup.find_all("img")

    for img in img_tags:
        img_url = img["src"]
        if not img_url.startswith(("http:", "https:")):
            img_url = makeHomeUrl(url) + img_url
            
        response = requests.head(img_url)
        if response.status_code != 200:
            continue

        headers = response.headers
        content_length = int(headers.get("content-length", 0))
        content_type = headers.get("content-type", "")

        if content_length > 0 and "image" in content_type:
            width = int(headers.get("x-image-width", 0))
            height = int(headers.get("x-image-height", 0))
            
            if not (width >= min_image_width and height >= min_image_height):
                continue

        linked_img_url = None
        for link_tag in img.find_parents("a"):
            linked_img_url = link_tag.get("href")
            if linked_img_url and linked_img_url.lower().endswith((".png", ".jpg", ".jpeg")):
                break

        if linked_img_url:
            linked_filename = os.path.join(path, linked_img_url.split("/")[-1])
            linked_filename = remove_suffix_if_present(linked_filename, "_")
            download_image(linked_img_url, linked_filename)
        else:
            filename = os.path.join(path, img_url.split("/")[-1])
            filename = remove_suffix_if_present(filename, "_")
            download_image(img_url, filename)

if __name__ == "__main__":
    main(path, url, min_image_width, min_image_height)