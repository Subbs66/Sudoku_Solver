import cv2
import numpy as np
import requests
import json
import base64

import sudoku

img= cv2.imread ("/home/subhash/Pictures/sudoku.png",1)
print(img.shape)


gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

blur = cv2.GaussianBlur(gray.copy(), (9, 9), 0)

thresh1 = cv2.adaptiveThreshold(blur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)

inv = cv2.bitwise_not(thresh1)

# inv=cv2.Canny(img,100,200) #this can be used instead of all the above pre processing steps

# cv2.imshow('after pre processing',inv)


_,contours,hierarchy = cv2.findContours(inv, 1, 2)
contours = sorted(contours, key=cv2.contourArea, reverse=True)
c = contours[0]
area = cv2.contourArea(c)
print(area)

sum_tuple = []
sub_tuple = []
for pt in c:
    sum_tuple.append(pt[0][0]+pt[0][1])
    sub_tuple.append(pt[0][0]-pt[0][1])

max_pos_sum = sum_tuple.index(max(sum_tuple))
min_pos_sum = sum_tuple.index(min(sum_tuple))
max_pos_sub = sub_tuple.index(max(sub_tuple))
min_pos_sub = sub_tuple.index(min(sub_tuple))
bottom_right = c[max_pos_sum][0]
bottom_left = c[min_pos_sub][0]
top_right = c[max_pos_sub][0]
top_left = c[min_pos_sum][0]

print(bottom_left,bottom_right,top_left,top_right)

#cv2.drawContours(img, [c], -1, (255, 0, 0), 2)
# cv2.imshow("img",img)

src = np.array([top_left, top_right, bottom_left, bottom_right], dtype='float32')
pts2 = np.float32([[0,0],[360,0],[0,360],[360,360]])

M = cv2.getPerspectiveTransform(src,pts2)
dst = cv2.warpPerspective(img,M,(360,360))
# cv2.imshow("net",dst)

print(dst.shape)

height = int(360/9)
width = int(360/9)
x = 0
y = 0
images = []
for i in range(0,9):
    x = 0
    for j in range(0,9):
        images.append(cv2.cvtColor(dst[y:y+height,x:x+width], cv2.COLOR_BGR2GRAY))
        x = x + height
    y = y + width

print("number of boxes = {}".format(len(images)))
ret,image_x = cv2.threshold(images[48],127,255,cv2.THRESH_BINARY_INV)

# cv2.imwrite("number1.jpg", image_x)

# cv2.imshow("i",image_x)
# cv2.waitKey(0)
# cv2.destroyAllWindows()7b187446-711a-4c26-9c9f-da1cf9e63b5f

#Detecting digits with base64 api
array=[]
count=0
for ele in images:
    count+=1
    # ele=cv2.bitwise_not(ele, mask = None)
    # elem = cv2.GaussianBlur(ele, (3, 3), 0)
    # ret,elem = cv2.threshold(ele,127,255,cv2.THRESH_BINARY_INV)
    # elem = cv2.copyMakeBorder(elem, 3, 3, 3, 3, cv2.BORDER_CONSTANT)
    _, im_arr = cv2.imencode('.jpg', ele)  # im_arr: image in Numpy one-dim array format.
    im_bytes = im_arr.tobytes()
    im_b64 = base64.b64encode(im_bytes)

        # cv2.imwrite("number1.jpg", elem)
        #
        # with open("/home/subhash/Desktop/spam/spam max/Sudoku/number1.jpg", "rb") as image_file:
        #     im_b64 = base64.b64encode(image_file.read())
    # cv2.imshow("i",ele)
    # cv2.waitKey(0)

    imog="data:image/png;base64," + im_b64

    url = "https://base64.ai/api/scan"

    payload = json.dumps({
         "image": imog,
         "modelTypes": [
        "ocr"
         ]
    })
    headers = {
         'Content-Type': 'application/json',
         'Authorization': 'ApiKey f20180678@hyderabad.bits-pilani.ac.in:7c573065-aefd-4f9d-9345-3f2a30bf3b94'
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    try:
        if int(response.text[len(response.text)-6])>10:
            array.append(int(response.text[len(response.text)-6])%10)
        else:
            if int(response.text[len(response.text)-6])==9 :
                x=input("manual input for ({},{})th block".format(count%9,(count/9)+1))
                array.append(x)
                print(x)

            elif int(response.text[len(response.text)-6])==6 :
                x=input("manual input for ({},{})th block".format(count%9,(count/9)+1))
                array.append(x)
                print(x)
            else:
                array.append(int(response.text[len(response.text)-6]))
                print(response.text[len(response.text)-6])
    except:
        array.append(0)
        print(0)
# print(response.text)
greed=[]
sudoku.solve(sudoku.gridder(array))
