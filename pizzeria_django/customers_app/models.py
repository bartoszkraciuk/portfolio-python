from django.db import models
from django.core.exceptions import ValidationError


class Customer(models.Model):
    CUSTOMER_TYPES = [
        ('regular', 'Zwykly klient'),
        ('vip', 'VIP'),
    ]

    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    customer_type = models.CharField(max_length=10, choices=CUSTOMER_TYPES, default='regular')
    discount_percent = models.FloatField(default=0)
    loyalty_points = models.IntegerField(default=0)

    def clean(self):
        if self.customer_type == 'vip' and (self.discount_percent < 0 or self.discount_percent > 100):
            raise ValidationError({'discount_percent': 'Rabat musi byc w zakresie 0-100%'})
        if not self.name:
            raise ValidationError({'name': 'Nazwa klienta nie moze byc pusta!'})

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    @property
    def is_vip(self):
        return self.customer_type == 'vip'

    def __str__(self):
        vip_tag = " (VIP)" if self.is_vip else ""
        return f"{self.name}{vip_tag}"

    class Meta:
        ordering = ['name']