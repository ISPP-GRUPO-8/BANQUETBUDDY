from catering_owners.models import NotificationEvent, NotificationJobApplication

def global_variable(request):
    if request.user.is_authenticated:
        return {'notification_number': NotificationEvent.objects.filter(user=request.user).count() + NotificationJobApplication.objects.filter(user=request.user).count()}
    else:
        return {}