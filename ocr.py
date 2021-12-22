import cv2
import pytesseract

# pytesseract application path
pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'

# # get image path and read it
# img = cv2.imread('Capture.png')
# # convert from BGR to RGB
# img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
# # apply OCR and show result
# print('res = ', pytesseract.image_to_string(img))
# cv2.imshow('Result', img)
# cv2.waitKey(0)

def get_numberplate(img_path):
    img = cv2.imread(img_path)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    result = pytesseract.image_to_string(img)
    # remove unnecessary characters and spaces
    result_improved = ''
    for c in result:
        if(c.isalnum()):
            result_improved = result_improved + c
    print('OCR for ', img_path, ' : ', result_improved)
    return result_improved

# get_numberplate('1.png')
# get_numberplate('2.png')
# get_numberplate('3.png')
# get_numberplate('4.png')