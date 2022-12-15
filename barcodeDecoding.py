#NOT BEING USED ANYMORE

import cv2 as cv
import numpy as np
from pyzbar.pyzbar import decode
from PIL import Image
'''

def imageCapture():                     #captures the frames from the video streaming
    vid = cv2.VideoCapture(0)           #set as 0 for integrated webcam 1 for USB webcam
    while True:
        ret, frame = vid.read()
        barcodeDecoder(frame)
        ret2, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()
        yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
        #cv2.imshow('Image', frame)
        #code = cv2.waitKey(10)
        #if code == ord('q'):
        #    break

def barcodeDecoder(image):

    #img = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    img = cv2.imread(image)             #reads the image in numpy array
    barcodes = decode(img)              #decodes barcode 
    for barcode in barcodes:
        data = barcode.data.decode("utf-8")
        print(data)
    
    #for obj in barcodes:       

    
    #    (x, y, w, h) = obj.rect         #locating barcode in image
    #   cv2.rectangle(image, (x-10, y-10), (x+(w+10), y+(h+10)), (255, 0, 0), 2)

        #if obj.data!="":
        #print(obj.data)
        #print(obj.type)

'''
def barcodeDecoderTest(img):

    #img = cv.imread('barcode_example.jpg', cv.IMREAD_GRAYSCALE)
    closed = cv.morphologyEx(img, cv.MORPH_CLOSE, cv.getStructuringElement(cv.MORPH_RECT, (1, 21)))
    dens = np.sum(img, axis=0)
    mean = np.mean(dens)

    thresh = closed.copy()
    for idx, val in enumerate(dens):
        if val< 10800:
            thresh[:,idx] = 0

    (_, thresh2) = cv.threshold(thresh, 128, 255, cv.THRESH_BINARY + cv.THRESH_OTSU)
    barcodes = decode(thresh2)
    print(barcodes)



#image = "barcode3.jpg"
img = cv.imread("barcode.jpg", cv.IMREAD_GRAYSCALE)
barcodeDecoderTest(img)



'''
import numpy as np
import cv2 as cv
from pyzbar import pyzbar

#camera = cv.VideoCapture(0)
while True:
    #success, frame = camera.read() 
    # read the camera frame
    #frame = "barcode3.jpeg"
    #temp = frame
    #cv.imshow("frame", temp)
    #img = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    #cv.imshow("frame", img)

    closed = cv.morphologyEx(img, cv.MORPH_CLOSE, cv.getStructuringElement(cv.MORPH_RECT, (1, 21)))

    dens = np.sum(img, axis=0)

    thresh = closed.copy()
    for idx, val in enumerate(dens):
        if val< 10800:
            thresh[:,idx] = 0

    (_, thresh2) = cv.threshold(thresh, 128, 255, cv.THRESH_BINARY + cv.THRESH_OTSU)

    barcodes = pyzbar.decode(thresh2)
    #print(barcodes)
    for barcode in barcodes:
        data = barcode.data.decode("utf-8")
        print(data)

    cv.waitKey(10)
    '''
