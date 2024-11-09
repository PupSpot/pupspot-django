from django.shortcuts import render

# Create your views here.
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import UserProfile
import json

from django.contrib.auth.hashers import make_password

@csrf_exempt
def register_user(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            fullname = data.get('fullname')
            email = data.get('email')
            password = data.get('password')
            location = data.get('location', '')

            # Check if email is already registered
            if UserProfile.objects.filter(email=email).exists():
                return JsonResponse({'error': 'Email is already registered'}, status=400)


            # Hash the password
            hashed_password = make_password(password)

            # Create the UserProfile instance
            user_profile = UserProfile.objects.create(
                username=fullname,
                email=email,
                password=hashed_password,  # Store the hashed password
                location=location,
                bio=data.get('bio', '')
            )

            return JsonResponse({'message': 'User registered successfully'}, status=201)
        
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    
    return JsonResponse({'error': 'Invalid request method'}, status=405)

@csrf_exempt
def login_user(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            email = data.get('email')
            password = data.get('password')

            # Retrieve the user by email
            try:
                user = UserProfile.objects.get(email=email)
            except UserProfile.DoesNotExist:
                return JsonResponse({'error': 'Invalid email or password'}, status=400)

            # Check if the provided password matches
            if user.check_password(password):  # check_password handles hashed passwords
                # Successful login
                return JsonResponse({'message': 'Login successful'}, status=200)
            else:
                return JsonResponse({'error': 'Invalid email or password'}, status=400)
        
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    
    return JsonResponse({'error': 'Invalid request method'}, status=405)


@csrf_exempt  
def get_user_details(request):
    if request.method == 'GET':
        # Get username from the query parameter
        username = request.GET.get('username')  # Or use request.data.get('username') if it's a POST request

        if not username:
            return JsonResponse({'error': 'Username is required'}, status=400)

        try:
            # Get the user by username
            user = UserProfile.objects.get(username=username)
            
            # Collect user details
            user_data = {
                'username': user.username,
                'email': user.email,
                'bio':user.bio,
                'location': user.location
            }

            return JsonResponse({'user': user_data}, status=200)

        except UserProfile.DoesNotExist:
            return JsonResponse({'error': 'User not found'}, status=404)

    return JsonResponse({'error': 'Invalid request method'}, status=405)

