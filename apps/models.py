
from django.db.models import Model, CharField, ImageField, DecimalField, ForeignKey, SmallIntegerField, CASCADE, \
    DateTimeField


# Create your models here.
class Category(Model):
    class Meta:
        verbose_name_plural = "Categories"
        db_table = "category"
    name = CharField(max_length=100)

    def __str__(self):
        return self.name

class Product(Model):
    name = CharField(max_length=100)
    price = DecimalField(max_digits=10, decimal_places=2)
    quantity = SmallIntegerField(default=0)
    category = ForeignKey('apps.Category', CASCADE, related_name='products')
    created_at = DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class ProductImage(Model):
    product = ForeignKey('apps.Product', CASCADE, related_name='images')
    image = ImageField(upload_to='products/')