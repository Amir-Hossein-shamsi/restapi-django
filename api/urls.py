from django.urls import path
from rest_framework_nested import routers

from .views import CollectionViewSet,ProductViewSet

router=routers.DefaultRouter()

router.register(r'collection',viewset=CollectionViewSet)
router.register(r"product",viewset=ProductViewSet)







urlpatterns=router.urls