from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.exceptions import APIException, AuthenticationFailed
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from mainapp.authentication import generate_access_token, JWTAuthentication
from mainapp.models import User
from mainapp.serializers import UserSerializer


# Create your views here.
@api_view(['GET'])
def users(request):
    users_objects = User.objects.all()
    serializer = UserSerializer(users_objects, many=True)
    return JsonResponse(serializer.data, safe=False)

@api_view(['POST'])
def register(request):
    data = request.data
    if data['password'] != data['confirm_password']:
        raise APIException('Passwords do not match')
    serializer = UserSerializer(data=data)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return JsonResponse({'success': True,"message": 'User created successfully'})

@api_view(['POST'])
def login(request):
    email = request.data['email']
    password = request.data['password']
    user = User.objects.filter(email=email).first()
    if user is None or user.check_password(password):
        raise AuthenticationFailed('Wrong username or password')
    token = generate_access_token(user)
    response = Response()
    response.set_cookie(key='jwt', value=token, httponly=True)
    response.data = {
        'jwt': token
    }
    return response

class AuthenticatedUser(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response({"data":serializer.data})

@api_view(['POST'])
def logout(request):
    response  = Response()
    response.delete_cookie(key='jwt')
    response.data = {
        "message":"Successfully logged out"
    }
    return response