from django.urls import path
from .views import BagApi, BagDetailsApi, BagListApi

urlpatterns = [
    path("create", BagApi.as_view(), name="bag_create_api"),
    path("list", BagListApi.as_view(), name="bag_list_api"),
    path("<str:code>", BagDetailsApi.as_view(), name="bag_create_list_api")
]
