import cv2
import PIL
import pytesseract
import clean
import os
pytesseract.pytesseract.tesseract_cmd = 'C:\Program Files\Tesseract-OCR\\tesseract.exe'

def extraction():
    docs = []
    no_of_images = len(os.listdir('Images'))
    for k in range(1, no_of_images):
        if(k < 10):
            imgpth = "Images/img-000"+str(k)+".png"
        else:
            imgpth = "Images/img-00"+str(k)+".png"
        image = cv2.imread(imgpth)
        img = PIL.Image.open(imgpth)

        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        _, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY_INV)
        kernel = cv2.getStructuringElement(cv2.MORPH_CROSS, (3, 3))
        dilated = cv2.dilate(thresh, kernel, iterations=13)
        contours, hierarchy = cv2.findContours(
            dilated, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

        l = []
        for contour in contours:
            [x, y, w, h] = cv2.boundingRect(contour)

            if h > 300 and w > 300:
                continue
            if h < 40 or w < 40:
                continue

            cv2.rectangle(image, (x, y), (x+w, y+h), (0, 255, 0), 2)
            img1 = img.crop((x, y, x+w, y+h))
            l.append(pytesseract.image_to_string(img1))

        doc_text = []
        l.reverse()
        for i in l:
            doc_text.extend(clean.text_preprocessing(i))
        docs.append(doc_text)
    return docs

def extract_heading():
    l = []
    no_of_images = len(os.listdir('Images'))
    for k in range(1, no_of_images):
        if(k < 10):
            imgpth = "Images/img-000"+str(k)+".png"
        else:
            imgpth = "Images/img-00"+str(k)+".png"
        image = cv2.imread(imgpth)
        img = PIL.Image.open(imgpth)
        w, h = img.size
        points = [
            np.array([[0, h*0.4], [0, h*0.25], [w, h*0.25], [w, h*0.4]], dtype=np.int32)]

        [x, y, w, h] = cv2.boundingRect(points[0])
        img1 = img.crop((x, y, x+w, y+h))
        l.append(pytesseract.image_to_string(img1))

    non_empty_docs = [clean.text_preprocessing(i) for i in l]
    non_empty_docs = [x for x in non_empty_docs if x]
    return non_empty_docs