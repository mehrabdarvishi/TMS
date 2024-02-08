from django.forms import ModelForm
from .models import Program

class ProgramForm(ModelForm):
    class Meta:
        model = Program
        fields = ['code', 'title']