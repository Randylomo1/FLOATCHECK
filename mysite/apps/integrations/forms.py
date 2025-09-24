from django import forms
from .models import Integration

class IntegrationForm(forms.ModelForm):
    class Meta:
        model = Integration
        fields = ['integration_type', 'api_key', 'api_secret']
        widgets = {
            'integration_type': forms.Select(attrs={'class': 'form-control'}),
            'api_key': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter API Key'}),
            'api_secret': forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Enter API Secret'}),
        }
