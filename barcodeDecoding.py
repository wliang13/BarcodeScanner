import cv2
import numpy as np
from pyzbar.pyzbar import decode
from PIL import Image

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

    #img = cv2.imread(image)             #reads the image in numpy array
    barcodes = decode(image)              #decodes barcode 
    for obj in barcodes:       

        (x, y, w, h) = obj.rect         #locating barcode in image
        cv2.rectangle(image, (x-10, y-10), (x+(w+10), y+(h+10)), (255, 0, 0), 2)

        #if obj.data!="":
        #print(obj.data)
        #print(obj.type)

imageCapture()
#image = "barcode2.jpg"
#barcodeDecoder(image)
