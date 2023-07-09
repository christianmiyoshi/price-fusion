from django.shortcuts import render

# Create your views here.
from .models import Integration

# Create your views here.
def integration_list(request):
    integrations = Integration.objects.all()
    return render(request, 'integration/list/list.html', {'integrations' : integrations})