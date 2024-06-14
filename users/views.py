import json
from django.shortcuts import render
from django.http import JsonResponse
from django.views import View
from django.core.mail import send_mail
import random
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from users.models import Client, Motorcycle, Settings

User = Client


@method_decorator(csrf_exempt, name='dispatch')
class RegisterView(View):
    
    @staticmethod
    def get_base_url(request):
        base_url = f"{request.scheme}://{request.get_host()}"
        return base_url
    
    def get(self, request):
        context = {"base_url": self.get_base_url(request)}
        settings = Settings.objects.all().first()
        context.update({
            "agreement_text": settings.agreement_text,
            "bank_name": settings.bank_name,
            "bank_account_number": settings.bank_account_number,
        })
        return render(request, 'users/index.html', context)

    def post(self, request):
        body_unicode = request.body.decode('utf-8')
        body_data = json.loads(body_unicode)

        email = body_data.get("email")
        code = str(random.randint(100000, 999999))
        user, created = User.objects.get_or_create(email=email, defaults={'verification_code': code})
        if not created:
            user.verification_code = code
        
        user.steps = 'first'
        user.save()            
            
        send_mail('رمز التحقق الخاص بك', f'رمز التحقق الخاص بك هو :{code}', 'admin@taheed.com', [email])
        return JsonResponse({'message': 'Verification code sent'})


@method_decorator(csrf_exempt, name='dispatch')
class VerifyView(View):
    def post(self, request):
        body_unicode = request.body.decode('utf-8')
        body_data = json.loads(body_unicode)
        
        email = body_data.get('email')
        code = body_data.get('code')
        try:
            user = User.objects.get(email=email, verification_code=code)
            user.is_verified = True
            user.steps = 'second'
            user.save()
            return JsonResponse({'message': 'Email verified'})
        except User.DoesNotExist:
            return JsonResponse({'message': 'رمز خاطئ'}, status=400)



@method_decorator(csrf_exempt, name='dispatch')
class CompleteRegistrationView(View):
    def post(self, request):
        body_unicode = request.body.decode('utf-8')
        body_data = json.loads(body_unicode)
        email = body_data.get('email')
        user = Client.objects.get(email=email)
        user.full_name = body_data.get('full_name')
        user.phone = body_data.get('phone')
        user.id_number = body_data.get('id_number')
        user.bike_count = body_data.get('count')
        user.steps = "completed"

        user.save()
        return JsonResponse({'message': 'Registration completed'})


@method_decorator(csrf_exempt, name='dispatch')
class MotorcycleInfoView(View):
    def get(self, request):
        motorcycle = Motorcycle.objects.all().first()
        info = {
            "motorcycle_price": motorcycle.motorcycle_price,
            "available_motorcycles": motorcycle.available_motorcycles
        }
        return JsonResponse(info)
    
    

@method_decorator(csrf_exempt, name='dispatch')
class ClientDashbboardView(View):
    @staticmethod
    def get_base_url(request):
        base_url = f"{request.scheme}://{request.get_host()}"
        return base_url
    
    def get(self, request):
        context = {"base_url": self.get_base_url(request)}
        
        return render(request, 'users/dashboard.html', context)

