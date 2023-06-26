from flask import Flask, render_template, request, flash, redirect, Response, url_for
from flask_socketio import SocketIO, emit
from database import get_session
# from book import Book
import pandas as pd
# from user import db, User
# from faculty import db, Faculty
import os
import bcrypt
from face_recog import recognize_faces, load_known_faces
import time
from attendance import db, Attendance, User, Faculty, Book
from datetime import datetime, time
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from sqlalchemy import desc, asc, and_, or_

import cv2
# import face_recognition
# from datetime import datetime

app = Flask(__name__)
socketio = SocketIO(app)
app.config['SERVER_NAME'] = 'localhost:5000'
app.config["IMAGE_UPLOADS"] = "D:/Thesis Projects (Try)/attendance/static/uploads/id-pictures"
app.config["FACE_IMAGE_UPLOADS"] = "D:/Thesis Projects (Try)/attendance/static/uploads/face-images"
app.secret_key = 'your_secret_key'

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres@localhost/astelisk_db'
db.init_app(app)
migrate = Migrate(app, db)

known_faces_folder = "static/uploads/face-images/"
known_faces, known_names = load_known_faces(known_faces_folder)


# --------------------------------- ADMIN PAGES
@app.route('/admin-upload-books-file', methods=['GET', 'POST'])
def file_upload():
    session = get_session()

    if request.method == 'POST':
        if 'upload' in request.form:
            file = request.files['file']
            if file:
                # Read the Excel file using pandas
                df = pd.read_excel(file)

                # Save the data to the database
                try:
                    # Get the last book ID from the table
                    last_book = session.query(Book).order_by(Book.id.desc()).first()
                    last_id = last_book.id if last_book else 0

                    # Generate IDs for the new entries
                    df['id'] = range(last_id + 1, last_id + 1 + len(df))

                    # Save the DataFrame to the database
                    df.to_sql('book', con=session.get_bind(), if_exists='append', index=False, method='multi')
                    flash('File uploaded and data saved to the database successfully!', 'success')
                except Exception as e:
                    flash('An error occurred while saving the data to the database.', 'error')
                    print(str(e))

    session.close()
    return render_template('admin-upload_books_file.html')


@app.route('/admin-add-books', methods=['GET', 'POST'])
def index():
    session = get_session()

    if request.method == 'POST':
        if 'button1' in request.form:
            isbn = request.form.get('isbn')
            title = request.form.get('title')
            item_call_number = request.form.get('item_call_number')
            author = request.form.get('author')
            publisher = request.form.get('publisher')
            status = request.form.get('status')
            tags = request.form.get('tags')
            nfc_code = request.form.get('nfc_code')
            description = request.form.get('description')

            # Save the inputs to the database
            try:
                # Get the last book ID from the table
                last_book = session.query(Book).order_by(Book.id.desc()).first()
                last_id = last_book.id if last_book else 0

                # Generate the ID for the new book
                new_id = last_id + 1

                # Save the book to the database
                book = Book(id=new_id, isbn=isbn, title=title, item_call_number=item_call_number,
                            author=author, publisher=publisher, status=status, tags=tags, nfc_code=nfc_code, description=description)
                session.add(book)
                session.commit()
                flash('Book successfully added to the database!', 'success')
            except Exception as e:
                flash('An error occurred while saving the book to the database.', 'error')
                print(str(e))

    session.close()
    return render_template('admin-add_books.html')


# Edit Book route
@app.route('/admin-edit-book/<int:book_id>', methods=['GET', 'POST'])
def edit_book(book_id):
    session = get_session()
    book = session.query(Book).get(book_id)

    if request.method == 'POST':
        # Update the book details based on the form data
        book.isbn = request.form['isbn']
        book.title = request.form['title']
        book.item_call_number = request.form['item_call_number']
        book.author = request.form['author']
        book.publisher = request.form['publisher']
        book.status = request.form['status']
        book.tags = request.form['tags']
        book.nfc_code = request.form['nfc_code']
        book.description = request.form['description']

        session.commit()
        session.close()
        return redirect('/admin-all-books')

    session.close()
    return render_template('admin-edit_book.html', book=book)


@app.route('/admin-all-books')
def all_books():
    session = get_session()
    # Retrieve all books from the table
    book = session.query(Book).all()

    session.close()
    return render_template('admin-all_books.html', book=book)

# Delete Book route
@app.route('/admin-delete-book/<int:book_id>', methods=['GET', 'POST'])
def delete_book(book_id):
    session = get_session()
    book = session.query(Book).get(book_id)

    if request.method == 'POST':
        session.delete(book)
        session.commit()
        session.close()
        return redirect('/admin-all-books')

    session.close()
    return render_template('admin-delete_book.html', book=book)

@app.route('/admin-book-search', methods=['GET'])
def admin_book_search():
    query = request.args.get('query')
    results = Book.query.filter(Book.title.ilike(f'%{query}%')).all()
    return render_template('admin-book_search_results.html', query=query, results=results)

