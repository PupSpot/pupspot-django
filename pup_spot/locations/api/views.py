from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from ..models import Location
from ..schemas.locations import LocationFormSchema, LocationSchema
from pydantic import ValidationError

@api_view(['GET', 'POST'])
def location_list(request):
    if request.method == 'GET':
        locations = Location.objects.all()
        response_data = [LocationSchema.from_orm(location).model_dump() for location in locations]
        return Response(response_data)
    
    elif request.method == 'POST':
        try:
            # Validate input data
            location_data = LocationFormSchema(**request.data)
            
            # Get or create location
            location, created = Location.get_or_create_by_coordinates(
                latitude=location_data.latitude,
                longitude=location_data.longitude,
                city=location_data.city,
                region=location_data.region
            )
            
            # Convert to response schema
            response_data = LocationSchema.from_orm(location)
            
            return Response(
                response_data.model_dump(),
                status=status.HTTP_201_CREATED if created else status.HTTP_200_OK
            )
        except ValidationError as e:
            return Response(
                {"detail": str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )

@api_view(['GET'])
def get_location(request, location_id):
    location = get_object_or_404(Location, id=location_id)
    response_data = LocationSchema.from_orm(location)
    return Response(response_data.model_dump())

@api_view(['POST'])
def create_rating(request, location_id):
    try:
        location = get_object_or_404(Location, id=location_id)
        rating_value = float(request.data.get('rating'))
        
        if not 0 <= rating_value <= 5:
            return Response(
                {"detail": "Rating must be between 0 and 5"},
                status=status.HTTP_400_BAD_REQUEST
            )
            
        rating = request.user.create_location_rating(location, rating_value)
        return Response({"detail": "Rating created successfully"}, status=status.HTTP_201_CREATED)
    except ValueError:
        return Response(
            {"detail": "Invalid rating value"},
            status=status.HTTP_400_BAD_REQUEST
        )

@api_view(['POST'])
def create_crowd_meter(request, location_id):
    try:
        location = get_object_or_404(Location, id=location_id)
        value = float(request.data.get('value'))
        
        if not 1 <= value <= 10:
            return Response(
                {"detail": "Crowd meter value must be between 1 and 10"},
                status=status.HTTP_400_BAD_REQUEST
            )
            
        report = request.user.create_crowd_meter_report(location, value)
        location.update_crowd_meter()
        return Response({"detail": "Crowd meter report created successfully"}, status=status.HTTP_201_CREATED)
    except ValueError:
        return Response(
            {"detail": "Invalid crowd meter value"},
            status=status.HTTP_400_BAD_REQUEST
        )

@api_view(['POST'])
def create_dog_count(request, location_id):
    try:
        location = get_object_or_404(Location, id=location_id)
        count = int(request.data.get('count'))
        
        if count < 0:
            return Response(
                {"detail": "Dog count cannot be negative"},
                status=status.HTTP_400_BAD_REQUEST
            )
            
        report = request.user.create_dog_count_report(location, count)
        location.update_average_dog_count()
        return Response({"detail": "Dog count report created successfully"}, status=status.HTTP_201_CREATED)
    except ValueError:
        return Response(
            {"detail": "Invalid dog count value"},
            status=status.HTTP_400_BAD_REQUEST
        )

