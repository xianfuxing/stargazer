import random
import numpy as np
from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def index(reqest):
    return render(reqest, 'server/index.html')


def fake_bar(reqest):
    data = random.randint(5, 100)
    return HttpResponse(data)