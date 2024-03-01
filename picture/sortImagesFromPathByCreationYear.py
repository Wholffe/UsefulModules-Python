import os
from tqdm import tqdm
import shutil
import datetime
from PIL import Image
from PIL.ExifTags import TAGS

###Settings(optional)###
image_dir = r''
sorted_image_dir = r''

###Script###
while image_dir == '':
    image_dir = input('Path you want to sort images by year: ')
while sorted_image_dir == '':
    sorted_image_dir = input('Destination path for sorted images: ')

movable_files = []
file_list = os.listdir(image_dir)

def get_capture_date(image_path):
    try:
        with Image.open(image_path) as img:
            exif_data = img._getexif()
            if exif_data:
                for tag, value in exif_data.items():
                    tag_name = TAGS.get(tag, tag)
                    if tag_name == 'DateTimeOriginal':
                        capture_date = datetime.datetime.strptime(value, '%Y:%m:%d %H:%M:%S')
                        return str(capture_date.year)
            return None
    except Exception as e:
        print(f"Error finding DateTimeOriginal: {str(e)}")
        return None
    
def move_files_from_list(file_list, sorted_image_dir):
    for filename in tqdm(file_list):
        file_path = os.path.join(image_dir, filename)
        new_file_path = os.path.join(sorted_image_dir, filename)

        if not os.path.exists(new_file_path):
            shutil.move(file_path, new_file_path)

def create_unknown_dir(target_dir):
    unknown_year_dir = os.path.join(target_dir,'Unknown Year')
    if not os.path.exists(unknown_year_dir):
        os.makedirs(unknown_year_dir)
    return unknown_year_dir

def main():
    if os.path.exists(image_dir):
        print('Please enter a valid path')
        return
    for file in tqdm(file_list):
        file_path = os.path.join(image_dir,file)
        try:
            creation_year = get_capture_date(file_path)
        except:
            continue
        if not creation_year:
            unknown_dir = create_unknown_dir(sorted_image_dir)
            shutil.move(file_path,unknown_dir)
            continue

        new_dir = os.path.join(sorted_image_dir,creation_year)
        if not os.path.exists(new_dir):
            os.makedirs(new_dir)
        shutil.move(file_path, new_dir)

if __name__=='__main__':
    main()
