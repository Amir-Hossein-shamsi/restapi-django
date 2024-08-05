from .models import User
from rest_framework import serializers
from django.contrib.auth import authenticate
from django.utils.translation import gettext_lazy as _

class UserSerializer(serializers.ModelSerializer):
    
    class Meta:
        model=User
        fields=('email','password','first_name','last_name',"id")
        extra_kwargs={'password':{'write_only':True,'min_length':5},"first_name":{"default":"Unknown",'min_length':2},"last_name":{"default":"Unknown",'min_length':2}}

    def create(self,validated_data):
        """Create a new user with encrypted password and return it """
        return User.objects.create_user(**validated_data)
    



class AuthenticationSerializer(serializers.Serializer):
    email=serializers.CharField(allow_blank=False)
    password=serializers.CharField(
        style={'input_type':'password'},
        trim_whitespace=True,
        allow_blank=False)
    
    def validate(self, attrs):
        email=attrs.get('email')
        password=attrs.get('password')


        user=authenticate(self.context.get('request'),
                          username=email,
                          password=password)
        
        if not user:
            msg=_("Unable to authenticate with this credential")
            raise serializers.ValidationError(msg,code='authentication')
        
        attrs['user']=user
        # attrs['user__id']=user.id
        return attrs

