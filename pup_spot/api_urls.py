from django.urls import path, include

urlpatterns = [
    path('locations/', include('locations.api.urls')),
    path('users/', include('user_profiles.api.urls')),
    path('authentication/', include('authentication.api.urls')),
]
