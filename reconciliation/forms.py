from django import forms
from payments.models import MatchingRule

class UploadFileForm(forms.Form):
    file1 = forms.FileField()
    file2 = forms.FileField()

class MatchingRuleForm(forms.ModelForm):
    logic = forms.CharField(widget=forms.Textarea, help_text='Enter the rule logic in JSON format.')

    class Meta:
        model = MatchingRule
        fields = ['name', 'logic', 'confidence_weight']
