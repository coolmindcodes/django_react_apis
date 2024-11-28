from django.http import JsonResponse
from rest_framework.decorators import api_view

from mainapp.models import User
from mainapp.serializers import UserSerializer


# Create your views here.
@api_view(['GET'])
def hello(request):
    users = User.objects.all()
    serializer = UserSerializer(users, many=True)
    return JsonResponse(serializer.data, safe=False)