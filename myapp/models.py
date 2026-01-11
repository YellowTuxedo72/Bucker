from django.db import models
from django.contrib.auth.models import User
from django.conf import settings


class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    image = models.ImageField(upload_to='products/')
    date_of_creation = models.DateTimeField(auto_now_add=True)
    in_stock = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class WishlistItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='wishlist')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'product')

    def __str__(self):
        return f"{self.user.username} - {self.product.name}"
    

class Cart(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='cart')
    def __str__(self):
        return f'Корзина пользователя: {self.user}'
    
class CartDetails(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='cart_detatils')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    class Meta:
        unique_together = ('cart', 'product')

    def __str__(self):
        return f'{self.product.name} ({self.quantity})'
    
    @property
    def total_price(self):
        return self.product.price * self.quantity
        
class OrderStatus(models.TextChoices):
    PROCESSING = 'processing', 'В обработке'
    SHIPPED = 'shipped', 'Отправлен'
    CANCELED = 'canceled', 'Отменён'
    
class Order(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='orders'
    )

    status = models.CharField(
        max_length=20,
        choices=OrderStatus.choices
    )

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    postcode = models.CharField(max_length=20)
    email = models.EmailField()
    phone = models.CharField(max_length=20)

    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    date_of_creation = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Заказ #{self.id} ({self.get_status_display()})'


class OrderDetails(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField()

    def get_total(self):
        return self.price * self.quantity
