from django.contrib.auth import authenticate
from django.views.decorators.csrf import csrf_exempt
from rest_framework.authtoken.models import Token
from django.contrib.auth.hashers import make_password
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
    HTTP_200_OK
)
from rest_framework.response import Response
from django.contrib.auth.models import User


@csrf_exempt
@api_view(["POST"])
@permission_classes((AllowAny,)) 
def login(request):
    username = request.data.get("username")
    password = request.data.get("password")
    if username is None or password is None:
        return Response({'error': 'Please provide both username and password'},
                        status=HTTP_400_BAD_REQUEST)
    user = authenticate(username=username, password=password)
    if not user:
        return Response({'error': 'Invalid Credentials'},
                        status=HTTP_404_NOT_FOUND)
    token, _ = Token.objects.get_or_create(user=user)
    return Response({'token': token.key, 'last_login': user.last_login, "id": user.pk},
                    status=HTTP_200_OK)

def logout(request):
        # simply delete the token to force a login
        request.user.auth_token.delete()
        return Response(status=HTTP_200_OK)
@csrf_exempt
@api_view(["POST"])
@permission_classes((AllowAny,))
def keystorage(request):
    user_id = request.data.get("user_id")
    pubkey = request.data.get("keybundle")
    user = User.objects.get(pk = user_id)
    user.profile.keys = pubkey
    try:
       user.save()
       return Response(status=HTTP_200_OK)
    except Exception as e:
        print(e)
        return Response(status=HTTP_400_BAD_REQUEST)
       #
@csrf_exempt
@api_view(["GET"])
@permission_classes((AllowAny,))
def keys(request):
    user_id = request.GET.get('user_id')
    user = User.objects.get(pk = user_id)
    bundle = user.profile.keys
    return Response({'bundle':bundle}, status=HTTP_200_OK)
    #keybundle = user.profile.keys
    #print(keybundle)
    

@csrf_exempt
@api_view(["POST"])
@permission_classes((AllowAny,))
def create(request):
        user = User.objects.create(
            username=request.data.get('name'),
            email=request.data.get('email'),
            password = make_password(request.data.get('password'))
            #first_name=request.data.get('first_name'),
            #last_name=request.data.get('last_name')
        )

        #user.make_password(request.data.get('password'))
        user.save()

        return Response(status=HTTP_200_OK)