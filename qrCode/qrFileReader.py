from pyzbar.pyzbar import decode
import cv2
import os

###Settings###
image1_dir = r"<add/your/file_or_folderpath/here>"

###Script###
def main(image_dir:str):
    if not os.path.exists(image1_dir):
        print('Path does not exist')
        return

    qr_code_found = False
    image = cv2.cvtColor(cv2.imread(image_dir), cv2.COLOR_BGR2RGB)
    decoded_objects = decode(image)

    for obj in decoded_objects:
        data = obj.data.decode('utf-8')
        
        qr_code_text = f"QR Code: {data}"
        print(qr_code_text)
        
        qr_code_found = True

    if not qr_code_found:
        print('no qr code detected')
    
if __name__ == '__main__':
    main(image1_dir)