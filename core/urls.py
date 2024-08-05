

from django.urls import path
from rest_framework.routers import DefaultRouter
from . import views

# app_name='auth'

router=DefaultRouter()
router.register(r"user",viewset=views.UserCreateRetrieveViewSet)


urlpatterns=[
    path("login/",views.CustomAuthenticationToken.as_view())
]

urlpatterns += router.urls
