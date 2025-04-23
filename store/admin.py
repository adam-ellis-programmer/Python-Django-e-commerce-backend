from django.contrib import admin, messages
from django.http import HttpRequest
from . import models  # curr folder
from django.db.models import Count
from django.urls import reverse
from django.utils.html import format_html, urlencode

# Register your models here.

# convention modelAdmin


class InventoryFilter(admin.SimpleListFilter):
    title = 'inventory'
    parameter_name = 'inventory'  # used in the query string

    def lookups(self, request, model_admin):
        return [
            ('<10', 'Low'),
            ('>=10', 'OK')
        ]

    # In self.value(), the .value() method returns the currently selected filter value from the URL's query parameters.
    def queryset(self, request, queryset):
        if self.value() == '<10':
            return queryset.filter(inventory__lt=10)
        elif self.value() == '>=10':
            return queryset.filter(inventory__gte=10)


@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
    # form
    #  autocomplete_fields limits search fields to 10 then we have to search for them
    autocomplete_fields = ['collection']
    prepopulated_fields = {
        'slug': ['title']  # add multiple fields
    }
    # fields = []
    # exclude = []
    # readonly_fields = []
    actions = ['clear_inventory']  # pass the name of the method as a string
    # declarative programming is how we call inventory_status
    # because collection is a related field django shows a string represintation
    # it calls the __str__() but we overode it
    list_display = ['title', 'unit_price',
                    'inventory_status', 'collection_title']
    list_editable = ['unit_price']
    list_filter = ['collection', 'last_update', InventoryFilter]
    list_per_page = 10

    # Select_related for eager loading / pre loading the RELATED fields

    list_select_related = ['collection']

    def collection_title(self, product):
        return product.collection.title

    @admin.display(ordering='inventory')
    def inventory_status(self, product):
        if product.inventory < 10:
            return 'low '
        return 'OK!'

    # self - Reference to the ProductAdmin instance
    # request - The HTTP request object containing user session info
    # queryset contians the objects the user has selected

    @admin.action(description='Clear Inventory')
    def clear_inventory(self, request, queryset):
        updated_count = queryset.update(inventory=0)
        self.message_user(
            request,
            f'{updated_count} products were successfully updated',
            messages.INFO
        )


@admin.register(models.Customer)
class CustomerAdmin(admin.ModelAdmin):
    # autocomplete_fields = ['collection']
    list_display = ['first_name', 'last_name', 'membership']
    list_editable = ['membership']
    list_per_page = 10
    ordering = ['first_name', 'last_name']
    search_fields = ['first_name__istartswith', 'last_name__istartswith']


@admin.register(models.Collection)
class CollectionAdmin(admin.ModelAdmin):
    list_display = ['title', 'products_count']
    # limits search fields to 10 then we have to search for them
    # added so we can use   autocomplete_fields = ['collection']
    search_fields = ['title']
    # add @admin... for sorting - ordering to name of field to be used for sorting

    @admin.display(ordering='products_count')
    def products_count(self, collection):
        # reverse('admin:app_model_page')
        # {} = place_holders
        url = (
            reverse('admin:store_product_changelist')
            + '?'
            + urlencode({
                'collection__id': str(collection.id)
            }))
        return format_html('<a href="{}">{}</a>', url, collection.products_count)

    # overide an annotate
    # every model admin has get_queryset which we can over write
    # we are overiding the query set on the page here and annotate the colleciton with the number of products
    # annotate is createing a temporary field and calculating at the database level with Count --
    # more efficient way rather than Python calculating at run time

    # called for each collection in the list view
    # This overrides the default queryset to add the annotation. It creates a temporary attribute called products_count on each Collection object containing the count of related products.

    def get_queryset(self, request: HttpRequest):
        return super().get_queryset(request).annotate(
            products_count=Count('product')
        )

    # use decorator instead
    # admin.site.register(models.Product, ProductAdmin)


@admin.register(models.Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'placed_at', 'customer']


"""
A QuerySet in Django is a collection of database objects retrieved from your database. It's one of the most fundamental concepts in Django's ORM (Object-Relational Mapper).
Key characteristics of a QuerySet:

Database Abstraction: QuerySets let you interact with your database using Python code instead of raw SQL.
Lazy Evaluation: QuerySets are lazy - they don't hit the database until you actually need the data (when you iterate over them, slice them, or convert them to lists, etc.).
Chainable Operations: You can chain methods like .filter(), .exclude(), .order_by(), and .annotate() to refine your queries.
Query Builder: Each method you call on a QuerySet returns a new QuerySet without executing the query, allowing you to build complex queries step by step.
Represents DB Rows: Each object in a QuerySet represents a row in your database table.

Examples of QuerySets:
python# Basic queryset - all Product objects
Product.objects.all()

# Filtered queryset - Products with price > 100
Product.objects.filter(price__gt=100)

# Annotated queryset - Categories with product count
Category.objects.annotate(product_count=Count('product'))
In your admin example, overriding get_queryset lets you customize exactly what data is retrieved and how it's enhanced (with annotations) before being displayed in the admin interface.RetryClaude can make mistakes. Please double-check responses. 
"""
