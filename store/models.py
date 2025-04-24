from django.core.validators import MinValueValidator
from django.db import models
# Create your models here.
# https://docs.djangoproject.com/en/5.2/ref/models/fields/#field-types


# SKU = Stock Keeping Unit
# sku = models.CharField(max_length=10, primary_key=True)

# django creates the reverse relationship automatically
# we show the product to the user - we want to
# also show all the promotions that apply to that product
# therefor we create the relationship in the Product model
# as a ManyToMany
class Promotion(models.Model):
    description = models.CharField(max_length=255)
    discount = models.FloatField()
    # start_date
    # end_date


# defined before the product class so we can referece it


# circular dependencey
# By using related_name='+', you're telling Django:
# don't need to access all collections where this product is featured from the product side
# trys to create the reverse  collection_set nut we allready have
#  collection_set with collections
class Collection(models.Model):
    title = models.CharField(max_length=255)
    featured_product = models.ForeignKey(
        'Product', on_delete=models.SET_NULL, null=True,
        related_name='+'
    )
    # overide the string representation of an object
    # every object has this magic method
    # this __str__ method is called when we convert it to a string
    #
    # -> is type annotarion retuns a ...

    def __str__(self) -> str:
        # return super().__str__()
        return self.title

    # define a meta class for default ordering
    class Meta:
        ordering = ['title']


class Product(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField()
    # blank for admin interface
    description = models.TextField(null=True, blank=True)
    unit_price = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        validators=[MinValueValidator(1)]
    )
    inventory = models.IntegerField()
    last_update = models.DateTimeField(auto_now=True)
    # takes the id of the collection associated with * we do not delete this if we delete a collection
    collection = models.ForeignKey(Collection, on_delete=models.PROTECT)
    # target model is Promition -- django creates reverse in promotion class
    # promotions = models.ManyToManyField(Promotion, related_name='products')
    promotions = models.ManyToManyField(Promotion, blank=True)

    #  OVERIDING THE STRING REPRESENTATION OF THE PRODUCT MODEL
    def __str__(self) -> str:
        return self.title

    class Meta:
        ordering = ['title']


class Customer(models.Model):
    MEMBERSHIP_BRONZE = 'B'
    MEMBERSHIP_SILVER = 'B'
    MEMBERSHIP_GOLD = 'B'

    MEMBERSHIP_CHOICES = [
        (MEMBERSHIP_BRONZE, "Bronze"),
        (MEMBERSHIP_SILVER, "Silver"),
        (MEMBERSHIP_GOLD, "Gold"),
    ]

    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=255)
    birth_date = models.DateField(null=True)
    membership = models.CharField(
        max_length=1, choices=MEMBERSHIP_CHOICES, default=MEMBERSHIP_BRONZE)

    def __str__(self) -> str:
        return f'{self.first_name}  {self.last_name}'

    # https://docs.djangoproject.com/en/5.2/ref/models/options/#indexes
    class Meta():
        db_table = "store_customer"  # use singular names not plural
        indexes = [
            # index set on these fields
            models.Index(fields=["last_name", "first_name"]),
        ]
        # ordering = ['last_name', 'first_name']
        ordering = ['first_name', 'last_name']


class Order(models.Model):
    PAYMENT_STATUS_PENDING = 'P'
    PAYMENT_STATUS_COMPLETE = 'C'
    PAYMENT_STATUS_FAILED = 'F'

    PAYMENT_STATUS_CHOICES = [
        (PAYMENT_STATUS_PENDING, "Pending"),
        (PAYMENT_STATUS_COMPLETE, "complete"),
        (PAYMENT_STATUS_FAILED, "Failed"),
    ]

    # placed_at = models.DateTimeField(auto_now=True)
    placed_at = models.DateTimeField()  # now displays in the form
    payment_status = models.CharField(
        max_length=1,
        choices=PAYMENT_STATUS_CHOICES,
        default=PAYMENT_STATUS_PENDING
    )
    # ONE customer can have many orders
    customer = models.ForeignKey(Customer, on_delete=models.PROTECT)


class OrderItem(models.Model):
    # orderitem_set
    # order = models.ForeignKey(Order, on_delete=models.PROTECT, related_name='items')
    order = models.ForeignKey(Order, on_delete=models.PROTECT)
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    quantity = models.PositiveSmallIntegerField()
    # always store the price at the time it was ordered
    unit_price = models.DecimalField(max_digits=6, decimal_places=2)


# each address belongs to one cusotmer
# each customer has one address
# 1 - 1
# when customer gets deleted, address goes too
# .PROTECT = child must be deleted first


class Address(models.Model):
    street = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    customer = models.ForeignKey(
        Customer, on_delete=models.CASCADE,
    )


class Cart(models.Model):
    created_at = models.DateField(auto_now_add=True)


# if the cart gets deleted then the items go too
# if product deleted then it goes from every single cart
class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveSmallIntegerField()
