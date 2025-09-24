from rest_framework import serializers
from .models import FinancialDocument

class FinancialDocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = FinancialDocument
        fields = ['id', 'file', 'uploaded_at', 'file_type', 'processing_status']
