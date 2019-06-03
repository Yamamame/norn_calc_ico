from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.


def index(request):
    str_out = "Good Afternoon<p />"
    str_out += "こんにちは<p />"
    return HttpResponse(str_out)
