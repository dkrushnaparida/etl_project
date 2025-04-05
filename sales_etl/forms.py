from django import forms
from .models import SalesUpload

# Django form for file upload
class SalesUploadForm(forms.ModelForm):
    class Meta:
        model = SalesUpload
        fields = ['region_a_file', 'region_b_file']
