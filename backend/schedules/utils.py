from .models import Semester, Program

def get_semester(semester_code):
    semester_qs = Semester.objects.filter(code=semester_code)
    if  semester_qs.exists():
        return semester_qs.first()
    return None

