from django.urls import path
from . import views

app_name = 'schedules'

urlpatterns = [
    path('semester/', views.SemesterListView.as_view(), name='semester-list'),
    path('semester/new/', views.SemesterCreateView.as_view(), name='semester-create'),
    path('semester/<slug:semester_code>/', views.SemesterDetailView.as_view(), name='semester-detail'),
    path('semester/<slug:semester_code>/update/', views.SemesterUpdateView.as_view(), name='semester-update'),
    path('semester/<slug:semester_code>/delete/', views.SemesterDeleteView.as_view(), name='semester-delete'),

    path('semester/<slug:semester_code>/program/new/', views.ProgramCreateView.as_view(), name='program-create'),
    path('semester/<slug:semester_code>/program/<slug:program_code>/', views.ProgramDetailView.as_view(), name='program-detail'),
    path('semester/<slug:semester_code>/program/<slug:program_code>/update/', views.ProgramUpdateView.as_view(), name='program-update'),
    path('semester/<slug:semester_code>/program/<slug:program_code>/delete/', views.ProgramDeleteView.as_view(), name='program-delete'),


    path('semester/<slug:semester_code>/program/<slug:program_code>/course/new/', views.CourseCreateView.as_view(), name='course-create'),
    path('semester/<slug:semester_code>/program/<slug:program_code>/course/<int:id>/', views.CourseDetailView.as_view(), name='course-detail'),
    path('semester/<slug:semester_code>/program/<slug:program_code>/course/<int:id>/update/', views.CourseUpdateView.as_view(), name='course-update'),
    path('semester/<slug:semester_code>/program/<slug:program_code>/course/<int:id>/delete/', views.CourseDeleteView.as_view(), name='course-delete'),



    #path('semester/<slug:semester_code>/add-new-program', views.create_program, name='program-create'),
    #path('program/<slug:code>', views.ProgramDetailView.as_view(), name='program-detail'),



    path('course-session/new/', views.CourseSessionCreateView.as_view(), name='create-course-session'),
    path('instructor/new/', views.InstructorCreateView.as_view(), name='instructor-create'),
    path('course-title/new/', views.CourseTitleCreateView.as_view(), name='course-title-create'),
    path('program-title/', views.ProgramTitleListView.as_view(), name='program-title-list'),
    path('program-title/<int:pk>/update/', views.ProgramTitleUpdateView.as_view(), name='program-title-update'),
    path('program-title/<int:pk>/delete/', views.ProgramTitleDeleteView.as_view(), name='program-title-delete'),
    path('program-title/new', views.ProgramTitleCreateView.as_view(), name='program-title-create'),
]