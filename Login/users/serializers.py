from rest_framework import serializers
from users.models import CustomUser
from django.contrib.auth.hashers import make_password




# --------------------------------User Register Serializer--------------------------------


class UserRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)

    class Meta:

        model = CustomUser
        fields = ("email","password","username", "name","phone_number")

    def create(self, validated_data):
        email = validated_data.pop("email", None)
        password = validated_data.pop("password", None)
        user = CustomUser.objects.create(
            email=email, password=make_password(password), **validated_data
        )
        return user

    def update(self, instance, validated_data):
        instance.__dict__.update(validated_data)
        instance.save()
        return instance


# --------------------------------User Login Serializer--------------------------------

class UserLoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ["email", "password"]



# --------------------------------User Get Data Serializer--------------------------------


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id',"email","username","name","phone_number","is_active","is_staff","is_superuser"]



