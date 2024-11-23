from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from .models import Progress
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated;
from rest_framework import status

CLOUDINARY_BASE_URL = "https://res.cloudinary.com/djm6yhqvx/image/upload/"

@api_view(['POST', 'GET'])
@permission_classes([IsAuthenticated])
def progress(request, id=None):
    if request.method == 'POST':
        user = request.user 
        weight = request.data.get('weight')
        image = request.FILES.get('image')
        height = request.data.get('height')

        if not (weight and image and height):
            return Response({"error": "All fields are required"}, status=status.HTTP_400_BAD_REQUEST)
        
        progress = Progress.objects.create(
            user=user,
            weight=weight,
            image=image,
            height=height
        )   

        progress.image.name = f"{CLOUDINARY_BASE_URL}{progress.image.name}"
        progress.save()

        return Response({
            "message": "Progress uploaded successfully",
            "image_url": progress.image.name,
            "progress_id": progress.id
        }, status=status.HTTP_201_CREATED)
    
    if request.method == 'GET' and id is not None:
        progress = get_object_or_404(Progress, pk=id)
        return Response({
            "id": id,
            "user": progress.user.username,
            "weight": progress.weight,
            "image_url": progress.image.name,
            "height": progress.height,
            "date": progress.date
        })
    
    if request.method == 'GET' and id is None:
        progress_data = Progress.objects.filter(user=request.user).values('id', 'weight', 'image', 'height', 'date')
        return Response(list(progress_data))