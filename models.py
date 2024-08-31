from peewee import *
from os import getenv
from dotenv import load_dotenv

load_dotenv()

DB_NAME = getenv('DB_NAME')
API_KEY = getenv('API_KEY')

db = SqliteDatabase(f'{DB_NAME}')

class BaseModel(Model):
    class Meta:
        database = db

class Author(BaseModel):
    name = CharField(unique=True)
    cpf = CharField()
    password = CharField()

class Reader(BaseModel):
    name = CharField(unique=True)
    cpf = CharField()
    password = CharField()

class Book(BaseModel):
    name_book = CharField(unique=True)
    category_book = CharField()
    descr_book = TextField()
    author = ForeignKeyField(Author, backref='books')

class Loan(BaseModel):
    book = ForeignKeyField(Book, backref='loans')
    reader = ForeignKeyField(Reader, backref='loans')
    loan_date = DateField(formats=['%Y-%m-%d'])
    return_date = DateField(formats=['%Y-%m-%d'])
    status = CharField(default='disponível')

db.connect()
db.create_tables([Author, Reader, Book, Loan])
