from django.shortcuts import render
from rest_framework.decorators import api_view
from .models import User
from .userserializer import UserSerializer, LoginSerialzer
from rest_framework.response import Response
from django.conf import settings
import jwt
import datetime 


@api_view(["POST"])
def login(request):
    serializerData = LoginSerialzer(data=request.data)

    if serializerData.is_valid():
        clientuserdata = serializerData.validated_data

        try:
            realuserdata = User.objects.get(userName=clientuserdata["userName"])
            realuserdata = UserSerializer(realuserdata).data
            payload = {
                    "userId" : clientuserdata["userName"],
                    "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=1),
                    "iat": datetime.datetime.utcnow()
                }
            token = jwt.encode(payload, settings.SECRET_KEY, algorithm="HS256")
            if realuserdata["password"] == clientuserdata["password"]:
                print(clientuserdata)
                return Response(data={
                    "token":token,
                    "msg":"Login Successfull"
                })
            else:
                return Response({
                    "msg": "Invalid Username/Password"
                })

        except:
            return Response({
                "msg": "Invalid Username/Password"
            })

    return Response(serializerData.errors)


@api_view(["POST"])
def register(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({
            "mssg":"Account Creation Successful",
            "userdata":serializer.data
        })
    else:
        return Response({
            "mssg":"Account creation Failed", "Error":serializer.errors
        })

@api_view(["POST"])  
def check(request):
    user_id = request.headers["Authorization"]
    print(user_id)
    user_id = user_id.split(" ")[1]
    user_data = jwt.decode(user_id , settings.SECRET_KEY , algorithms="HS256")
    return Response(
       {
           "mssg":"Token generation",
           "token":user_id
       }
    )

