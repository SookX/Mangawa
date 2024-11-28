from django.contrib.auth.hashers import make_password
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from .models import CustomUser
from rest_framework.permissions import IsAuthenticated;
from django.shortcuts import get_object_or_404
from django.core.mail import send_mail
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.conf import settings
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator

def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

def send_activation_email(user, request):
    
    """
    Generates an activation link and sends it to the user's email.
    """

    token = default_token_generator.make_token(user)
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    
    activation_link = f"http://localhost:5173/activate/{uid}/{token}"
    
    send_mail(
        subject="Activate Your Account",
        message=f"Hi {user.username}, please activate your account using the following link: {activation_link}",
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[user.email],
    )

@api_view(['POST'])
def register(request):
    username = request.data.get('username')
    first_name = request.data.get('first_name', '')
    last_name = request.data.get('last_name', '')
    email = request.data.get('email')
    password = request.data.get('password')
    age = request.data.get('age', None)
    gender = request.data.get('gender', '')

    if not email or not password or not username:
        return Response(
            {"error": "Email, username, and password are required"},
            status=status.HTTP_400_BAD_REQUEST
        )

    if CustomUser.objects.filter(email=email).exists():
        return Response(
            {"error": "User with this email already exists"},
            status=status.HTTP_400_BAD_REQUEST
        )

    if CustomUser.objects.filter(username=username).exists():
        return Response(
            {"error": "Username already taken"},
            status=status.HTTP_400_BAD_REQUEST
        )

    user = CustomUser.objects.create(
        username=username,
        first_name=first_name,
        last_name=last_name,
        email=email,
        password=make_password(password),
        age=age,
        gender=gender,
        is_active=False
    )

    send_activation_email(user, request)    

    return Response(
        {"message": "User registered successfully. Please check your email to activate your account."},
        status=status.HTTP_201_CREATED
    )

@api_view(['POST'])
def login(request):
    email = request.data.get('email')
    password = request.data.get('password')

    if not email or not password:
        return Response(
            {"error": "Email and password are required"},
            status=status.HTTP_400_BAD_REQUEST
        )

    try:
        user = CustomUser.objects.get(email=email)
    except CustomUser.DoesNotExist:
        return Response(
            {"error": "Invalid email or password"},
            status=status.HTTP_401_UNAUTHORIZED
        )

    if not user.check_password(password):
        return Response(
            {"error": "Invalid email or password"},
            status=status.HTTP_401_UNAUTHORIZED
        )

    if not user.is_active:
        return Response(
            {"error": "User is inactive. Please activate your account."},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    token = get_tokens_for_user(user)

    return Response({
        "message": "Login successful",
        "token": token,
        "user": {
            "id": user.id,
            "username": user.username,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "email": user.email,
            "age": user.age,
            "gender": user.gender
        }
    }, status=status.HTTP_200_OK)

@api_view(['POST', 'GET', 'PUT'])
@permission_classes([IsAuthenticated])
def user(request, id=None):

    """
    Handles retrieving a user by ID or a list of all users. If a PUT request is received, updates the password for the authenticated user.
    Validates old and new passwords before updating the user's password.
    Returns appropriate success or error messages based on the operation.
    """

    
    if request.method == 'GET' and id is not None:
        user = get_object_or_404(CustomUser, pk=id)
        return Response({
        "user": {
            "id": user.id,
            "username": user.username,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "email": user.email,
            "age": user.age,
            "gender": user.gender
        }
    }, status=status.HTTP_200_OK)

    if request.method == 'GET' and id is None:
        users = CustomUser.objects.values('id', 'username', 'first_name', 'last_name', 'email', 'age', 'gender')
        return Response(list(users))
    
    if request.method == 'PUT':
        user = request.user
        old_password = request.data.get('old_password')
        new_password = request.data.get('new_password')

        if not old_password or not new_password:
            return Response(
                {"error": "Both old_password and new_password are required"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if not user.check_password(old_password):
            return Response(
                {"error": "Old password is incorrect"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        user.set_password(new_password)
        user.save()

        return Response({"message": "Password has been changed successfully"}, status=status.HTTP_200_OK)

@api_view(['GET'])
def activate_user(request, uidb64, token):
    
    """
    Activates the user account by verifying the activation token.
    Decodes the user ID from the URL, checks the validity of the token,
    and sets the user's account to active if the token is valid.
    Returns a success message if the account is activated, or an error message 
    if the token is invalid or expired.
    """
    
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = CustomUser.objects.get(pk=uid)
        if user.is_active is True:
            return Response({"error": "The user is allready activated!"}, status=status.HTTP_400_BAD_REQUEST)
    except (TypeError, ValueError, OverflowError, CustomUser.DoesNotExist):
        return Response({"error": "Invalid activation link"}, status=status.HTTP_400_BAD_REQUEST)

    if default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        return Response({"message": "Account activated successfully"}, status=status.HTTP_200_OK)
    else:
        return Response({"error": "Invalid or expired token"}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def forgot_password(request):
    
    """
    Handles password reset requests. Verifies the email provided in the request,
    generates a password reset token and unique ID, and sends a password reset link
    to the user's email. Returns a success message if the email is valid, or an 
    error message if the email does not exist.
    """
    
    email = request.data.get('email')
    if not email:
        return Response({"error": "Email is required"}, status=status.HTTP_400_BAD_REQUEST)

    try:
        user = CustomUser.objects.get(email=email)
    except CustomUser.DoesNotExist:
        return Response({"error": "User with this email does not exist"}, status=status.HTTP_404_NOT_FOUND)

    token = default_token_generator.make_token(user)
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    reset_link = f"http://localhost:5173/reset-password/{uid}/{token}"

    send_mail(
        subject="Reset Your Password",
        message=f"Hi {user.username}, use the link below to reset your password: {reset_link}",
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[email],
    )

    return Response({"message": "Password reset link has been sent to your email"}, status=status.HTTP_200_OK)

@api_view(['POST'])
def reset_password(request, uidb64, token):

    """
    Handles resetting a user's password using a unique ID and token.
    Decodes the user ID, validates the token, and updates the user's password
    if the token is valid. Returns a success message if the password is reset,
    or an error message if the token or reset link is invalid or expired.
    """


    new_password = request.data.get('password')
    if not new_password:
        return Response({"error": "Password is required"}, status=status.HTTP_400_BAD_REQUEST)

    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = CustomUser.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, CustomUser.DoesNotExist):
        return Response({"error": "Invalid or expired reset link"}, status=status.HTTP_400_BAD_REQUEST)

    if not default_token_generator.check_token(user, token):
        return Response({"error": "Invalid or expired reset token"}, status=status.HTTP_400_BAD_REQUEST)

    user.set_password(new_password)
    user.save()
    return Response({"message": "Password has been reset successfully"}, status=status.HTTP_200_OK)
