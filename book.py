from sqlalchemy import Column, String, Integer
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Book(Base):
    __tablename__ = 'books'
    id = Column(Integer, primary_key=True)
    isbn = Column(String)
    title = Column(String)
    item_call_number = Column(String)
    author = Column(String)
    publisher = Column(String)
    status = Column(String)
    tags = Column(String)
    nfc_code = Column(String)

    # Add any additional columns as needed

    def __repr__(self):
        return f'<Book(id={self.id}, title={self.title}, author={self.author})>'
