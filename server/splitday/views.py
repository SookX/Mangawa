from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from .models import SplitDay, Exercise, KgAndReps
from rest_framework.permissions import IsAuthenticated;
from datetime import date
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from datetime import datetime

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

@api_view(['POST', 'GET'])
def kgandreps(request, id = None):

    if request.method == 'POST':
        exercise = get_object_or_404(Exercise, pk = id)
        kg = request.data.get('kg')
        reps = request.data.get('reps')
        dates = request.data.get('date')
        
        if id is None:
            return Response("No id provided!", status=status.HTTP_400_BAD_REQUEST)

        if dates:
            dates = datetime.strptime(dates, '%Y-%m-%d').date()
        else:
            dates = date.today()
        
        createdKgAndReps = KgAndReps.objects.create(
            exercise = exercise,
            kg = kg,
            reps = reps,
            date = dates
        )

        return Response({
            "message": "Kg and reps created!",
            "exercise_id": createdKgAndReps.exercise.id,
            "kg": createdKgAndReps.kg,
            "reps": createdKgAndReps.reps,
            "date": createdKgAndReps.date
        }, status=status.HTTP_201_CREATED)
    
    if request.method == 'GET':
        start_date = request.GET.get('start_date')
        end_date = request.GET.get('end_date')
        
        if id is None:
            kgandreps = KgAndReps.objects.all().values('id', 'kg', 'reps', 'date')
        else:
            exercise = get_object_or_404(Exercise, pk = id)
            try:
                if start_date:
                    start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
                if end_date:
                    end_date = datetime.strptime(end_date, '%Y-%m-%d').date()
            except ValueError:
                return Response({"error": "Invalid date format. Use YYYY-MM-DD."}, status=status.HTTP_400_BAD_REQUEST)
            
            if start_date and end_date:
                kgandreps = KgAndReps.objects.filter(exercise = exercise, date__range=[start_date, end_date]).values('id', 'kg', 'reps', 'date')
            elif start_date:
                kgandreps = KgAndReps.objects.filter(exercise = exercise, date=start_date).values('id', 'kg', 'reps', 'date')
            else:
                kgandreps = KgAndReps.objects.filter(exercise = exercise).values('id', 'kg', 'reps', 'date')

        if id is None:
            kgandreps = KgAndReps.objects.all().values('id', 'kg', 'reps', 'date')

        return Response(list(kgandreps), status=status.HTTP_200_OK)