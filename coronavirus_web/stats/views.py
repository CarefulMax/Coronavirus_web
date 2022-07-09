from django.shortcuts import render, redirect
import json
from django.http import HttpResponse
import os
from datetime import datetime

from .models import RegionalStats, LastParsed


# Create your views here.
def index(request):
    context = {}
    latest_date = LastParsed.objects.get().parsed_info_datetime
    regional_stats_list = RegionalStats.objects.filter(date=latest_date).order_by('-new_cases')
    # print(regions)
    # print(regional_stats_list)
    # regional_stats_list = list(range(80))
    context['regional_stats_list'] = regional_stats_list
    regional_stats_columns = ['region', 'new_cases', 'hospitalised', 'recovered', 'died']
    context['regional_stats_columns'] = regional_stats_columns
    context['actual_date'] = latest_date

    return render(request, 'stats/index.html', context)


def download_current(request):
    print('Скачивание')
    # print(os.getcwd())
    latest_date = LastParsed.objects.get().parsed_info_datetime
    # print(latest_date)
    # print(type(latest_date))
    regional_stats_list = RegionalStats.objects.filter(date=latest_date)
    result = {'stats': []}
    filepath = f'static/files/jsons/current_{latest_date}.json'
    for regional_stats in regional_stats_list:
        result['stats'].append({
            'date': str(regional_stats.date),
            'region': regional_stats.region.region,
            'new_cases': regional_stats.new_cases,
            'hospitalised': regional_stats.hospitalised,
            'recovered': regional_stats.recovered,
            'died': regional_stats.died,
            'vaccinated_first_component_cumulative': regional_stats.vaccinated_first_component_cumulative,
            'vaccinated_fully_cumulative': regional_stats.vaccinated_fully_cumulative,
            'collective_immunity': float(regional_stats.collective_immunity),
        })
    # print(result)
    if not os.path.isfile(filepath):
        with open(filepath, 'w') as file:
            json.dump(result, file, indent=2, ensure_ascii=False)
    with open(filepath, 'rb') as file:
        response = HttpResponse(file.read())
        response['Content-Disposition'] = "attachment; filename=%s" % filepath
        return response
