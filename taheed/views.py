# views.py
from django.shortcuts import render

def custom_admin_dashboard(request):

    context = {
        'active_users': 100,
        'blocked_users': 20,
    }
    return render(request, 'admin/index.html', context)

