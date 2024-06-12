import json
from django.shortcuts import render
from django.http import JsonResponse
from django.views import View
from django.core.mail import send_mail
import random
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from users.models import Client

User = Client


@method_decorator(csrf_exempt, name='dispatch')
class RegisterView(View):
    def get(self, request):
        return render(request, 'users/index.html')

    def post(self, request):
        body_unicode = request.body.decode('utf-8')
        body_data = json.loads(body_unicode)

        email = body_data.get("email")
        code = str(random.randint(100000, 999999))
        user, created = User.objects.get_or_create(email=email, defaults={'verification_code': code})
        if not created:
            user.verification_code = code
            user.save()
        send_mail('Your verification code', f'Your code is {code}', 'from@example.com', [email])
        return JsonResponse({'message': 'Verification code sent'})

class VerifyView(View):
    def post(self, request):
        email = request.body.get('email')
        code = request.body.get('code')
        try:
            user = User.objects.get(email=email, verification_code=code)
            user.is_verified = True
            user.save()
            return JsonResponse({'message': 'Email verified'})
        except User.DoesNotExist:
            return JsonResponse({'message': 'Invalid code'}, status=400)

class CompleteRegistrationView(View):
    def post(self, request):
        email = request.body.get('email')
        user = User.objects.get(email=email)
        user.full_name = request.body.get('full_name')
        user.phone = request.body.get('phone')
        user.id_number = request.body.get('id_number')
        user.bike_count = request.body.get('bike_count')
        if 'receipt' in request.FILES:
            user.receipt = request.FILES['receipt']
        user.save()
        return JsonResponse({'message': 'Registration completed'})




# views.py
from django.shortcuts import render

def custom_admin_dashboard(request):

    context = {
        'active_users': 100,
        'blocked_users': 200,
    }
    return render(request, 'admin/custom_dashboard.html', context)
