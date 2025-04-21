from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.
# like an aciton in mern


def calculate():
    x = 1
    y = 2
    return x
 

def sayHello(req):
    x = calculate()

    # return HttpResponse('Hello world')
    return render(req, 'hello.html', {'name': 'Adam'})
 