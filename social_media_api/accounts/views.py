from rest_framework import status, generics
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.contrib.auth import login
from django.shortcuts import get_object_or_404
from .models import CustomUser
from .serializers import (
    UserRegistrationSerializer, 
    UserLoginSerializer, 
    UserProfileSerializer,
    UserListSerializer
)

@api_view(['GET'])
@permission_classes([AllowAny])
def accounts_root(request):
    """Accounts API root endpoint showing available user management endpoints"""
    endpoints = {
        'message': 'User Management API',
        'endpoints': {
            'register': '/api/accounts/register/',
            'login': '/api/accounts/login/',
            'profile': '/api/accounts/profile/',
            'list_users': '/api/accounts/users/',
            'follow_user': '/api/accounts/follow/<user_id>/',
        },
        'authentication': 'Token-based authentication required for most endpoints',
        'registration_fields': ['username', 'email', 'password'],
        'login_fields': ['username', 'password']
    }
    return Response(endpoints)

@api_view(['POST'])
@permission_classes([AllowAny])
def register(request):
    serializer = UserRegistrationSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user_id': user.id,
            'username': user.username,
            'message': 'User registered successfully'
        }, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([AllowAny])
def login_user(request):
    serializer = UserLoginSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        login(request, user)
        return Response({
            'token': token.key,
            'user_id': user.id,
            'username': user.username,
            'message': 'Login successful'
        }, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT'])
@permission_classes([IsAuthenticated])
def profile(request):
    if request.method == 'GET':
        serializer = UserProfileSerializer(request.user)
        return Response(serializer.data)
    
    elif request.method == 'PUT':
        serializer = UserProfileSerializer(request.user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST', 'DELETE'])
@permission_classes([IsAuthenticated])
def follow_user(request, user_id):
    try:
        user_to_follow = CustomUser.objects.get(id=user_id)
    except CustomUser.DoesNotExist:
        return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
    
    if user_to_follow == request.user:
        return Response({'error': 'Cannot follow yourself'}, status=status.HTTP_400_BAD_REQUEST)
    
    if request.method == 'POST':
        request.user.following.add(user_to_follow)
        return Response({'message': f'Now following {user_to_follow.username}'})
    
    elif request.method == 'DELETE':
        request.user.following.remove(user_to_follow)
        return Response({'message': f'Unfollowed {user_to_follow.username}'})

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_users(request):
    users = CustomUser.objects.exclude(id=request.user.id)
    serializer = UserListSerializer(users, many=True)
    return Response(serializer.data)
