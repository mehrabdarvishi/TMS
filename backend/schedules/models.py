from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

class Instructor(models.Model):
    first_name = models.CharField(verbose_name='نام', max_length=30)
    last_name = models.CharField(verbose_name='نام خانوادگی', max_length=30)

    def __str__(self) -> str:
        return f'{self.first_name} {self.last_name}'

class ProgramTitle(models.Model):
    title = models.CharField(verbose_name='عنوان', unique=True, max_length=80)

    def __str__(self) -> str:
        return self.title

class CourseTitle(models.Model):
    title = models.CharField(verbose_name='عنوان', unique=True, max_length=80)

    def __str__(self) -> str:
        return self.title

# ترم
class Semester(models.Model):

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
    day_validator = [MinValueValidator(1), MaxValueValidator(31)]
    code = models.SlugField('کد', max_length=20)
    day_start = models.IntegerField(verbose_name='روز شروع', validators=day_validator)
    month_start = models.PositiveSmallIntegerField(verbose_name='ماه شروع', choices=MONTH_CHOICES)
    year_start = models.IntegerField(verbose_name='سال شروع', validators=year_validators)
    day_end = models.IntegerField(verbose_name='روز پایان', validators=day_validator)
    month_end = models.PositiveSmallIntegerField(verbose_name='ماه پایان' ,choices=MONTH_CHOICES)
    year_end = models.IntegerField(verbose_name='سال پایان', validators=year_validators)


    def __str__(self) -> str:
        return self.code
    
    class Meta:
        ordering = ['year_start', 'month_start']

# دوره
class Program(models.Model):
    code = models.SlugField(verbose_name='کد', max_length=20, unique=True)
    title = models.ForeignKey(verbose_name='عنوان', to=ProgramTitle, on_delete=models.SET_NULL, null=True, blank=True)
    semester = models.ForeignKey(verbose_name='ترم', to=Semester, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.code
    
    
# درس
class Course(models.Model):
    title= models.ForeignKey(verbose_name='عنوان', to=CourseTitle, on_delete=models.CASCADE)
    instructor = models.ForeignKey(verbose_name='مدرس', to=Instructor, on_delete=models.SET_NULL, null=True, blank=True)
    program = models.ForeignKey(verbose_name='دوره', to=Program, on_delete=models.CASCADE)
    instructor_evaluation_grade = models.IntegerField(verbose_name='نمره ارزیابی مدرس', validators=[MinValueValidator(1), MaxValueValidator(5)], null=True, blank=True)
    group = models.SmallIntegerField(verbose_name='گروه', validators=[MinValueValidator(1)], null=True, blank=True)


    def __str__(self) -> str:
        return self.title.title

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

    course = models.ForeignKey(verbose_name='درس', to=Course, on_delete=models.CASCADE)
    location = models.CharField(verbose_name='محل برگزاری', max_length=50, null=True, blank=True)
    start_time = models.TimeField(verbose_name='ساعت شروع')
    end_time = models.TimeField(verbose_name='ساعت پایان')
    weekday = models.CharField(verbose_name='روز هفته', max_length=1, choices=WEEKDAY_CHOICES)

    def duration_in_minutes(self):
        start_minutes = self.start_time.hour*60 + self.start_time.minute
        end_minutes = self. end_time.hour*60 + self.end_time.minute
        return end_minutes - start_minutes
    
    def schedule_field_width(self):
        return f'{self.duration_in_minutes()*1.7}px'