from django.db import models
from django.contrib.auth import get_user_model
import uuid

User= get_user_model()

class WasteBag(models.Model):
    qr_code = models.CharField(max_length=255, unique=True, default=uuid.uuid4)
    assigned_to = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True, related_name="bags"
    )
    is_assigned = models.BooleanField(default=False)
    assigned_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "WASTE_BAG"


class BagAssignmentHistory(models.Model):
    bag = models.ForeignKey(WasteBag, on_delete=models.CASCADE, related_name="assignment_history")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    assign_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "BAG_ASSIGNMENT_HISTORY"


class WasteProduct(models.Model):
    session = models.ForeignKey(BagAssignmentHistory, on_delete=models.CASCADE, related_name="products")
    name = models.CharField(max_length=100)
    weight = models.FloatField(default=0.0)  # in kilograms
    category = models.CharField(
        max_length=50,
        choices=[
            ("plastic", "Plastic"),
            ("metal", "Metal"),
            ("organic", "Organic"),
            ("glass", "Glass"),
            ("other", "Other"),
        ],
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "WASTE_PRODUCT"