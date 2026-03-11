from django.db import models
from menu_app.models import Pizza
from customers_app.models import Customer


class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def subtotal(self):
        """Suma przed rabatem."""
        return sum(item.total_price for item in self.items.all())

    @property
    def discount_amount(self):
        """Kwota rabatu VIP."""
        if self.customer.is_vip:
            return round(self.subtotal * self.customer.discount_percent / 100, 2)
        return 0

    @property
    def total_price(self):
        """Suma po rabacie."""
        return round(self.subtotal - self.discount_amount, 2)

    def __str__(self):
        return f"Zamowienie #{self.id} ({self.customer.name})"

    class Meta:
        ordering = ['-created_at']


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    pizza = models.ForeignKey(Pizza, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    unit_price = models.FloatField(blank=True, null=True)

    @property
    def total_price(self):
        return self.unit_price * self.quantity

    def save(self, *args, **kwargs):
        if not self.unit_price:
            self.unit_price = self.pizza.price
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.quantity}x {self.pizza.name}"