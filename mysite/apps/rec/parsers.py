import csv
import io
import pandas as pd
import pdfplumber
from ofxparse import OfxParser
from django.core.files.storage import default_storage

def parse_csv(file_path):
    with default_storage.open(file_path, 'rb') as f:
        binary_content = f.read()
    try:
        decoded_content = binary_content.decode('utf-8-sig')
    except UnicodeDecodeError:
        decoded_content = binary_content.decode('latin-1')
    
    content_io = io.StringIO(decoded_content)
    reader = csv.reader(content_io)
    header = next(reader)
    data = list(reader)
    return header, data

def parse_excel(file_path):
    with default_storage.open(file_path, 'rb') as f:
        df = pd.read_excel(f, engine='openpyxl')
    header = df.columns.tolist()
    data = df.values.tolist()
    return header, data

def parse_pdf(file_path):
    header = []
    data = []
    with default_storage.open(file_path, 'rb') as f:
        with pdfplumber.open(f) as pdf:
            for page in pdf.pages:
                table = page.extract_table()
                if table:
                    if not header:
                        header = table[0]
                    data.extend(table[1:])
    return header, data

def parse_ofx(file_path):
    with default_storage.open(file_path, 'rb') as f:
        ofx = OfxParser.parse(f)
    
    account = ofx.accounts[0]
    statement = account.statement
    transactions = statement.transactions

    header = ['Transaction ID', 'Amount', 'Date', 'Payee']
    data = []
    for t in transactions:
        data.append([t.id, t.amount, t.date, t.payee])
    
    return header, data
