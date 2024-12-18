from django.db import models


class TimeStampedModel(models.Model):
    """
    Abstract class to add created_at and updated_at fields.
    """

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Category(TimeStampedModel):
    name = models.CharField(max_length=50)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name


class Item(TimeStampedModel):
    
    PURCHASE_STATUS_CHOICES = [
        ("buy", "Buy"),
        ("low_stock", "Low Stock"),
        ("out_of_stock", "Out of Stock"),
        ("available", "Available"),
    ]

    name = models.CharField(max_length=50)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    purchase_status = models.CharField(
        max_length=20, choices=PURCHASE_STATUS_CHOICES, default="available"
    )
    
    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        # Check if status has changed
        if self.pk:  # Only for existing items
            old_item = Item.objects.get(pk=self.pk)
            if old_item.purchase_status != self.purchase_status:
                InventoryLog.objects.create(
                    item=self,
                    previous_status=old_item.purchase_status,
                    new_status=self.purchase_status
                )
        super().save(*args, **kwargs)  # Call the parent save method


class InventoryLog(models.Model):
    ACTION_CHOICES = [("status_change", "Status Change")]

    item = models.ForeignKey(
        Item, on_delete=models.CASCADE, related_name="status_change_logs"
    )
    previous_status = models.CharField(max_length=20)
    new_status = models.CharField(max_length=20)
    action = models.CharField(
        max_length=20, choices=ACTION_CHOICES, default="status_change"
    )
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.item.name} changed from {self.previous_status} to {self.new_status} on {self.timestamp}"
