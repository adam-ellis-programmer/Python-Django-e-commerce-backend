# F = field and.. a query expression, code that produces a value
from django.db.models import Q, F, Value, Func, ExpressionWrapper, DecimalField
from django.shortcuts import render

from django.db.models.aggregates import Count, Max, Min, Avg, Sum
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse
from django.db.models.functions import Concat
from store.models import Product, OrderItem, Order, Customer
# Create your views here.
# like an aciton in mern

"""
query_set like firebase
get returns an object not a query set

"""


def sayHello(req):
    # each order can have many items
    # query_set = Order.objects.select_related(
    #     # __products referenced in the order items
    #     'customer').prefetch_related('orderitem_set__product').order_by('-placed_at')[:5]

    #   aggeregating data
    # result = Product.objects.filter(collection__id=1).aggregate(
    #     hello=Count('id'), min_price=Min('unit_price'))

    # Annotation Object
    # value is dirivitive of the Value class
    # querySet = Customer.objects.annotate(is_new=Value(True))
    # querySet = Customer.objects.annotate(new_id=F('id')+1)
    # querySet = Customer.objects.annotate(
    #     # CONCAT
    #     full_name=Func(F('first_name'), Value(
    #         ' '), F('last_name'), function='CONCAT')
    # )
    # querySet = Customer.objects.annotate(
    #     # CONCAT -- use value oterwise django thinks it is a column in the table
    #     full_name=Concat('first_name', Value(' '), 'last_name')
    # )
    # CREATES A LEFT JOIN
    # querySet = Customer.objects.annotate(
    #     orders_count=Count('order')
    # )

    # discounted_price = ExpressionWrapper(
    #     F('unit_price') * 0.8, output_field=DecimalField()

    #     query_set=Product.objects.annotate(
    #         discounted_price=dis
    #     )
    # )

    # querySet = Customer.objects.annotate(
    #      ExpressionWrapper(F('unit_price') * 0.8, output_field=DecimalField)
    #     discounted_price=
    # )

    return render(req, 'hello.html', {'name': 'Adam', 'result': list(querySet)})
