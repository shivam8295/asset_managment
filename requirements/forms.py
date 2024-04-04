from django import forms

class ExcelUploadFprm(forms.Form):
    csv_file=forms.FileField(label="select and excel file")