@app.route('/admin-all-users')
def admin_all_users():
    session = get_session()
    # Retrieve all books from the table
    student = session.query(User).order_by(User.lName.asc()).all()
    faculty = session.query(Faculty).order_by(Faculty.lName.asc()).all()
    # user = session.query(User).union(session.query(Faculty)).order_by(User.lName, Faculty.lName)
    user = session.query(User.lName.label('lName'), User.gName.label('gName'), User.studentWebmail.label('webmail')).\
    union(db.session.query(Faculty.lName.label('lName'), Faculty.gName.label('gName'), Faculty.webmail.label('webmail'))).\
    order_by(asc('lName')).all()

    session.close()
    return render_template('admin-all_users.html', student=student, faculty=faculty, user=user)

# --------------------------------- PATRON PAGES
@app.route('/patron-register')
def patron_register():
    return render_template('patron-register.html')

@app.route('/patron-register-info', methods=['GET', 'POST'])
def register_patron():
    session = get_session()
    if request.method == "POST":
            gName = request.form.get('gName')
            lName = request.form.get('lName')
            mName = request.form.get('mName')
            program = request.form.get('program')
            studentNumber = request.form.get('studentNumber')
            studentWebmail = request.form.get('studentWebmail')
            phoneNumber = request.form.get('phoneNumber')
            address = request.form.get('address')
            password = request.form.get('password')
            section = request.form.get('section')

            hashedPassword = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

            user = User(gName=gName, lName=lName, mName=mName, program=program, studentNumber=studentNumber, studentWebmail=studentWebmail, phoneNumber=phoneNumber, address=address, password=hashedPassword, section=section)
            session.add(user)
            session.commit()

            if request.files:
                image = request.files["image"]
                faceImage = request.files["faceImage"]
                print(image)
                print(faceImage)
                image.save(os.path.join(app.config["IMAGE_UPLOADS"], studentNumber + ".jpg"))
                faceImage.save(os.path.join(app.config["FACE_IMAGE_UPLOADS"], studentNumber + ".jpg"))

    return render_template("patron-register.html")

@app.route('/patron-register-faculty')
def patron_register_faculty():
    return render_template('patron-register_faculty.html')

@app.route('/patron-register-faculty-info', methods=['GET', 'POST'])
def patron_register_faculty_info():
    session = get_session()
    if request.method == "POST":
            gName = request.form.get('gName')
            lName = request.form.get('lName')
            mName = request.form.get('mName')
            webmail = request.form.get('webmail')
            phoneNumber = request.form.get('phoneNumber')
            address = request.form.get('address')
            password = request.form.get('password')

            hashedPassword = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

            faculty = Faculty(gName=gName, lName=lName, mName=mName, webmail=webmail, phoneNumber=phoneNumber, address=address, password=hashedPassword)
            session.add(faculty)
            session.commit()

            if request.files:
                image = request.files["image"]
                faceImage = request.files["faceImage"]
                print(image)
                print(faceImage)
                image.save(os.path.join(app.config["IMAGE_UPLOADS"], webmail + ".jpg"))
                faceImage.save(os.path.join(app.config["FACE_IMAGE_UPLOADS"], webmail + ".jpg"))

    return render_template("patron-register_faculty.html")


# --------------------------------- KIOSK PAGES
@app.route('/kiosk-login')
def kiosk_login():
    return render_template('kiosk-login.html')

@app.route('/kiosk-video_feed')
def kiosk_video_feed():
    def generate_frames():
        video_capture = cv2.VideoCapture(0)
        while True:
            ret, frame = video_capture.read()

            frame_with_faces, recognized_name = recognize_faces(frame, known_faces, known_names)
            
            # print("Frame:", frame)
            # print("Known Faces:", known_faces)
            # print("Known Names:", known_names)
            # print("Frame with Faces:", frame_with_faces)
            # print("Recognized Faces:", recognized_name)
            
            # time.sleep(2)

            ret, jpeg = cv2.imencode('.jpg', frame_with_faces)
            frame_bytes = jpeg.tobytes()

            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n\r\n')

            if recognized_name:
                # Send a message to the front-end indicating a recognized face
                print("Sending recognized face message")
                socketio.emit('recognized_face', {'name': recognized_name})

    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/kiosk-confirm-identity/<source>/<name>', methods=['GET', 'POST'])
def kiosk_confirm_identity(name, source):
    session = get_session()
    
    if request.method == 'POST':
        if request.form['action'] == 'yes':
            current_date = datetime.now().date()
            current_time = datetime.now().time().strftime("%H:%M:%S")
            
            attendanceCheck = Attendance.query.filter(
                Attendance.studentNumber == name,
                Attendance.loginDate == current_date).first()
            print(attendanceCheck)
            
            if attendanceCheck:
                if source == "logout":
                    attendance = session.query(Attendance).get(attendanceCheck.id)
                    attendance.logoutTime = current_time
                    session.commit()
                else:
                    return redirect(url_for('patron_register_faculty', name=name))

            else:
                if source == "login":
                    attendance = Attendance(studentNumber=name, loginDate=current_date, loginTime=current_time)
                    session.add(attendance)
                else:
                    return redirect(url_for('patron_register'))
            
            session.commit()
            return redirect(url_for('kiosk_home'))
        
        elif request.form['action'] == 'no':
            return redirect(url_for('kiosk_login'))

    return render_template('kiosk-confirm_identity.html', name=name)
@app.route('/kiosk-logout')
def kiosk_logout():
    return render_template('kiosk-logout.html')

@app.route('/kiosk-home')
def kiosk_home():
    return render_template('kiosk-home.html')

if __name__ == '__main__':
    app.run(debug=True)
