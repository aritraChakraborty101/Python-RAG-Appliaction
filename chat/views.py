from django.shortcuts import render, get_object_or_404
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from .models import ChatMessage, Conversation
from .serializers import (
    ChatMessageSerializer, 
    ChatRequestSerializer, 
    ConversationSerializer,
    ConversationDetailSerializer
)
from .rag_service import get_rag_service
from .scheduler import get_scheduled_jobs, run_job_now
from .tasks import (
    run_all_housekeeping_tasks,
    delete_old_conversations,
    cleanup_orphaned_messages,
    cleanup_inactive_users,
    generate_statistics
)


def chat_page(request):
    """Render the chat interface"""
    return render(request, 'chat/chat_multi.html')


def scheduler_admin_page(request):
    """Render the scheduler admin interface"""
    return render(request, 'chat/scheduler_admin.html')


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


# Admin-only scheduler management endpoints

@api_view(['GET'])
@permission_classes([IsAdminUser])
def scheduler_status(request):
    """
    Get scheduler status and list of scheduled jobs (Admin only)
    
    GET /admin/scheduler/status
    Returns: Scheduler information and job list
    """
    jobs = get_scheduled_jobs()
    return Response({
        'status': 'running' if jobs else 'not_running',
        'total_jobs': len(jobs),
        'jobs': jobs
    }, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAdminUser])
def trigger_task(request):
    """
    Manually trigger a housekeeping task (Admin only)
    
    POST /admin/scheduler/trigger
    Body: {"task": "all|conversations|messages|users|stats"}
    Returns: Task result
    """
    task_name = request.data.get('task', 'all')
    
    try:
        if task_name == 'all':
            result = run_all_housekeeping_tasks()
            return Response({
                'message': 'All housekeeping tasks completed',
                'result': result
            }, status=status.HTTP_200_OK)
        
        elif task_name == 'conversations':
            count = delete_old_conversations()
            return Response({
                'message': f'Deleted {count} old conversations',
                'deleted_count': count
            }, status=status.HTTP_200_OK)
        
        elif task_name == 'messages':
            count = cleanup_orphaned_messages()
            return Response({
                'message': f'Cleaned {count} orphaned messages',
                'cleaned_count': count
            }, status=status.HTTP_200_OK)
        
        elif task_name == 'users':
            count = cleanup_inactive_users()
            return Response({
                'message': f'Deleted {count} inactive users',
                'deleted_count': count
            }, status=status.HTTP_200_OK)
        
        elif task_name == 'stats':
            stats = generate_statistics()
            return Response({
                'message': 'Statistics generated',
                'statistics': stats
            }, status=status.HTTP_200_OK)
        
        else:
            return Response(
                {'error': 'Invalid task name. Choose: all, conversations, messages, users, or stats'},
                status=status.HTTP_400_BAD_REQUEST
            )
    
    except Exception as e:
        return Response(
            {'error': f'Task failed: {str(e)}'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['GET'])
@permission_classes([IsAdminUser])
def system_statistics(request):
    """
    Get current system statistics (Admin only)
    
    GET /admin/scheduler/statistics
    Returns: System usage statistics
    """
    try:
        stats = generate_statistics()
        return Response(stats, status=status.HTTP_200_OK)
    except Exception as e:
        return Response(
            {'error': f'Failed to generate statistics: {str(e)}'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
