from django.urls import path
from . import views

app_name = 'schedules'

urlpatterns = [
    path('semester/', views.SemesterListView.as_view(), name='semester-list'),
    path('semester/new/', views.SemesterCreateView.as_view(), name='semester-create'),
    path('semester/<slug:semester_code>/', views.SemesterDetailView.as_view(), name='semester-detail'),
    path('semester/<slug:semester_code>/update/', views.SemesterUpdateView.as_view(), name='semester-update'),
    path('semester/<slug:semester_code>/delete/', views.SemesterDeleteView.as_view(), name='semester-delete'),

    path('semester/<slug:semester_code>/program/new', views.program_create, name='program-create'),
    path('semester/<slug:semester_code>/program/<slug:program_code>/', views.program_detail, name='program-detail'),
    path('semester/<slug:semester_code>/program/<slug:program_code>/update/', views.program_update, name='program-update'),
    path('semester/<slug:semester_code>/program/<slug:program_code>/delete/', views.program_delete, name='program-delete'),



    #path('semester/<slug:semester_code>/add-new-program', views.create_program, name='program-create'),
    #path('program/<slug:code>', views.ProgramDetailView.as_view(), name='program-detail'),



    path('semester/new/', views.SemesterCreateView.as_view(), name='create-semester'),
    path('course/new/', views.CourseCreateView.as_view(), name='course-create'),
    path('course-session/new/', views.CourseSessionCreateView.as_view(), name='create-course-session'),
    path('instructor/add/', views.InstructorCreateView.as_view(), name='create-instructor'),
    path('course-title/add/', views.CourseTitleCreateView.as_view(), name='course-title-create'),
    path('program-title/', views.ProgramTitleListView.as_view(), name='program-title-list'),
    path('program-title/<int:pk>/update/', views.ProgramTitleUpdateView.as_view(), name='program-title-update'),
    path('program-title/<int:pk>/delete/', views.ProgramTitleDeleteView.as_view(), name='program-title-delete'),
    path('program-title/new', views.ProgramTitleCreateView.as_view(), name='program-title-create'),
    
]