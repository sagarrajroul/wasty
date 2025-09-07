from django.urls import path

from . import views

urlpatterns = [
    path("withdraw/<int:pk>", views.WalletUpdateApi.as_view(), name="withdraw money"),
    path("wallet/<int:user_id>", views.WalletRetrivApi.as_view(), name="see wallet money"),
    path("withdrawHistory/<int:wallet_id>", views.WithdrawHistoryRetrivApi.as_view(), name="see withdraw history"),
    path("item/<int:pk>", views.ItemRetrivUpdateApi.as_view(), name="update or delete item"),
    path("item", views.ItemCreateApi.as_view(), name="create new item"),
    path("item/list", views.ItemListApi.as_view(), name="create new item"),
    path("product/<int:pk>", views.ProductRetrivUpdateApi.as_view(), name="update or delete product"),
    path("product", views.ProductCreateApi.as_view(), name="create new product"),
    path("product/list", views.ProductListApi.as_view(), name="List all  product"),

]
