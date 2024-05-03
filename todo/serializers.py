from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.authtoken.models import Token 
from .models import Todo


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password')

    def validate_email(self, value):
        # Normalize the email to provide a consistent format
        value = value.lower().strip()
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("A user with that email already exists.")
        return value
    
    def save(self):
        api_user = User.objects.create_user(
            username=self.validated_data['username'],
            email=self.validated_data['email'],
            password=self.validated_data['password']
        )
        api_user.save()
        
        api_token = Token.objects.create(user=api_user)
        
        

class TodoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Todo
        fields = ('id', 'title', 'description', 'completed', 'created_at', 'created_by')
        read_only_fields = ('created_by',)
    
    def create(self, validated_data):
        # Add the current user from the request to the validated data
        user = self.context['request'].user
        validated_data['created_by'] = user
        return super().create(validated_data)
    
    
    
    