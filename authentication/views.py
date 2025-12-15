from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import UserRegistrationSerializer
from .emails import send_verification_email


def signup_page(request):
    """Render the signup HTML page"""
    return render(request, 'authentication/signup.html')


@api_view(['POST'])
def signup(request):
    serializer = UserRegistrationSerializer(data=request.data)
    
    if serializer.is_valid():
        user = serializer.save()
        
        # Send verification email asynchronously (non-blocking)
        send_verification_email(user.username, user.email)
        
        return Response(
            {'message': 'User registered successfully'},
            status=status.HTTP_201_CREATED
        )
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
