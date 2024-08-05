from rest_framework import mixins,status,permissions,authentication
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.viewsets import GenericViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.settings import api_settings

from core.models import User
from .serializer import AuthenticationSerializer, UserSerializer


# class UserViewAPI(ViewSet):   
#     def list(self, request):
#         queryset = get_user_model.objects.all()
#         serializer = UserSerializer(queryset, many=True)
#         return Response(serializer.data) 

#     def create(self,request):
#         serializer=UserSerializer(data=request.data)
#         if serializer.is_valid(): 
#             serializer.save() 
#             user=get_user_model.objects.create_user(serializer.data)
#             return Response(user, 
#                             status=status.HTTP_201_CREATED)     
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST) 



class CustomAuthenticationToken(ObtainAuthToken):
    renderer_classes=api_settings.DEFAULT_RENDERER_CLASSES
    serializer_class=AuthenticationSerializer



    
class UserCreateRetrieveViewSet(mixins.CreateModelMixin,mixins.RetrieveModelMixin,GenericViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    http_method_names = ['get','post']
    lookup_field = "pk"
    authentication_classes=(authentication.TokenAuthentication,)
    # permission_classes=[permissions.IsAuthenticated,]

    def get_permissions(self):
        if self.action == 'retrieve':
            permission_classes = (permissions.IsAuthenticated,)
        else:
            permission_classes = []
        return [permission() for permission in permission_classes]


    def create(self, request, *args, **kwargs):    
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(data=serializer.data,status=status.HTTP_201_CREATED)
        return Response(data=serializer.errors,status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        # query = request.GET.get('query', None)  # read extra data
        return Response(self.serializer_class(instance).data,
                        status=status.HTTP_200_OK)




