# F = field and.. a query expression, code that produces a value
from django.db.models import Q, F, Value, Func, ExpressionWrapper, DecimalField
# query by generic content type
from django.contrib.contenttypes.models import ContentType
from django.shortcuts import render

from django.db import transaction

from django.db.models.aggregates import Count, Max, Min, Avg, Sum
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse
from django.db.models.functions import Concat
from store.models import Product, OrderItem, Order, Customer, Collection
from tags.models import TaggedItem
# Create your views here.
# like an aciton in mern

from django.db import connection

"""
query_set like firebase
get returns an object not a query set

"""


# @transaction.atomic()
def sayHello(req):

    # with connection.cursor() as cursor:
    #     cursor.execute()

    # # context manager
    # with transaction.atomic():
    #     collection = Collection()
    #     collection.title = 'Video Games'
    #     collection.feat = Product(pk=1)

    return render(req, 'hello.html', {'name': 'Adam'})
