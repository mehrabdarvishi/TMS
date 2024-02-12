from typing import Any
from django.db.models.base import Model as Model
from django.db.models.query import QuerySet
from django.urls import reverse, reverse_lazy
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.list import ListView
from .models import Instructor, Semester, Program, Course, CourseSession, ProgramTitle, CourseTitle


class SemesterCreateView(CreateView):
    model = Semester
    fields = ['code', 'month_start', 'year_start', 'month_end', 'year_end']
    success_url = reverse_lazy('schedules:semester-list')

class SemesterListView(ListView):
    model = Semester

class SemesterDetailView(DetailView):
    model = Semester
    slug_url_kwarg = 'semester_code'
    slug_field = 'code'

class SemesterUpdateView(UpdateView):
    model = Semester
    fields = '__all__'
    template_name_suffix = '_update_form'
    slug_url_kwarg = 'semester_code'
    slug_field = 'code'

    def get_success_url(self) -> str:
        return reverse('schedules:semester-detail', kwargs={'semester_code':self.object.code})

class SemesterDeleteView(DeleteView):
    model = Semester
    slug_url_kwarg = 'semester_code'
    slug_field = 'code'
    success_url = reverse_lazy('schedules:semester-list')

class ProgramCreateView(CreateView):
    model = Program
    fields = ['code', 'title']
    
    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        semester_code = self.kwargs.get('semester_code')
        form.instance.semester = Semester.objects.get(code=semester_code)
        return form
    
    def get_success_url(self) -> str:
        semester_code = self.kwargs.get('semester_code')
        return reverse_lazy('schedules:semester-detail', kwargs={'semester_code': semester_code})

class ProgramDetailView(DetailView):
    model = Program

    def get_object(self) -> Model:
        program_code, semester_code = self.kwargs.get('program_code'), self.kwargs.get('semester_code')
        semester = Semester.objects.get(code=semester_code)
        return Program.objects.get(code=program_code, semester=semester)
        

class ProgramUpdateView(UpdateView):
    model = Program
    fields = ['code', 'title']
    template_name_suffix = '_update_form'

    def get_object(self) -> Model:
        program_code, semester_code = self.kwargs.get('program_code'), self.kwargs.get('semester_code')
        semester = Semester.objects.get(code=semester_code)
        return Program.objects.get(code=program_code, semester=semester)

    def get_success_url(self) -> str:
        semester_code = self.kwargs.get('semester_code')
        program_code = self.object.code
        return reverse_lazy('schedules:program-detail', kwargs={'semester_code':semester_code, 'program_code':program_code})

class ProgramDeleteView(DeleteView):
    model = Program

    def get_object(self) -> Model:
        semester_code, program_code = self.kwargs.get('semester_code'), self.kwargs.get('program_code')
        semester = Semester.objects.get(code=semester_code)
        return Program.objects.get(code=program_code, semester=semester)

    def get_success_url(self) -> str:
        semester_code = self.kwargs.get('semester_code')
        return reverse_lazy('schedules:semester-detail', kwargs={'semester_code':semester_code})
    
class CourseCreateView(CreateView):
    model = Course
    fields = ['title', 'instructor', 'instructor_evaluation_grade']

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        program_code = self.kwargs.get('program_code')
        form.instance.program = Program.objects.get(code=program_code)
        return form
    
    def get_success_url(self) -> str:
        semester_code = self.kwargs.get('semester_code')
        program_code = self.kwargs.get('program_code')
        return reverse_lazy('schedules:program-detail', kwargs={'semester_code': semester_code, 'program_code': program_code})


class CourseDetailView(DetailView):
    model = Course
    pk_url_kwarg = 'id'

    
class CourseUpdateView(UpdateView):
    model = Course
    fields = ['title', 'instructor', 'instructor_evaluation_grade']
    template_name_suffix = '_update_form'

    def get_object(self) -> Model:
        return Course.objects.get(id=self.kwargs.get('id'))

    def get_success_url(self) -> str:
        semester_code, program_code, course_id = self.kwargs.get('semester_code'), self.kwargs.get('program_code'), self.kwargs.get('id')
        return reverse_lazy('schedules:course-detail', kwargs={'semester_code':semester_code, 'program_code':program_code, 'id':course_id})

class CourseDeleteView(DeleteView):
    model = Course

    def get_object(self) -> Model:
        return Course.objects.get(id=self.kwargs.get('id'))

    def get_success_url(self) -> str:
        kwargs = {
            'semester_code': self.kwargs.get('semester_code'),
            'program_code': self.kwargs.get('program_code'),
        }
        return reverse_lazy('schedules:program-detail', kwargs=kwargs)

class CourseSessionCreateView(CreateView):
    model = CourseSession
    template_name_prefix = 'course_session'
    template_name = 'schedules/course_session_form.html'
    fields = ['course', 'location', 'start_time', 'end_time', 'weekday']


class InstructorCreateView(CreateView):
    model = Instructor
    fields = ['first_name', 'last_name']
    success_url = reverse_lazy('schedules:instructor-create')

class ProgramTitleCreateView(CreateView):
    model = ProgramTitle
    template_name='schedules/program_title_form.html'
    fields = ['title']
    success_url = reverse_lazy('schedules:program-title-list')

class ProgramTitleListView(ListView):
    model = ProgramTitle
    template_name = 'schedules/program_title_list.html'

class ProgramTitleUpdateView(UpdateView):
    model = ProgramTitle
    fields = '__all__'
    template_name = 'schedules/program_title_form.html'
    success_url = reverse_lazy('schedules:program-title-list')

class ProgramTitleDeleteView(DeleteView):
    model = ProgramTitle
    success_url = reverse_lazy('schedules:program-title-list')
    template_name = 'schedules/program_title_confirm_delete.html'


class CourseTitleCreateView(CreateView):
    model = CourseTitle
    template_name = 'schedules/course_title_form.html'
    fields = ['title']
    success_url = reverse_lazy('schedules:course-title-create')
