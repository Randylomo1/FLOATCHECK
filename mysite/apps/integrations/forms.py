from django import forms
from .models import Integration

class IntegrationForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(IntegrationForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Integration
        fields = ['integration_type', 'api_key', 'api_secret']
        widgets = {
            'integration_type': forms.Select(attrs={'class': 'form-control'}),
            'api_key': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter API Key'}),
            'api_secret': forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Enter API Secret'}),
        }
