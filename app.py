from flask import Flask, render_template, request, redirect, Response
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from pyzbar.pyzbar import decode
import cv2


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)

camera = cv2.VideoCapture(0)

def barcodeDecoder(image):
    barcodes = decode(image)            #decode function from pyzbar that decodes barcodes
    for obj in barcodes:
        (x, y, w, h) = obj.rect         #locating barcode in image
        #creating a rectangle around the barcode
        cv2.rectangle(image, (x-10, y-10), (x+(w+10), y+(h+10)), (255, 0, 0), 2)

def gen_frames():  
    while True:
        success, frame = camera.read()  # read the camera frame
        barcodeDecoder(frame)           #decode function that decodes the barcode
        if not success:
            break
        else:
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n') 


class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Row %r>' % self.id

@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        row_number = request.form['content']
        new_row = Todo(content=row_number)

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
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == "__main__":
    app.run(debug=True)