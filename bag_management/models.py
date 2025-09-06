from django.conf import settings
from django.db import models

class Bag(models.Model):
    code = models.CharField(max_length=128, unique=True, db_index=True)  # QR payload
    label = models.CharField(max_length=120, blank=True)
    assigned_to = models.ForeignKey(
        settings.AUTH_USER_MODEL, null=True, blank=True,
        on_delete=models.CASCADE, related_name="bags"
    )
    assigned_at = models.DateTimeField(null=True, blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = "BAG"

