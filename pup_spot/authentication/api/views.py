from django.http import JsonResponse
from django.views.decorators.csrf import ensure_csrf_cookie, csrf_protect
from django.contrib.auth import login, logout
from user_profiles.models import UserProfile
import json

@ensure_csrf_cookie
def get_csrf_token(request):
    return JsonResponse({'detail': 'CSRF cookie set'})

@csrf_protect
def login_view(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        email = data.get('email')
        password = data.get('password')
        
        try:
            user = UserProfile.objects.get(email=email)
            if user.check_password(password):
                login(request, user)
                return JsonResponse({
                    'detail': 'Successfully logged in',
                    'user': {
                        'email': user.email,
                        'fullName': user.username
                    }
                })
            else:
                return JsonResponse({'detail': 'Invalid credentials'}, status=400)
        except UserProfile.DoesNotExist:
            return JsonResponse({'detail': 'Invalid credentials'}, status=400)
    
    return JsonResponse({'detail': 'Method not allowed'}, status=405)

@csrf_protect
def register_view(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        email = data.get('email')
        password = data.get('password')
        full_name = data.get('fullName')
        
        if UserProfile.objects.filter(email=email).exists():
            return JsonResponse({'detail': 'Email already registered'}, status=400)
        
        user = UserProfile.objects.create(
            email=email,
            username=full_name,
            display_name=full_name
        )
        user.set_password(password)
        user.save()
        
        login(request, user)
        return JsonResponse({
            'detail': 'Successfully registered',
            'user': {
                'email': user.email,
                'fullName': user.username
            }
        }, status=201)
    
    return JsonResponse({'detail': 'Method not allowed'}, status=405)

@csrf_protect
def logout_view(request):
    if request.method == 'POST':
        logout(request)
        return JsonResponse({'detail': 'Successfully logged out'})
    
    return JsonResponse({'detail': 'Method not allowed'}, status=405)