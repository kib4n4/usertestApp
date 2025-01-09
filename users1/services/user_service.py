#services/user_service.py

from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from django.contrib.auth.models import Group
from django.core.exceptions import ValidationError
from ..common.validators import missing_required_fields
from ..models.user_model import User
from django.contrib.auth.models import Group


class UserService:
    def __init__(self):
        self.model = User

    def create_user(self, data):
        # Validate required fields
        required_fields = ['username', 'email', 'password']
        missing_fields = missing_required_fields(data, required_fields)

        if missing_fields:
            raise ValidationError(f"Missing required fields: {missing_fields}")

        # Create the user
        user = self.model.objects.create_user(
            username=data['username'],
            email=data['email'],
            password=data['password']
        )

        # Generate a token for the user
        token, created = Token.objects.get_or_create(user=user)

        # Return user and token data
        return {
            'id': str(user.id),
            'username': user.username,
            'email': user.email,
            'token': token.key
        }

    def login_user(self, data):
        # Validate required fields
        required_fields = ['email', 'password']
        missing_fields = missing_required_fields(data, required_fields)

        if missing_fields:
            raise ValidationError(f"Missing login required fields: {missing_fields}")

        email = data['email']
        password = data['password']

        # Authenticate the user
        user = authenticate(username=email, password=password)
        if not user:
            print("invalid email or password")
            raise ValidationError("Invalid email or password")

        if not user.is_active:
            raise ValidationError("Account is deactivated")

        # Generate or retrieve the token
        token, created = Token.objects.get_or_create(user=user)

        # Return user and token data
        return {
            'username': user.username,
            'email': user.email,
            'token': token.key
        }

    def list_users(self):
        # Retrieve all users
        return list(self.model.objects.values('id', 'username', 'email', 'date_joined'))

    def assign_role(self,user_id,role_group_name,requester):
        if not requester.is_superuser:
            raise ValidationError("Only superusers can assign roles.")
        user = self.model.objects.get(id=user_id)
        group, created = Group.objects.get_or_create(name=role_group_name)
        group.user_set.add(user)
        return {
            'message':f"Role{role_group_name} assigned to user {user.username} successfully"
        }