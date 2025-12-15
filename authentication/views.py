from django.shortcuts import render
from django.contrib.auth import authenticate
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import UserRegistrationSerializer
from .emails import send_verification_email


def signup_page(request):
    """Render the signup HTML page"""
    return render(request, 'authentication/signup.html')


def login_page(request):
    """Render the login HTML page"""
    return render(request, 'authentication/login.html')


def dashboard(request):
    """Render the dashboard page"""
    return render(request, 'authentication/dashboard.html')


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


@api_view(['POST'])
def login(request):
    """
    User login endpoint that returns JWT access and refresh tokens.
    Accepts username and password, validates credentials.
    """
    username = request.data.get('username')
    password = request.data.get('password')
    
    if not username or not password:
        return Response(
            {'error': 'Username and password are required'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    # Authenticate user
    user = authenticate(username=username, password=password)
    
    if user is not None:
        # Generate JWT tokens
        refresh = RefreshToken.for_user(user)
        
        return Response({
            'access': str(refresh.access_token),
            'refresh': str(refresh),
            'user': {
                'id': user.id,
                'username': user.username,
                'email': user.email
            }
        }, status=status.HTTP_200_OK)
    
    return Response(
        {'error': 'Invalid credentials'},
        status=status.HTTP_401_UNAUTHORIZED
    )


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def chat_history(request):
    """
    Protected route example - requires valid JWT token.
    Returns mock chat history for authenticated user.
    """
    return Response({
        'user': request.user.username,
        'chat_history': [
            {'id': 1, 'message': 'Hello!', 'timestamp': '2024-01-01T10:00:00Z'},
            {'id': 2, 'message': 'How are you?', 'timestamp': '2024-01-01T10:01:00Z'},
        ]
    }, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def protected_test(request):
    """
    Another protected route for testing JWT authentication.
    """
    return Response({
        'message': 'You have access to this protected route',
        'user': request.user.username,
        'user_id': request.user.id
    }, status=status.HTTP_200_OK)
