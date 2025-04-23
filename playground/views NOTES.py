# F = field and.. a query expression, code that produces a value
from django.db.models import Q, F
from django.shortcuts import render
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse
from store.models import Product, OrderItem
# Create your views here.
# like an aciton in mern

"""
query_set like firebase
get returns an object not a query set

"""


def sayHello(req):
    # query_set = Product.objects.all()

    # product = Product.objects.filter(pk=1).first() # returns none so we do not get an exeption
    # returns none so we do not get an exeption
    # exists = Product.objects.filter(pk=1).exists()  # returns a boolean
    # query_set = Product.objects.filter( unit_price__range=(20, 30))  # returns a boolean
    # query_set = Product.objects.filter(
    #     collection__id__range=(1, 2, 3))  # filter across relationships
    # cas insensitive
    # query_set = Product.objects.filter(title__icontains='coffee')
    # query_set = Product.objects.filter(title__istartswith='coffee')
    # query_set = Product.objects.filter(last_update__year=2021)
    # query_set = Product.objects.filter(last_update__month=2021)
    # query_set = Product.objects.filter(last_update__day=2021)
    # query_set = Product.objects.filter(last_update__date=2021)
    # query_set = Product.objects.filter(description__isnull=True)
    # query_set = Product.objects.filter(
    #     inventory__lt=10).filter(unit_price__gt=45)
    # query_set = Product.objects.filter(
    #     Q(inventory__lt=10) | Q(unit_price__gt=20))
    # query_set = Product.objects.filter(
    #     Q(inventory__lt=10) & Q(unit_price__gt=80))
    # unit price is NOT less than 80
    # query_set = Product.objects.filter(
    #     Q(inventory__lt=10) & ~Q(unit_price__gt=80))
    # finds products that = unit price
    # query_set = Product.objects.filter(inventory=F('unit_price'))
    # ref field in a related table
    # query_set = Product.objects.filter(inventory=F('collection__id'))

    # query_set = Product.objects.order_by('title')
    # unit price in asc and title by desc -- if same price we sort title desc order
    # query_set = Product.objects.order_by('unit_price', '-title')
    # unit price in desc and titel in asc as -
    # query_set = Product.objects.order_by('unit_price', '-title').reverse()
    # query_set = Product.objects.filter(collection__id=1).order_by('unit_price')
    # product = Product.objects.order_by('unit_price')[0]
    # product = Product.objects.earliest('unit_price')
    # product = Product.objects.latest('unit_price')

    # first page 0,1,2,3,4
    # query_set = Product.objects.all()[:5]
    # second page 5,6,7,8,9 --- off set clause
    # query_set = Product.objects.all()[5:10]

    # we can read related fields -- performs an inner join
    # -- this gives us dicitonary objects rather than a bunch of instances s
    # query_set = Product.objects.values('id', 'title', 'collection__title')

    # returns tuples not dicitonaries
    # query_set = Product.objects.values_list('id', 'title', 'collection__title')

    # query for Products that have been ordered
    # using in lookup type to find all products whos id is a givenlist
    # This Django query is selecting products that have been ordered at least once. Let's break it down:
    # In plain English, this query is finding "all products that have appeared in at least one order."

    # so it gathers all the ids from the products and checks to see if any of those IDs are in are in the order items table at least once the field it checks int the orderItem table is product_d it checks for distinct values
    # query_set = Product.objects.filter(
    #     id__in=OrderItem.objects.values('product_id').distinct()).order_by('title')

    # SELECT * FROM products
    # WHERE id IN (
    # SELECT DISTINCT product_id
    # FROM order_items
    # )

    # product_id as django creats this at runtime -- distinct = remove duplicates
    # query_set = OrderItem.objects.values('product_id').distinct()

    # here we get instances of the values
    # where as with values we get dictionary objects

    # this causes database to take a long time
    # query_set = Product.objects.only('id', 'title')

    # meaning we are interesetd in all fields other than the description
    # so we defer this until later
    # if we are not rendering the description we can use
    # the defer to defer the data read
    # Lazy Loading: The deferred fields are only fetched from the database when you specifically access them.
    # query_set = Product.objects.defer('description')

    # select the field we want to pre load
    # quicker as we create A JOIN between the tables
    # span relationships
    # select reateatd other end has 1 instance (collection)
    # pre fetch related (n) = many - like promitions of our product
    # tries to read two databases 2 x 1000
    # only queries the product table nto the related table  so we use select related
    # uses the inner join
    # span relationships using __someOtherField
    # select related (1) = other end of the relationship has one instnace
    # prefetch related (many) =promotions
    # query_set = Product.objects.select_related('collection').all()
    # one procuct has MANY promotions
    query_set = Product.objects.prefetch_related('promotions').select_related('collection').all()
    # query_set = Product.objects.prefetch_related('promotions').select_related('collection').all()

    # methods return a query set so we can chain to build complex query

    # l = list(query_set)
    # product = Product.objects.get(pk=0)
    # list = query_set.filter().filter().order_by()
    # list = query_set.filter(title='Bread Ww Cluster')

    # for p in list:
    # print(p)

    # query_set[0:5]
    # for product in query_set:
    #     print(product)
    # return HttpResponse('Hello world')
    return render(req, 'hello.html', {'name': 'Adam', 'products': list(query_set)})
    # return render(req, 'hello.html', {'name': 'Adam', 'product': product})
