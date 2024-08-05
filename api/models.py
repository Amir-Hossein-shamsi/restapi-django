from uuid import uuid4
from django.db import models
from django.core.validators import MinValueValidator

class Collection(models.Model):
    title=models.CharField(max_length=255)
    featured_product = models.ForeignKey(
        'Product', on_delete=models.SET_NULL, null=True, related_name='+', blank=True)
    
    def __str__(self) -> str:
        return self.title
    
    class Meta:
        ordering=['title']



class Product(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    unit_price = models.DecimalField(
        max_digits=6, decimal_places=2, validators=[MinValueValidator(1)])
    inventory = models.IntegerField()
    last_update = models.DateTimeField(auto_now=True,null=True)
    collection = models.ForeignKey(
        Collection, on_delete=models.PROTECT, related_name='products')
    
    def __str__(self) -> str:
        return f"product is {self.title}"
    
    class Meta:
        ordering=['last_update']




class Cart(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4)
    create_at = models.DateField(auto_now_add=True)


class CartItem(models.Model):
    cart = models.ForeignKey(
        Cart, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1)]
    )

    class Meta:
        unique_together = [['cart', 'product']]    