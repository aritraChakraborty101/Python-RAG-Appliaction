from django.shortcuts import render, get_object_or_404
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import ChatMessage, Conversation
from .serializers import (
    ChatMessageSerializer, 
    ChatRequestSerializer, 
    ConversationSerializer,
    ConversationDetailSerializer
)
from .rag_service import get_rag_service


def chat_page(request):
    """Render the chat interface"""
    return render(request, 'chat/chat_multi.html')


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def chat(request):
    """
    Handle chat requests from authenticated users
    
    POST /chat
    Body: {"message": "user question", "conversation_id": 1 (optional)}
    Returns: {"user_message": "...", "ai_response": "...", "timestamp": "...", "conversation_id": 1}
    """
    serializer = ChatRequestSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    user_message = serializer.validated_data['message']
    conversation_id = serializer.validated_data.get('conversation_id')
    
    try:
        # Get or create conversation
        if conversation_id:
            conversation = get_object_or_404(Conversation, id=conversation_id, user=request.user)
        else:
            # Create new conversation with first message as title
            title = user_message[:50] + ('...' if len(user_message) > 50 else '')
            conversation = Conversation.objects.create(
                user=request.user,
                title=title
            )
        
        # Get RAG service and generate response
        rag_service = get_rag_service()
        ai_response = rag_service.get_response(user_message)
        
        # Save to database
        chat_message = ChatMessage.objects.create(
            conversation=conversation,
            user=request.user,
            user_message=user_message,
            ai_response=ai_response
        )
        
        # Return response
        response_serializer = ChatMessageSerializer(chat_message)
        data = response_serializer.data
        data['conversation_id'] = conversation.id
        return Response(data, status=status.HTTP_201_CREATED)
        
    except Exception as e:
        return Response(
            {'error': f'Failed to process chat: {str(e)}'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def conversations_list(request):
    """
    Get list of conversations for the authenticated user
    
    GET /conversations
    Returns: List of conversations
    """
    conversations = Conversation.objects.filter(user=request.user)
    serializer = ConversationSerializer(conversations, many=True)
    return Response({
        'count': conversations.count(),
        'conversations': serializer.data
    }, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def conversation_detail(request, conversation_id):
    """
    Get a specific conversation with all messages
    
    GET /conversations/<id>
    Returns: Conversation with messages
    """
    conversation = get_object_or_404(Conversation, id=conversation_id, user=request.user)
    serializer = ConversationDetailSerializer(conversation)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def conversation_delete(request, conversation_id):
    """
    Delete a conversation and all its messages
    
    DELETE /conversations/<id>
    Returns: Success message
    """
    conversation = get_object_or_404(Conversation, id=conversation_id, user=request.user)
    conversation.delete()
    return Response(
        {'message': 'Conversation deleted successfully'},
        status=status.HTTP_200_OK
    )


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def conversation_rename(request, conversation_id):
    """
    Rename a conversation
    
    PUT /conversations/<id>/rename
    Body: {"title": "New Title"}
    Returns: Updated conversation
    """
    conversation = get_object_or_404(Conversation, id=conversation_id, user=request.user)
    
    title = request.data.get('title', '').strip()
    if not title:
        return Response(
            {'error': 'Title cannot be empty'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    conversation.title = title
    conversation.save()
    
    serializer = ConversationSerializer(conversation)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def chat_history(request):
    """
    Get chat history for the authenticated user (legacy endpoint)
    
    GET /chat-history?limit=20
    Returns: List of chat messages (newest first)
    """
    limit = request.query_params.get('limit', 20)
    try:
        limit = min(int(limit), 100)
    except ValueError:
        limit = 20
    
    messages = ChatMessage.objects.filter(user=request.user).order_by('-timestamp')[:limit]
    
    serializer = ChatMessageSerializer(messages, many=True)
    return Response({
        'count': messages.count(),
        'messages': serializer.data
    }, status=status.HTTP_200_OK)
