from django import forms
from .models import PaymentSource

class CSVUploadForm(forms.Form):
    payment_source = forms.ModelChoiceField(queryset=PaymentSource.objects.all(), label="Select Payment Source")
    csv_file = forms.FileField(label="Upload CSV File")
