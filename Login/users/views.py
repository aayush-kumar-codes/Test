from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from . import serializers
from . import models
from rest_framework.authtoken.models import Token
from .models import CustomUser
from django.contrib.auth import authenticate




# --------------------------------User Register View--------------------------------

class UserRegister(APIView):
    def get_serializer(self):
        return serializers.UserRegisterSerializer()

    def post(self, request):
        serializer = serializers.UserRegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            token = Token.objects.create(user=user)
            json = serializer.data
            json["token"] = token.key
            return Response(
                {
                    "key": token.key,
                    "message": "Success",
                },
                status=status.HTTP_201_CREATED,
            )
        else:
            data = {"error": True, "errors": serializer.errors}
            return Response(data, status=status.HTTP_400_BAD_REQUEST)





# --------------------------------User Login View--------------------------------

class UserAuth(APIView):
    def get_serializer(self):
        return serializers.UserLoginSerializer()

    def post(self, request):
        isemail = CustomUser.objects.filter(email=request.data.get("email"))
        if not isemail:
            data = {
                "message": "Account with this email does not exist",
                "field": "email",
            }
            return Response(data, status=status.HTTP_401_UNAUTHORIZED)
        if not isemail[0].is_active:
            data = {
                "message": "your account is not activated",
                "field": "email",
            }
            return Response(data, status=status.HTTP_401_UNAUTHORIZED)

        user = authenticate(
            email=request.data.get("email"), password=request.data.get("password")
        )
        if user is not None:
            try:
                token = Token.objects.get(user_id=user.id)
            except:
                token = Token.objects.create(user=user)
            return Response({"key": token.key, "message": "Login Successful"})
        else:
            data = {
                "field": "password",
                "message": "This password is incorrect, please try again",
            }

            return Response(data, status=status.HTTP_401_UNAUTHORIZED)




# --------------------------------Get User Data and User UpdateView--------------------------------

class User(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = serializers.UserSerializer(
            models.CustomUser.objects.get(pk=request.user.id)
        )
        return Response(serializer.data)

    def get_serializer(self):
        return serializers.UserSerializer()

    def patch(self, request):
        objects = models.CustomUser.objects.filter(email=request.user.email).first()
        serializer = serializers.UserSerializer(
            objects, data=request.data, partial=True
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




# --------------------------------Get User Delete View--------------------------------


class UserDelete(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request):
        email = request.data.get("email")
        if not email:
            return Response({"status":"email is required"},status=status.HTTP_400_BAD_REQUEST)
        models.CustomUser.objects.filter(email=email).delete()
        return Response({"status":"deleted"},status=status.HTTP_204_NO_CONTENT)



# --------------------------------Get All User List View--------------------------------


class UserList(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        objects = models.CustomUser.objects.all()
        serializer = serializers.UserSerializer(objects,many=True)
        return Response(serializer.data)
