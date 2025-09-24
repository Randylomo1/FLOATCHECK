from rest_framework import generics
from .models import FinancialDocument
from .serializers import FinancialDocumentSerializer
from .tasks import handle_csv_file, handle_excel_file, handle_clean_pdf, handle_scanned_pdf, handle_ofx_file

class FileUploadView(generics.CreateAPIView):
    queryset = FinancialDocument.objects.all()
    serializer_class = FinancialDocumentSerializer

    def perform_create(self, serializer):
        document = serializer.save()
        file_type = document.file_type

        if file_type == 'csv':
            handle_csv_file.delay(document.id)
        elif file_type == 'xlsx' or file_type == 'xls':
            handle_excel_file.delay(document.id)
        elif file_type == 'pdf_clean':
            handle_clean_pdf.delay(document.id)
        elif file_type == 'pdf_scanned':
            handle_scanned_pdf.delay(document.id)
        elif file_type == 'ofx':
            handle_ofx_file.delay(document.id)
        else:
            document.processing_status = 'unsupported_file_type'
            document.save()

        if document.processing_status != 'unsupported_file_type':
            document.processing_status = 'pending'
            document.save()
