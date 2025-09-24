from celery import shared_task
import pandas as pd
import pdfplumber
import re
from ofxparse import OfxParser
from .models import FinancialDocument, Transaction
import pytesseract
from pdf2image import convert_from_path

@shared_task
def handle_csv_file(document_id):
    document = FinancialDocument.objects.get(id=document_id)
    file_path = document.file.path
    try:
        df = pd.read_csv(file_path)
        for _, row in df.iterrows():
            Transaction.objects.create(
                document=document,
                transaction_id=row.get('Transaction ID'),
                date=row.get('Date'),
                amount=row.get('Amount'),
                description=row.get('Description'),
            )
        document.processing_status = 'processed'
        document.save()
    except Exception as e:
        document.processing_status = f'failed: {e}'
        document.save()

@shared_task
def handle_excel_file(document_id):
    document = FinancialDocument.objects.get(id=document_id)
    file_path = document.file.path
    try:
        df = pd.read_excel(file_path)
        for _, row in df.iterrows():
            Transaction.objects.create(
                document=document,
                transaction_id=row.get('Transaction ID'),
                date=row.get('Date'),
                amount=row.get('Amount'),
                description=row.get('Description'),
            )
        document.processing_status = 'processed'
        document.save()
    except Exception as e:
        document.processing_status = f'failed: {e}'
        document.save()

@shared_task
def handle_clean_pdf(document_id):
    document = FinancialDocument.objects.get(id=document_id)
    file_path = document.file.path
    try:
        with pdfplumber.open(file_path) as pdf:
            text = ''
            for page in pdf.pages:
                text += page.extract_text()
        # This is a simple example, a more robust solution would be needed for a real-world scenario
        for line in text.split('\n'):
            match = re.match(r'(\S+)\s+(\S+)\s+(\S+)\s+(.*)', line)
            if match:
                transaction_id, date, amount, description = match.groups()
                Transaction.objects.create(
                    document=document,
                    transaction_id=transaction_id,
                    date=date,
                    amount=amount,
                    description=description,
                )
        document.processing_status = 'processed'
        document.save()
    except Exception as e:
        document.processing_status = f'failed: {e}'
        document.save()

@shared_task
def handle_scanned_pdf(document_id):
    document = FinancialDocument.objects.get(id=document_id)
    file_path = document.file.path
    try:
        images = convert_from_path(file_path)
        text = ''
        for image in images:
            text += pytesseract.image_to_string(image)

        # This is a simple example, a more robust solution would be needed for a real-world scenario
        for line in text.split('\n'):
            match = re.match(r'(\S+)\s+(\S+)\s+(\S+)\s+(.*)', line)
            if match:
                transaction_id, date, amount, description = match.groups()
                Transaction.objects.create(
                    document=document,
                    transaction_id=transaction_id,
                    date=date,
                    amount=amount,
                    description=description,
                )
        document.processing_status = 'processed'
        document.save()
    except Exception as e:
        document.processing_status = f'failed: {e}'
        document.save()

@shared_task
def handle_ofx_file(document_id):
    document = FinancialDocument.objects.get(id=document_id)
    file_path = document.file.path
    try:
        with open(file_path, 'rb') as f:
            ofx = OfxParser.parse(f)
        for transaction in ofx.account.statement.transactions:
            Transaction.objects.create(
                document=document,
                transaction_id=transaction.id,
                date=transaction.date.date(),
                amount=transaction.amount,
                description=transaction.memo,
            )
        document.processing_status = 'processed'
        document.save()
    except Exception as e:
        document.processing_status = f'failed: {e}'
        document.save()
