from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from .models import Progress
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated;
from rest_framework import status
from datetime import datetime
import cloudinary
import cloudinary.uploader

@api_view(['POST', 'GET'])
@permission_classes([IsAuthenticated])
def progress(request):
    if request.method == 'POST':
        user = request.user
        weight = request.data.get('weight')
        image = request.FILES.get('image')
        height = request.data.get('height')
        date = request.data.get('date')
        
        if not (weight and image and height):
            return Response({"error": "All fields are required"}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            date = datetime.strptime(date, '%Y-%m-%d').date() if date else datetime.now().date()
        except ValueError:
            return Response({"error": "Invalid date format. Use YYYY-MM-DD."}, status=status.HTTP_400_BAD_REQUEST)

        upload_result = cloudinary.uploader.upload(image)

        image_url = upload_result['secure_url']

        progress = Progress.objects.create(
            user=user,
            weight=weight,
            image=image_url, 
            height=height,
            date=date
        )

        return Response({
            "message": "Progress uploaded successfully",
            "image_url": image_url,
            "progress_id": progress.id
        }, status=status.HTTP_201_CREATED)
    
    if request.method == 'GET':
        start_date = request.GET.get('start_date')
        end_date = request.GET.get('end_date')

        try:
            if start_date:
                start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
            if end_date:
                end_date = datetime.strptime(end_date, '%Y-%m-%d').date()
        except ValueError:
            return Response({"error": "Invalid date format. Use YYYY-MM-DD."}, status=status.HTTP_400_BAD_REQUEST)

        if start_date and end_date:
            progress_data = Progress.objects.filter(user=request.user, date__range=[start_date, end_date]).values('id', 'weight', 'height', 'date')
        elif start_date:
            progress_data = Progress.objects.filter(user=request.user, date=start_date).values('id', 'weight', 'image', 'height', 'date')
        else:
            progress_data = Progress.objects.filter(user=request.user).values('id', 'weight', 'height', 'date')

        return Response(list(progress_data), status=status.HTTP_200_OK)
