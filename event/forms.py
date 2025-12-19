from django import forms
from .models import Lead
from django.core.exceptions import ValidationError

class LeadForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.keys():
            self.fields[field].widget.attrs['class'] = 'form-control'
    class Meta:
        model = Lead
        fields = "__all__"
        labels = {
            'name': 'Nome',
            'email': 'E-mail'
        }
        
    def clean_name(self):
        name = self.cleaned_data.get('name')
        if len(name) < 3:
            print('entrou no erro do form')
            raise ValidationError("Nome deve conter pelo menos 3 letras")
        return name

