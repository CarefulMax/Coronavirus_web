from django.shortcuts import render
from django.http import HttpResponse
from datetime import datetime

from .models import RegionalStats


# Create your views here.
def index(request):
    context = {}
    # regions = Regions.objects.all()
    regional_stats_list = RegionalStats.objects.all()
    # print(regional_stats_list)
    regional_stats_list = list(range(80))
    context['regional_stats_list'] = regional_stats_list
    regional_stats_columns = ['region', 'new_cases', 'hospitalised', 'recovered', 'died']
    context['regional_stats_columns'] = regional_stats_columns
    actual_date = datetime.today().strftime("%d.%m %Y года")
    context['actual_date'] = actual_date
    return render(request, 'stats/index.html', context)


def parse(request):
    print("Парсинг делать хочу")
    return HttpResponse
