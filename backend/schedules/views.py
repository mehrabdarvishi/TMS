from django.shortcuts import render
from django.http import HttpResponse
from django.db.models.base import Model as Model
from django.urls import reverse, reverse_lazy
from django.views import View
from django.views.generic import TemplateView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.list import ListView
import pandas as pd
from .models import Instructor, Semester, Program, Course, CourseSession, ProgramTitle, CourseTitle
from .forms import CourseForm, SemesterForm
from .utils import overlapping_sessions_wrapped

class SemesterCreateView(CreateView):
    model = Semester
    form_class = SemesterForm
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
    form_class = CourseForm

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
    pk_url_kwarg = 'course_id'

    
class CourseUpdateView(UpdateView):
    model = Course
    form_class = CourseForm
    template_name_suffix = '_update_form'

    def get_object(self) -> Model:
        return Course.objects.get(id=self.kwargs.get('course_id'))

    def get_success_url(self) -> str:
        semester_code, program_code, course_id = self.kwargs.get('semester_code'), self.kwargs.get('program_code'), self.kwargs.get('course_id')
        return reverse_lazy('schedules:course-detail', kwargs={'semester_code':semester_code, 'program_code':program_code, 'course_id':course_id})

class CourseDeleteView(DeleteView):
    model = Course

    def get_object(self) -> Model:
        return Course.objects.get(id=self.kwargs.get('course_id'))

    def get_success_url(self) -> str:
        kwargs = {
            'semester_code': self.kwargs.get('semester_code'),
            'program_code': self.kwargs.get('program_code'),
        }
        return reverse_lazy('schedules:program-detail', kwargs=kwargs)

class CourseSessionCreateView(CreateView):
    model = CourseSession
    fields = ['location', 'start_time', 'end_time', 'weekday']
    template_name = 'schedules/course_session_form.html'
    

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        course_id = self.kwargs.get('course_id')
        form.instance.course = Course.objects.get(id=course_id)
        return form
    
    def get_success_url(self) -> str:
        semester_code, program_code, course_id = self.kwargs.get('semester_code'), self.kwargs.get('program_code'), self.kwargs.get('course_id')
        return reverse_lazy('schedules:course-detail', kwargs={'semester_code': semester_code, 'program_code': program_code, 'course_id':course_id})

class CourseSessionUpdateView(UpdateView):
    model = CourseSession
    fields = ['location', 'start_time', 'end_time', 'weekday']
    template_name = 'schedules/course_session_update_form.html'

    def get_object(self) -> Model:
        # Getting the object using all of the url params (Instead of just using the course id.) for ensuring a completely valid url.
        semester = Semester.objects.get(code=self.kwargs.get('semester_code'))
        program = Program.objects.get(code=self.kwargs.get('program_code'), semester=semester)
        course = Course.objects.get(id=self.kwargs.get('course_id'), program=program)
        return CourseSession.objects.get(id=self.kwargs.get('session_id'), course=course)
    
    def get_success_url(self) -> str:
        kwargs = {
            'semester_code': self.kwargs.get('semester_code'),
            'program_code': self.kwargs.get('program_code'),
            'course_id': self.kwargs.get('course_id')
        }
        return reverse_lazy('schedules:course-detail', kwargs=kwargs)

class CourseSessionDeleteView(DeleteView):
    model = CourseSession
    template_name = 'schedules/course_session_confirm_delete.html'

    def get_object(self) -> Model:
        semester = Semester.objects.get(code=self.kwargs.get('semester_code'))
        program = Program.objects.get(code=self.kwargs.get('program_code'), semester=semester)
        course = Course.objects.get(id=self.kwargs.get('course_id'), program=program)
        session = CourseSession.objects.get(id=self.kwargs.get('session_id'), course=course)
        return session
    
    def get_success_url(self) -> str:
        kwargs = {
            'semester_code': self.kwargs.get('semester_code'),
            'program_code': self.kwargs.get('program_code'),
            'course_id': self.kwargs.get('course_id'),
        }
        return reverse_lazy('schedules:course-detail', kwargs=kwargs)

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


class ProgramSchedule(View):
    def get(self, request, *args, **kwargs):
        semester = Semester.objects.get(code=kwargs.get('semester_code'))
        program = Program.objects.get(code=kwargs.get('program_code'), semester=semester)
        courses = program.course_set.all()
        program_sessions = CourseSession.objects.filter(course__in=courses).order_by('start_time')
        context = {
            'saturday_sessions': overlapping_sessions_wrapped(program_sessions.filter(weekday='ش').all()),
            'sunday_sessions': overlapping_sessions_wrapped(program_sessions.filter(weekday='ی').all()),
            'monday_sessions': overlapping_sessions_wrapped(program_sessions.filter(weekday='د').all()),
            'tuesday_sessions': overlapping_sessions_wrapped(program_sessions.filter(weekday='س').all()),
            'wednesday_sessions': overlapping_sessions_wrapped(program_sessions.filter(weekday='چ').all()),
            'thursday_sessions': overlapping_sessions_wrapped(program_sessions.filter(weekday='پ').all()),
            'friday_sessions': overlapping_sessions_wrapped(program_sessions.filter(weekday='ج').all()),
        }
        return render(request, 'schedules/program_schedule.html', context=context)
    

class ExportDataTemplateView(TemplateView):
    template_name = 'schedules/export_data.html'

def export_data_to_excel(request):
    course_sessions = CourseSession.objects.values('course__program__semester__code', 'course__program__code', 'course__title__title', 'course__group', 'weekday', 'start_time', 'end_time', 'location', 'course__instructor__first_name', 'course__instructor__last_name', 'course__instructor_evaluation_grade')

    df = pd.DataFrame.from_records(course_sessions)
    df.rename(columns={
        'course__program__semester__code': 'کد ترم',
        'course__program__code': 'کد دوره',
        'course__title__title': 'نام درس',
        'course__group': 'شماره گروه',
        'weekday': 'روز',
        'start_time': 'ساعت شروع',
        'end_time': 'ساعت پایان',
        'location': 'محل برگزاری',
        'course__instructor__first_name': 'نام استاد',
        'course__instructor__last_name': 'نام خانوادگی استاد',
        'course__instructor_evaluation_grade': 'نمره ارزیابی استاد'
    }, inplace=True)

    response = HttpResponse(content_type='application/xlsx')
    response['Content-Disposition'] = f'attachment; filename="schedule_data.xlsx"'
    with pd.ExcelWriter(response) as writer:
        df.to_excel(writer, index=False)

    return response