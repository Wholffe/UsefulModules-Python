import cv2
from pyzbar.pyzbar import decode

def main():
    cap = cv2.VideoCapture(0)
    qr_code_found = False

    while not (qr_code_found or cv2.waitKey(1) & 0xFF == ord('q')):
        _, frame = cap.read()
        decoded_objects = decode(frame)

        for obj in decoded_objects:
            data = obj.data.decode('utf-8')
            
            qr_code_text = f"QR Code: {data}"
            print(qr_code_text)

            qr_code_found = True

        cv2.imshow('QR Code Scanner', frame)

    cap.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()