from django.db import models
from django.utils import timezone

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Categories"

class Item(models.Model):
    STATUS_CHOICES = [
        ('in-stock', 'In Stock'),
        ('low-stock', 'Low Stock'),
        ('out-of-stock', 'Out of Stock'),
        ('expiring-soon', 'Expiring Soon'),
        ('expired', 'Expired'),
    ]

    name = models.CharField(max_length=200)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='items')
    quantity = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    unit = models.CharField(max_length=50)
    reorder_level = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    cost_per_unit = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    supplier = models.CharField(max_length=200, blank=True)
    expiry_date = models.DateField(null=True, blank=True)
    last_updated = models.DateTimeField(auto_now=True)
    location = models.CharField(max_length=200, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='in-stock')

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        # Automatically update status based on quantity
        if self.quantity <= 0:
            self.status = 'out-of-stock'
        elif self.quantity <= self.reorder_level:
            self.status = 'low-stock'
        else:
            # Only set to in-stock if it was out-of-stock or low-stock
            if self.status in ['out-of-stock', 'low-stock']:
                self.status = 'in-stock'
        super().save(*args, **kwargs)

class Transaction(models.Model):
    TYPE_CHOICES = [
        ('purchase', 'Purchase'),
        ('usage', 'Usage'),
        ('wastage', 'Wastage'),
        ('return', 'Return'),
        ('adjustment', 'Adjustment'),
    ]

    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name='transactions', null=True)
    item_name = models.CharField(max_length=200) # Fallback for deleted items or initial data
    type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    quantity = models.DecimalField(max_digits=10, decimal_places=2)
    unit = models.CharField(max_length=50)
    date = models.DateTimeField(default=timezone.now)
    user = models.CharField(max_length=200)
    notes = models.TextField(blank=True)
    balance_after = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.type} - {self.item_name} ({self.date.strftime('%Y-%m-%d')})"

class Alert(models.Model):
    TYPE_CHOICES = [
        ('low-stock', 'Low Stock'),
        ('expiring-soon', 'Expiring Soon'),
        ('expired', 'Expired'),
        ('out-of-stock', 'Out of Stock'),
    ]
    SEVERITY_CHOICES = [
        ('critical', 'Critical'),
        ('warning', 'Warning'),
        ('info', 'Info'),
    ]

    type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name='alerts', null=True)
    item_name = models.CharField(max_length=200)
    message = models.TextField()
    severity = models.CharField(max_length=20, choices=SEVERITY_CHOICES)
    date = models.DateTimeField(default=timezone.now)
    category = models.CharField(max_length=100) # Denormalized for quick filtering

    def __str__(self):
        return f"{self.severity} Alert: {self.item_name}"
