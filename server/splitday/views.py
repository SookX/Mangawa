from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from .models import SplitDay, Exercise, KgAndReps
from rest_framework.permissions import IsAuthenticated;
from datetime import date
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404

@api_view(['POST', 'GET'])
@permission_classes([IsAuthenticated])
def splitDay(request):

    if request.method == 'POST':
        name = request.data.get('name')
        exercises = request.data.get('exercises', None)

        splitDay = SplitDay.objects.create(
            user = request.user,
            name = name
        )

        if exercises and isinstance(exercises, list):
            for exercise_name in exercises:
                Exercise.objects.create(
                    splitDay=splitDay,
                    name=exercise_name,
                    date=date.today()
                )

        else:
            model_autput = ['name1', 'name2', 'name3']
            for name_in_mode in model_autput:
                Exercise.objects.create(
                    splitDay=splitDay,
                    name=name_in_mode,
                    date=date.today()
                )

        return Response({"message": "SplitDay and Exercises created successfully!"}, status=status.HTTP_201_CREATED)
    
    if request.method == 'GET':
        splitDays = SplitDay.objects.filter(user = request.user).values('id', 'user', 'name')
        return Response(list(splitDays), status=status.HTTP_200_OK)
    
@api_view(['POST', 'GET'])
@permission_classes([IsAuthenticated])
def exercise(request, id):
    
    splitday = get_object_or_404(SplitDay, pk = id)
    
    if request.method == 'POST':
        exercises = request.data.get('exercises', None)
        
        if exercises is None:
            return Response("No exercises provided", status=status.HTTP_404_NOT_FOUND)

        for exercise in exercises:
            Exercise.objects.create(
                splitDay = splitday,
                name = exercise,
                date=date.today()
            )

        return Response("Created succsessfully!", status=status.HTTP_201_CREATED)
    
    if request.method == 'GET':
        exercises = Exercise.objects.filter(splitDay = splitday).values('id', 'name', 'date')
        return Response(list(exercises), status=status.HTTP_200_OK)