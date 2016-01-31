from django import forms

class NameForm(forms.Form):
    your_text = forms.CharField(label='your_text', max_length=5000)