from django.core.serializers import serialize
from django.http import JsonResponse
from rest_framework import viewsets, status, generics, mixins
from rest_framework.decorators import api_view
from rest_framework.exceptions import APIException, AuthenticationFailed
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from mainapp.authentication import generate_access_token, JWTAuthentication
from mainapp.models import User, Permission, Role
from mainapp.serializers import UserSerializer, PermissionSerializer, RoleSerializer


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
    return JsonResponse({'success': True, "message": 'User created successfully'})


@api_view(['POST'])
def login(request):
    email = request.data['email']
    password = request.data['password']
    user = User.objects.filter(email=email).first()
    if user is None or user.check_password(password) == False:
        raise AuthenticationFailed('Wrong username or password. Try again')
    token = generate_access_token(user)
    response = Response()
    response.set_cookie(key='jwt', value=token, httponly=True)
    response.data = {
        'jwt': token
    }
    return response


@api_view(['POST'])
def logout(_):
    response = Response()
    response.delete_cookie(key='jwt')
    response.data = {
        "message": "Successfully logged out"
    }
    return response


class AuthenticatedUser(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response({"data": serializer.data})


class PermissionApiView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = PermissionSerializer(Permission.objects.all(), many=True)
        return Response({"data": serializer.data})


class RoleViewSet(viewsets.ViewSet):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def list(self, request):
        serializer = RoleSerializer(Role.objects.all(), many=True)
        return Response({"data": serializer.data})

    def retrieve(self, request, pk=None):
        serializer = RoleSerializer(Role.objects.get(id=pk))
        return Response({"data": serializer.data})

    def create(self, request):
        serializer = RoleSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"data": serializer.data}, status=status.HTTP_201_CREATED)

    def update(self, request, pk=None):
        serializer = RoleSerializer(Role.objects.get(id=pk), data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"data": serializer.data}, status=status.HTTP_202_ACCEPTED)

    def destroy(self, request, pk=None):
        role = Role.objects.get(id=pk)
        if role:
            role.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response({"data": "Role not found"})


class UserApiView(generics.GenericAPIView, mixins.ListModelMixin, mixins.RetrieveModelMixin):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer
    queryset = User.objects.all()

    def get(self, request, pk=None):
        if pk:
            return Response({"data": self.retrieve(request, pk).data})
        else:
            return Response({"data": self.list(request).data})

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"data": serializer.data}, status=status.HTTP_201_CREATED)

    def put(self, request, pk=None):
        serializer = UserSerializer(User.objects.get(id=pk), data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"data": serializer.data}, status=status.HTTP_202_ACCEPTED)

    def delete(self, request, pk=None):
        user = User.objects.get(id=pk)
        if user:
            user.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response({"data": "User not found"})

    def patch(self, request, pk=None):
        user = User.objects.get(id=pk)
        if user:
            serializer = UserSerializer(user, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response({"data": serializer.data}, status=status.HTTP_202_ACCEPTED)
