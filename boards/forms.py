from django import forms

class BoardForm(forms.Form) :
    title = forms.CharField()
    content = forms.CharField()