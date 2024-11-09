from django.urls import path
from .views import location_list, get_location, create_rating, create_crowd_meter, create_dog_count

urlpatterns = [
    path('locations/', location_list, name='location_list'),
    path('locations/<int:location_id>/', get_location, name='get_location'),
    path('locations/<int:location_id>/rate/', create_rating, name='create_rating'),
    path('locations/<int:location_id>/crowd-meter/', create_crowd_meter, name='create_crowd_meter'),
    path('locations/<int:location_id>/dog-count/', create_dog_count, name='create_dog_count'),
]
