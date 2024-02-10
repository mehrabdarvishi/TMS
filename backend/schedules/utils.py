from .models import Semester, Program

def get_semester(semester_code):
    semester_qs = Semester.objects.filter(code=semester_code)
    if  semester_qs.exists():
        return semester_qs.first()
    return None

def get_program(program_code, semester_code=None):
    if semester_code:
        semester = get_semester(semester_code)
        if semester:
            program_qs = semester.program_set.filter(code=program_code)
            if program_qs.exists():
                return program_qs.first()
    else:
        program_qs = Program.objects.filter(code=program_code)
        if program_qs.exists():
            return program_qs.first()
    return None