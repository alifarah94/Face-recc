from flask import Flask, render_template, request, url_for
#from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename
import face_recognition
import os

app = Flask(__name__)
#PEOPLE_FOLDER = os.path.join('static', 'people_photo')
#app.config['UPLOAD_FOLDER'] = PEOPLE_FOLDER
APP_ROOT = os.path.dirname(os.path.abspath(__file__))

@app.route('/upload')
def upload():
    return render_template('upload.html')

@app.route('/uploader', methods = ['GET', 'POST'])
def upload_file():
    location = os.path.join(APP_ROOT, 'static/')
    print(location)
    if request.method == 'POST':
        f = request.files['file']
        f1 = request.files['file1']
        #file_name=f.filename
        #file_name1 = f1.filename
        f.save(secure_filename(f.filename))
        f1.save(secure_filename(f1.filename))
        #destination = "/".join([location, file_name])
        #destination = "/".join([location, file_name1])
        #f.save(destination)
        #f1.save(destination)
        #image_names = os.listdir('./static')
        #print(destination)
        image_of_known_person = face_recognition.load_image_file(f.filename) # User uploads person to be reconised
        image_of_unknown_person = face_recognition.load_image_file(f1.filename)  # User uploads person to be reconised
        known_face_encodings = face_recognition.face_encodings(image_of_known_person)[0] # Gets the first persons face encodings
        known = [known_face_encodings]
        unknown_face_encodings = face_recognition.face_encodings(image_of_unknown_person)[0] # Gets the first persons face encodings
        for hi in unknown_face_encodings:
            results = face_recognition.compare_faces(known, unknown_face_encodings)
            name = "Unknown"
            if results[0] == True:
                name = "Same person"
            else:
                name = "Not same person"


    return name #render_template("complete.html", image_name=image_names) #render_template("complete.html", user_image = f1.filename)




if __name__ == '__main__':
    app.run(debug=True)

