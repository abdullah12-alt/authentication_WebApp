from django.shortcuts import render
from rest_framework.response import Response
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from .serializers import UserSerializer
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from django.contrib.auth import logout
# Create your views here.
from rest_framework.views import APIView
class RegisterUser(APIView):
    allowed_methods = ['POST']

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if not serializer.is_valid():
            return Response({'status': 403, 'errors': serializer.errors, 'message': 'something went wrong'})
        serializer.save()
        user = User.objects.get(username=serializer.data['username'])
        token_obj , _ = Token.objects.get_or_create(user=user)
        return Response({'status': 200, 'payload': serializer.data, 'message': 'your data is saved'})


class LoginUser(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        token = Token.objects.get(key=response.data['token'])
        return Response({'status': 200, 'token': token.key, 'user_id': token.user_id, 'message': 'login successful'})


class LogoutUser(APIView):
    def post(self, request):
        try:
            request.user.auth_token.delete()
        except (AttributeError, Token.DoesNotExist):
            pass
        logout(request)
        return Response({'status': 200, 'message': 'logout successful'})