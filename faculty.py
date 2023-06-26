from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

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
        