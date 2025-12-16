from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import ChatMessage
from .serializers import ChatMessageSerializer, ChatRequestSerializer
from .rag_service import get_rag_service


def chat_page(request):
    """Render the chat interface"""
    return render(request, 'chat/chat.html')


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def chat(request):
    """
    Handle chat requests from authenticated users
    
    POST /chat
    Body: {"message": "user question"}
    Returns: {"user_message": "...", "ai_response": "...", "timestamp": "..."}
    """
    # Validate request
    serializer = ChatRequestSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    user_message = serializer.validated_data['message']
    
    try:
        # Get RAG service and generate response
        rag_service = get_rag_service()
        ai_response = rag_service.get_response(user_message)
        
        # Save to database
        chat_message = ChatMessage.objects.create(
            user=request.user,
            user_message=user_message,
            ai_response=ai_response
        )
        
        # Return response
        response_serializer = ChatMessageSerializer(chat_message)
        return Response(response_serializer.data, status=status.HTTP_201_CREATED)
        
    except Exception as e:
        return Response(
            {'error': f'Failed to process chat: {str(e)}'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def chat_history(request):
    """
    Get chat history for the authenticated user
    
    GET /chat-history?limit=20
    Returns: List of chat messages (newest first)
    """
    # Get limit from query params (default 20, max 100)
    limit = request.query_params.get('limit', 20)
    try:
        limit = min(int(limit), 100)
    except ValueError:
        limit = 20
    
    # Get user's chat messages
    messages = ChatMessage.objects.filter(user=request.user)[:limit]
    
    # Serialize and return
    serializer = ChatMessageSerializer(messages, many=True)
    return Response({
        'count': messages.count(),
        'messages': serializer.data
    }, status=status.HTTP_200_OK)
