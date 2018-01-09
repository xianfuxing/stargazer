import random
import numpy as np
from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import ListView, DeleteView
from pure_pagination.mixins import PaginationMixin

from .models import Host


def index(request):
    return render(request, 'server/index.html')


class ServerListView(PaginationMixin, ListView):
    model = Host
    context_object_name = 'hosts'
    template_name = 'server/host_list.html'

    paginate_by = 5
    object = Host

    def get_context_data(self, *, object_list=None, **kwargs):
        ctx = super().get_context_data(object_list=None, **kwargs)
        host_count = Host.objects.all().count()
        ctx['host_count'] = host_count

        return ctx


def fake_bar(request):
    data = random.randint(5, 100)
    return HttpResponse(data)