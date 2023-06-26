from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

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
        
