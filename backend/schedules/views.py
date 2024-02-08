from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.list import ListView
from .models import Instructor, Semester, Program, Course, CourseSession, ProgramTitle, CourseTitle
from .forms import ProgramForm



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



def create_program(request, semester_code):
    form = ProgramForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            semester = Semester.objects.filter(code=semester_code)
            if semester.exists():
                semester = semester.first()
                code, title = form.cleaned_data['code'], form.cleaned_data['title']
                program = Program(code=code, title=title, semester=semester)
                program.save()
                return redirect('schedules:semester-detail', semester_code=semester.code)
    else:
        context = {
            'form': form
        }
        return render(request, 'schedules/program_form.html', context=context)

class ProgramCreateView(CreateView):
    model = Program
    fields = ['code', 'title']

#class ProgramDetailView(DetailView):
#    model = Program
#    slug_url_kwarg = 'code'
#    slug_field = 'code'
    
def program_detail(request, semester_code, program_code):
    semester = Semester.objects.filter(code=semester_code)
    if semester.exists():
        semester = semester.first()
        program = Program.objects.filter(code=program_code, semester=semester)
        if program.exists():
            program = program.first()
            context = {
                'program': program
            }
            return render(request, template_name='schedules/program_detail.html', context=context)


def program_update(request, semester_code, program_code):
    semester_qs = Semester.objects.filter(code=semester_code)
    if semester_qs.exists():
        semester = semester_qs.first()
        if request.method == 'POST':
            form = ProgramForm(request.POST)
            if form.is_valid():
                program_qs = Program.objects.filter(code=program_code, semester=semester)
                if program_qs.exists():
                    program = program_qs.first()
                    updated_code, updated_title = form.cleaned_data.get('code'), form.cleaned_data.get('title')
                    program.code = updated_code
                    program.title = updated_title
                    program.save()
                    return redirect('schedules:program-detail', semester_code=semester.code, program_code=updated_code)
        else:
            program_qs = Program.objects.filter(code=program_code, semester=semester)
            if program_qs.exists():
                form = ProgramForm(instance=program_qs.first())
                context = {
                    'form': form
                }
                return render(request, template_name='schedules/program_update_form.html', context=context)
        

#class ProgramUpdateView(UpdateView):
#    model = Program
#    fields = '__all__'
#    slug_url_kwarg = 'semester_code'
#    slug_field = 'code'
#    template_name_suffix = '_update_form'


class CourseCreateView(CreateView):
    model = Course
    fields = ['title', 'instructor', 'program', 'instructor_evaluation_grade']


class CourseSessionCreateView(CreateView):
    model = CourseSession
    template_name_prefix = 'course_session'
    template_name = 'schedules/course_session_form.html'
    fields = ['course', 'location', 'start_time', 'end_time', 'weekday']


class InstructorCreateView(CreateView):
    model = Instructor
    fields = ['first_name', 'last_name']

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
