import numpy as np
import cv2
import imutils
import pytesseract
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

image = cv2.imread('Images/3.jpg')

image = imutils.resize(image, width=500)

cv2.imshow("Original Image", image)
cv2.waitKey(0)

# Переводим в серый цвет
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Убираем шумы
gray = cv2.bilateralFilter(gray, 11, 17, 17)

# Находим края
edged = cv2.Canny(gray, 170, 200)

# Находим контуры
contours, new  = cv2.findContours(edged.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

img1 = image.copy()
cv2.drawContours(img1, contours, -1, (0,255,0), 3)

# Сортируем контуры с минимальной площадью равной 30
contours = sorted(contours, key = cv2.contourArea, reverse = True)[:30]
NumberPlateCur = None # Изначально контур номера отсутствует

# Рисуем контуры
img2 = image.copy()
cv2.drawContours(img2, contours, -1, (0,255,0), 3)

# Ищем максимальной близкий контур к номеру
count = 0
index =7
for c in contours:
        peri = cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, 0.02 * peri, True)
        if len(approx) == 4:  # Выбираем контур с 4 углами
            NumberPlateCur = approx # Приближенный контур становится текущим

            # Обрезаем фотографию и добавляем в папку
            x, y, w, h = cv2.boundingRect(c) # Нахождение координат номера
            new_img = gray[y:y + h, x:x + w]
            cv2.imwrite('Cropped/' + str(index) + '.png', new_img)
            index+=1

            break


# Рисуем найденный контур на оригинальной фотографии
cv2.drawContours(image, [NumberPlateCur], -1, (0,255,0), 3)
cv2.imshow("Final Image With Number Plate Detected", image)
cv2.waitKey(0)

Cropped= 'Cropped/7.png'
cv2.imshow("Cropped Image ", cv2.imread(Cropped))


text = pytesseract.image_to_string(Cropped, lang='eng')
print("Number is :" + text)

cv2.waitKey(0)