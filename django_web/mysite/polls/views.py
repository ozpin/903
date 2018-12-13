from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse


def index(request):
    return HttpResponse("お帰りなさいませ、ご主人様！ You're at the polls index.")