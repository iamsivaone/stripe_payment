import uuid

from django.db import models


class Invoice(models.Model):
    invoice_number = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=30)
    email = models.EmailField(max_length=100)
    project_name = models.CharField(max_length=150)
    amount = models.DecimalField(max_digits=7, decimal_places=2)

    def __str__(self):
        return self.name
