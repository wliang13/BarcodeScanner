import os         
from flask import Flask, render_template, request, redirect, Response, send_file
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from pyzbar.pyzbar import decode
import cv2
import winsound 
from Excel_Exporter import exportExcelSheet

basedir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] =\
    'sqlite:///' + os.path.join(basedir, 'database.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    factory = db.Column(db.String(10), nullable=False)
    building = db.Column(db.String(10), nullable=False)
    row = db.Column(db.String(10), nullable=False)
    barcode = db.Column(db.String(50), nullable=False)    
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Row %r>' % self.id

cameraCaptureVar=0

def gen_frames():  
    if cameraCaptureVar == 0:
        camera = cv2.VideoCapture(0)
    else:
        return 0
    while True:
        # read the camera frame
        success, frame = camera.read() 
        barcodes = decode(frame)
        for obj in barcodes:
            #locating barcode in image
            (x, y, w, h) = obj.rect         
            #creating a rectangle around the barcode
            cv2.rectangle(frame, (x-10, y-10), (x+(w+10), y+(h+10)), (255, 0, 0), 2)
            string = "Barcode Scanned"
            cv2.putText(frame, string, (x-20, y-20), cv2.FONT_HERSHEY_DUPLEX, 1.0, (255, 255, 255), 2)
            #the next line is for showing the barcode data that is being scanned on the video feed
            #cv2.putText(frame, obj.data, (x-20, y-20), cv2.FONT_HERSHEY_DUPLEX, 1.0, (255, 255, 255), 2)
            
            data = obj.data.decode("utf-8")
            with app.app_context():
                check = Todo.query.filter_by(barcode=data).first()
                if check==None:
                    update = Todo.query.filter_by(barcode='Not Scanned Yet').first()
                    if update==None:
                        latest_entry = Todo.query.order_by(Todo.id.desc()).first()
                        if latest_entry==None:
                            new_entry = Todo(factory=0, building=0, row=0, barcode=data)
                        else:
                            new_entry = Todo(factory=latest_entry.factory, building=latest_entry.building, row=latest_entry.row, barcode=data)
                        db.session.add(new_entry)
                        db.session.commit()
                    else:
                        update.barcode = data
                        db.session.commit()
                    sFreqSuccess = 1000  # succes sound frequency
                    sDurSuccess = 500 # success sound duration
                    winsound.Beep(sFreqSuccess,sDurSuccess)   #Play audio Que

        if not success:
            break
        else:
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n') 
    camera.release()
        

@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        factory_number = request.form['factory']
        building_number = request.form['building']
        row_number = request.form['row']
        new_row = Todo(factory=factory_number, building=building_number, barcode='Not Scanned Yet', row=row_number)

        try:
            db.session.add(new_row)
            db.session.commit()
            return redirect('/')
        except:
            return
    else:
        rows = Todo.query.order_by(Todo.date_created).all()
        return render_template('index.html', rows=rows)

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
    row_selected = Todo.query.get_or_404(id)
    if request.method == 'POST':
        row_selected.factory = request.form['factory']
        row_selected.building = request.form['building']
        row_selected.row = request.form['row']

        try:
            db.session.commit()
            return redirect('/')
        except:
            return 
    else:
        return render_template('update.html', row_selected=row_selected)

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
    rows = Todo.query.order_by(Todo.date_created).all()
    exportExcelSheet(rows)
    return render_template('index.html', rows=rows)


if __name__ == "__main__":
    app.run(debug=True)


