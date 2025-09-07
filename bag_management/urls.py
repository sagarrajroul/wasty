from django.urls import path
from . import views

urlpatterns = [
    path("", views.CreateBagApi.as_view(), name="create_bag"),
    path("add-waste-product/<int:bag_id>", views.AddWasteProductAPIView.as_view(), name="add_waste_product"),
    path("bag-products-history/<int:bag_id>", views.BagProductHistoryAPIView.as_view(), name="bag_products_history"),
    path("assign", views.AssignAPIView.as_view(), name="scan_qr"),
    path("unassign", views.UnassignBagAPIView.as_view(), name="unassign_bag"),
    path("user-history/<int:user_id>", views.UserBagHistoryAPIView.as_view(), name="user_bag_history"),
    path("check/<str:qr_code>", views.CheckBagApi.as_view(), name="check_bag_details"),

]
