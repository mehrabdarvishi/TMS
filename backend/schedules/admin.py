from django.contrib import admin
from .models import Instructor, Semester, Program, Course, CourseSession, ProgramTitle, CourseTitle


# Register your models here.
admin.site.register(Instructor)
admin.site.register(Semester)
admin.site.register(Program)
admin.site.register(Course)
admin.site.register(CourseSession)
admin.site.register(ProgramTitle)
admin.site.register(CourseTitle)