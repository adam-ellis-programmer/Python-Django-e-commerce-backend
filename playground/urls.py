from django.urls import path
from . import views  # from current folder
# no call to the funciton () just a reference

# URL config
urlpatterns = [
    # path('playground/hello', views.sayHello)
    path('hello/', views.sayHello)
]
 

# def name(args):
#     pass
