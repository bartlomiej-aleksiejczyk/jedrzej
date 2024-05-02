from django import forms

class ScriptForm(forms.Form):
    script = forms.CharField(widget=forms.Textarea)
