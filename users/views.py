import base64
import json
from uuid import uuid4
from django.urls import reverse
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views import View
from django.core.mail import send_mail
import random
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from users.models import Client, Motorcycle, Settings
from django.core.files.base import ContentFile

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
        
        user_exists_and_completed = User.objects.filter(email=email, steps="completed")
        print("user_exists_and_completed >> ", user_exists_and_completed)
        if user_exists_and_completed:
            return JsonResponse({'message': 'هذا المستخدم مسجل من قبل لدينا'}, status=400)
        
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
            print("verify view >> ", user.bike_count)
            user.save()
            return JsonResponse({'message': 'Email verified'})
        except User.DoesNotExist:
            return JsonResponse({'message': 'رمز خاطئ'}, status=400)



@method_decorator(csrf_exempt, name='dispatch')
class CompleteRegistrationView(View):
    
    @staticmethod 
    def get_base_url(request):
        base_url = f"{request.scheme}://{request.get_host()}"
        return base_url
    
    @staticmethod
    def readjust_motorcylce_info(bike_count):
        motorcycle_info = Motorcycle.objects.first()
        motorcycle_info.available_motorcycles -= int(bike_count)
        motorcycle_info.soldout_motorcycles += int(bike_count)
        motorcycle_info.total_rental_amount += int(bike_count) * motorcycle_info.motorcycle_price
        motorcycle_info.save()
    
    @staticmethod
    def base64_to_file(base64_string):
        format, imgstr = base64_string.split(';base64,')
        ext = format.split('/')[-1]
        return ContentFile(base64.b64decode(imgstr), name=uuid4().hex + "." + ext)

    def post(self, request):
        body_unicode = request.body.decode('utf-8')
        body_data = json.loads(body_unicode)
        email = body_data.get('email')
        user = Client.objects.get(email=email)
        user.full_name = body_data.get('full_name')
        user.phone = body_data.get('phone')
        user.id_number = body_data.get('id_number')
        user.bike_count = body_data.get('count')
        user.receipt = self.base64_to_file(body_data.get('receipt'))
        user.steps = "completed"
        user.save()
        self.readjust_motorcylce_info(user.bike_count)
        response = {
            "url": f"{self.get_base_url(request)}{reverse('dahsboard')}?email={email}&code={user.verification_code}"
            }
        
        return JsonResponse(response)


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
        email = request.GET.get('email')
        code = request.GET.get('code')
        user_exists = User.objects.filter(email=email, verification_code=code).first()
        if user_exists:
            user_exists.verification_code = str(random.randint(100000, 999999))
            user_exists.save()
            motorcycle_info = Motorcycle.objects.first()
            context.update({
                "email": email,
                "full_name": user_exists.full_name,
                "bike_count": user_exists.bike_count,
                "total_reservation": user_exists.bike_count * motorcycle_info.motorcycle_price,
                "available_motorcycles_count": motorcycle_info.available_motorcycles
                })
            return render(request, 'users/dashboard.html', context)
        return redirect('login-to-dashboard')


@method_decorator(csrf_exempt, name='dispatch')
class AddMotorcyclesView(View):
    
    @staticmethod
    def readjust_motorcylce_info(bike_count):
        motorcycle_info = Motorcycle.objects.first()
        motorcycle_info.available_motorcycles -= int(bike_count)
        motorcycle_info.soldout_motorcycles += int(bike_count)
        motorcycle_info.total_rental_amount += int(bike_count) * motorcycle_info.motorcycle_price
        motorcycle_info.save()
        return motorcycle_info
    
    def post(self, request):
        body_unicode = request.body.decode('utf-8')
        body_data = json.loads(body_unicode)
        email = body_data.get("email")
        motorcycles_count = body_data.get("motorcycles_count")        
        user = User.objects.filter(email=email, steps="completed")
        if user.exists():
            user = user.first()
            user.bike_count += int(motorcycles_count)
            user.save()
            motorcycle_info = self.readjust_motorcylce_info(motorcycles_count)
            response = {
                'message': 'Motorcycles added',
                'count': user.bike_count,
                'total': user.bike_count * motorcycle_info.motorcycle_price
            }
            return JsonResponse(response)
        return JsonResponse({'message': 'something went wrong!'}, status=400)
    


@method_decorator(csrf_exempt, name='dispatch')
class RequestToLoginView(View):
    def post(self, request):
        body_unicode = request.body.decode('utf-8')
        body_data = json.loads(body_unicode)
        email = body_data.get("email")
        user = User.objects.filter(email=email).first()
        if user:
            send_mail('رمز التحقق الخاص بك', f'رمز التحقق الخاص بك هو :{user.verification_code}', 'admin@taheed.com', [email])
            return JsonResponse({'message': 'تم ارسال رمز التحقق الي البريد الالكتروني', 'success': True})
        
        return JsonResponse({'message': 'لا يوجد عميل بهذا البريد الالكتروني'}, status=400) 



@method_decorator(csrf_exempt, name='dispatch')
class LoginToDashboardView(View):
    
    @staticmethod
    def get_base_url(request):
        base_url = f"{request.scheme}://{request.get_host()}"
        return base_url
    
    def get(self, request):
        context = {"base_url": self.get_base_url(request)}
        return render(request, 'users/login-to-dashboard.html', context)
    
    def post(self, request):
        body_unicode = request.body.decode('utf-8')
        body_data = json.loads(body_unicode)
        email = body_data.get("email")
        code = body_data.get("otp")
        user_exists = User.objects.filter(email=email, verification_code=code).first()
        if user_exists:
            response = {
            "url": f"{self.get_base_url(request)}{reverse('dahsboard')}?email={email}&code={code}",
            "success": True
            }
            return JsonResponse(response)
        
        return JsonResponse({'message': 'كلمة المرور لمرة واحدة غير صحيحة'})