from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from .models import Todo
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from .serializers import UserSerializer, TodoSerializer
from rest_framework.generics import ListAPIView, CreateAPIView, RetrieveAPIView, UpdateAPIView, DestroyAPIView
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.authtoken.models import Token 
from rest_framework.filters import SearchFilter,OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend

# Create your views here.
@api_view(["POST"])
def signup(request):
    serializer = UserSerializer(data=request.data)
    
    if serializer.is_valid():
        serializer.save()
        
        user = User.objects.get(username=request.data["username"])
        token = Token.objects.get(user=user)
        serializer = UserSerializer(user)
        
        data = {
            "user": {"id": serializer.data["id"],
                     "username": serializer.data["username"],
                     "email": serializer.data["email"]},
            "token": token.key
        }
        
        return Response(data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
def login(request):
    username = request.data.get('username')
    password = request.data.get('password')
    user = authenticate(username=username, password=password)

    if user:
        token, _ = Token.objects.get_or_create(user=user)
        serializer = UserSerializer(user)
        response_data = {
            'user': serializer.data,
            'token': token.key
        }
        return Response(response_data)
    return Response({"detail": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)
    
    
class CreateListTodos(ListAPIView, CreateAPIView):
    serializer_class = TodoSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['title', 'completed']
    search_fields = ['=description']
    ordering_fields = ['created_at']
    
    def get_queryset(self):
        # Only return todos for the current user
        return Todo.objects.filter(created_by=self.request.user)
    
    

class RetrieveUpdateDestroyTodo(RetrieveAPIView, UpdateAPIView, DestroyAPIView):
    serializer_class = TodoSerializer
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]