from decimal import ROUND_DOWN, Decimal
from rest_framework import serializers

from .models import Cart, CartItem, Collection, Product


class CollectionSerializer(serializers.ModelSerializer):
    class Meta:
        model=Collection
        fields=['id','title','product_count']
        extra_kwargs={"title":{"min_length":2}}
    product_count=serializers.IntegerField(read_only=True)  



class ProductSerializer(serializers.ModelSerializer):
    collection=CollectionSerializer
    price_with_tax=serializers.SerializerMethodField(method_name='calculating_tax')
    class Meta:
        model=Product
        fields=["id","title","description","unit_price","inventory","price_with_tax","collection"]    


    def calculating_tax(self, product: Product):
        return product.unit_price * Decimal(1.1).quantize(Decimal('.01'),rounding=ROUND_DOWN)
    
class SimpleProductSerializer(serializers.ModelSerializer):
    class Meta:
        model=Product
        fields=["id","title","unit_price","inventory"]


class CartItemSerializers(serializers.ModelSerializer):
    product=SimpleProductSerializer(read_only=True)
    total_price=serializers.SerializerMethodField()
    def get_total_price(self,cart_item:CartItem):
        return cart_item.quantity*cart_item.product.unit_price


    class Meta:
        model=CartItem        
        fields=["cart_id","product","quantity","total_price"]



class CartSerializers(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only=True)
    items = CartItemSerializers(many=True, read_only=True)
    total_price = serializers.SerializerMethodField()

    def get_total_price(self, cart):
        return sum([item.quantity * item.product.unit_price for item in cart.items.all()])

    class Meta:
        model=Cart
        fields=["id","items","total_price"]


