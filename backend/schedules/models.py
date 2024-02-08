from collections.abc import Iterable
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

class Instructor(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)

    def __str__(self) -> str:
        return f'{self.first_name} {self.last_name}'

class ProgramTitle(models.Model):
    title = models.CharField(verbose_name='عنوان', max_length=80)

    def __str__(self) -> str:
        return self.title

class CourseTitle(models.Model):
    title = models.CharField(verbose_name='عنوان', max_length=80)

# ترم
class Semester(models.Model):

    month_validators = [MinValueValidator(1), MaxValueValidator(12)]

    MONTH_CHOICES = {
        1:'فروردین',
        2:'اردیبهشت',
        3:'خرداد',
        4:'تیر',
        5:'مرداد',
        6:'شهریور',
        7:'مهر',
        8:'آبان',
        9:'آذر',
        10:'دی', 
        11:'بهمن', 
        12:'اسفند',
    }
    year_validators = [MinValueValidator(1390), MaxValueValidator(1450)]
    code = models.SlugField('کد', max_length=20)
    month_start = models.PositiveSmallIntegerField(verbose_name='ماه شروع', choices=MONTH_CHOICES)
    year_start = models.IntegerField(verbose_name='سال شروع', validators=year_validators)
    month_end = models.PositiveSmallIntegerField(verbose_name='ماه پایان' ,choices=MONTH_CHOICES)
    year_end = models.IntegerField(verbose_name='سال پایان', validators=year_validators)

    def __str__(self) -> str:
        return self.code

# دوره
class Program(models.Model):
    code = models.SlugField(verbose_name='کد', max_length=20, unique=True)
    title = models.ForeignKey(verbose_name='عنوان', to=ProgramTitle, on_delete=models.SET_NULL, null=True, blank=True)
    semester = models.ForeignKey(verbose_name='ترم', to=Semester, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self) -> str:
        return self.code
    
    
# درس
class Course(models.Model):
    title= models.ForeignKey(to=CourseTitle, on_delete=models.SET_NULL, null=True, blank=True)
    instructor = models.ForeignKey(to=Instructor, on_delete=models.SET_NULL, null=True, blank=True)
    program = models.ForeignKey(to=Program, on_delete=models.SET_NULL, null=True, blank=True)
    instructor_evaluation_grade = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])

class CourseSession(models.Model):
    WEEKDAY_CHOICES = [
        ('ش', 'شنبه'),
        ('ی', 'یک‌شنبه'),
        ('د', 'دوشنبه'),
        ('س', 'سه‌شنبه'),
        ('چ', 'چهارشنبه'),
        ('پ', 'پنج‌شنبه'),
        ('ج', 'جمعه'),
    ]

    course = models.ForeignKey(to=Course, on_delete=models.CASCADE)
    location = models.CharField(verbose_name='محل برگزاری', max_length=50, null=True, blank=True)
    start_time = models.TimeField(verbose_name='ساعت شروع')
    end_time = models.TimeField(verbose_name='ساعت پایان')
    weekday = models.CharField(verbose_name='روز هفته', max_length=1, choices=WEEKDAY_CHOICES)