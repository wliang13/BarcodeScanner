from flask import Flask, render_template, request, redirect, Response, send_file
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from pyzbar.pyzbar import decode
import cv2
import winsound 
from Excel_Exporter import exportExcelSheet



app = Flask(__name__) #Flask dependency
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)

barcodeList = [] 
rowList= []
#dexport = []                       #list of decoded barcodes
temp=0
#camera = cv2.VideoCapture(0)
cameraCaptureVar=0

"""
def barcodeDecoder(image):
    barcodes = decode(image)            #decode function from pyzbar that decodes barcodes
    for obj in barcodes:
        (x, y, w, h) = obj.rect         #locating barcode in image
        #creating a rectangle around the barcode
        cv2.rectangle(image, (x-10, y-10), (x+(w+10), y+(h+10)), (255, 0, 0), 2)

        #adding barcode values to the list
        if obj.data not in barcodeList:
            #might no need list, might just need to add to database
            barcodeList.append(obj.data)
            temp = obj.data    
            #print(temp)
            
"""

def gen_frames():  
    if cameraCaptureVar == 0:
        camera = cv2.VideoCapture(0)
    else:
        return 0
    while True:
        success, frame = camera.read()  # read the camera frame
        barcodes = decode(frame)
        for obj in barcodes:
            (x, y, w, h) = obj.rect         #locating barcode in image
            #creating a rectangle around the barcode
            cv2.rectangle(frame, (x-10, y-10), (x+(w+10), y+(h+10)), (255, 0, 0), 2)
            string = "Barcode Scanned"
            cv2.putText(frame, string, (x-20, y-20), cv2.FONT_HERSHEY_DUPLEX, 1.0, (255, 255, 255), 2)
            #the next line is for showing the barcode data that is being scanned on the video feed
            #cv2.putText(frame, obj.data, (x-20, y-20), cv2.FONT_HERSHEY_DUPLEX, 1.0, (255, 255, 255), 2)
            
            data = obj.data.decode("utf-8")
            if data not in barcodeList:
                #might not need list, might just need to add to database
                barcodeList.append(data)

                sFreqSuccess = 1000  # succes sound frequency
                sDurSuccess = 500 # success sound duration
                winsound.Beep(sFreqSuccess,sDurSuccess)   #Play audio Que
                global temp         #for showing barcode in third page
                temp = 1
            #    temp = obj.data  
            #    #yield obj.data  
            #    #print(temp)

        if not success:
            break
        else:
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n') 
    camera.release()
        


class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    #barcode = db.Column(db.string(200))         #barcodes stored in database
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Row %r>' % self.id

@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        row_number = request.form['content']
        rowList.append(row_number)          ###############################
        new_row = Todo(content=row_number)

        try:
            db.session.add(new_row)
            db.session.commit()
            return redirect('/')
        except:
            return
    else:
        rows = Todo.query.order_by(Todo.date_created).all()
        return render_template('index2.html', rows=rows, barcodeList=barcodeList)

@app.route('/delete/<int:id>')
def delete(id):
    delete_row = Todo.query.get_or_404(id)

    try:
        db.session.delete(delete_row)
        db.session.commit()
        return redirect('/')
    except:
        return 

@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    row = Todo.query.get_or_404(id)
    if request.method == 'POST':
        row.content = request.form['content']

        try:
            db.session.commit()
            return redirect('/')
        except:
            return 
    else:
        return render_template('update.html', row=row)

@app.route('/video_page')
def video_page():
    return render_template('videoPage.html')

@app.route('/video_feed')   
def video_feed():
    if cameraCaptureVar==1:
        filename = 'novideo.jpg'
        return  send_file(filename, mimetype='image/jpg')
    else:
        return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')


#Myabe use this function for showing the barcode in index.html
#@app.route('/show_barcode')
#def show_barcode():
#    if temp == 0:
#        return render_template('barcodeDisplay.html', temp=temp)
#    else:
#        return render_template('barcodeDisplay.html', barcodeList=barcodeList, temp=temp)

@app.route('/stop_camera')
def stop_camera():
    global cameraCaptureVar
    cameraCaptureVar=1
    return render_template('videoPage.html')

@app.route('/start_camera')
def start_camera():
    global cameraCaptureVar
    cameraCaptureVar = 0
    return render_template('videoPage.html')

@app.route('/export')
def export():
    #dexport.append(barcodeList)
    #dexport.append(rowList)
    #print(dexport)
    exportExcelSheet(rowList, barcodeList)
    rows = Todo.query.order_by(Todo.date_created).all()
    return render_template('index2.html', rows=rows, barcodeList=barcodeList)



if __name__ == "__main__":
    app.run(debug=True)
