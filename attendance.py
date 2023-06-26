from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Attendance(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    studentNumber = db.Column(db.String(100))
    loginDate = db.Column(db.Date, nullable=False)
    loginTime = db.Column(db.Time, nullable=False)
    logoutTime = db.Column(db.Time)

    def __init__(self, studentNumber, loginDate, loginTime):
        self.studentNumber = studentNumber
        self.loginDate = loginDate
        self.loginTime = loginTime
        # self.logoutTime = logoutTime

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    gName = db.Column(db.String(100))
    lName = db.Column(db.String(100))
    mName = db.Column(db.String(100))
    program = db.Column(db.String(100))
    studentNumber = db.Column(db.String(100))
    studentWebmail = db.Column(db.String(100))
    phoneNumber = db.Column(db.String(100))
    address = db.Column(db.String(100))
    password = db.Column(db.String(255))
    section = db.Column(db.String(100))

    def __init__(self, gName, lName, mName, program, studentNumber, studentWebmail, phoneNumber, address, password, section):
        self.gName = gName
        self.lName = lName
        self.mName = mName
        self.program = program
        self.studentNumber = studentNumber
        self.studentWebmail = studentWebmail
        self.phoneNumber = phoneNumber
        self.address = address
        self.password = password
        self.section = section
        
class Faculty(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    gName = db.Column(db.String(100))
    lName = db.Column(db.String(100))
    mName = db.Column(db.String(100))
    webmail = db.Column(db.String(100))
    phoneNumber = db.Column(db.String(100))
    address = db.Column(db.String(100))
    password = db.Column(db.String(255))

    def __init__(self, gName, lName, mName, webmail, phoneNumber, address, password):
        self.gName = gName
        self.lName = lName
        self.mName = mName
        self.webmail = webmail
        self.phoneNumber = phoneNumber
        self.address = address
        self.password = password
        
class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    isbn = db.Column(db.String(100))
    title = db.Column(db.String(100))
    item_call_number = db.Column(db.String(100))
    author = db.Column(db.String(100))
    publisher = db.Column(db.String(100))
    status = db.Column(db.String(100))
    tags = db.Column(db.String(100))
    nfc_code = db.Column(db.  String(100))
    description = db.Column(db.String(100))
    
    def __init__(self, id, isbn, title, item_call_number, author, publisher, status, tags, nfc_code, description):
        self.id = id
        self.isbn = isbn
        self.title = title
        self.item_call_number = item_call_number
        self.author = author
        self.publisher = publisher
        self.status = status
        self.tags = tags
        self.nfc_code = nfc_code
        self.description = description
