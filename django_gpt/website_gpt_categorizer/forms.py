from django import forms

class UploadFileForm(forms.Form):
    csv_file = forms.FileField()

class ReadFileForm(forms.Form):
    file = forms.FileField()