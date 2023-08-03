from ArabicOcr import arabicocr
import cv2
# from google.colab.patches import cv2_imshow
def ocr(path):
    image_path = path
    out_image = 'out.jpg'
    results = arabicocr.arabic_ocr(image_path, out_image)
    print(results)
    words = []
    hadith=""
    for i in range(len(results)):
        word = results[i][1]
        words.append(word)
        hadith+=word
    with open('file.txt', 'w', encoding='utf-8') as myfile:
        myfile.write(str(words))
        new_hadith = str(word)
    img = cv2.imread('out.jpg', cv2.IMREAD_UNCHANGED)
    # cv2.imshow(img)
    return new_hadith