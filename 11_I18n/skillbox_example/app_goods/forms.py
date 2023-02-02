from django import forms


class UploadPriceFileForm(forms.Form):
    file = forms.FileField()
