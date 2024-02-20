from django import forms
from .models import Course, Semester

class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['title', 'instructor', 'group', 'instructor_evaluation_grade']
        widgets = {
            'instructor_evaluation_grade': forms.NumberInput(attrs={
                'min': 1,
                'max': 5,
            }),
            'group': forms.NumberInput(attrs={
                'min': 1,
                'max': 10,
            }),
        }


class SemesterForm(forms.ModelForm):
    class Meta:
        model = Semester
        fields = ['code', 'day_start', 'month_start', 'year_start', 'day_end', 'month_end', 'year_end']
        widgets = {
            'day_start': forms.NumberInput(attrs={
                'min': 1,
                'max': 31,
            }),
            'day_end': forms.NumberInput(attrs={
                'min': 1,
                'max': 31,
            }),
            'year_start': forms.NumberInput(attrs={
                'min': 1390,
                'max': 1450,
            }),
            'year_end': forms.NumberInput(attrs={
                'min': 1390,
                'max': 1450,
            }),
        }
