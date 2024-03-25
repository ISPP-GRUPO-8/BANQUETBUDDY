import re
from django.http import HttpResponseForbidden

from catering_employees.models import Employee

class ProtectCurriculumMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        return response

    def process_view(self, request, view_func, view_args, view_kwargs):
        is_employee = hasattr(request.user, 'EmployeeUsername')
        is_catering_company = hasattr(request.user, 'CateringCompanyusername')
        
        if request.path.startswith('/media/curriculums/'):
            
            if not request.user.is_authenticated:
                return HttpResponseForbidden("No tiene permiso para acceder a esta página")

            file_name = re.search(r'media/(.+)$', request.path).group(1)
            
            if not (is_employee or is_catering_company):
                return HttpResponseForbidden("No tiene permiso para acceder a esta página")

            if is_employee:
                employee_instance = Employee.objects.get(user = request.user)
                if employee_instance.curriculum.name != file_name:
                    return HttpResponseForbidden("No tiene permiso para acceder a esta página")

        return None