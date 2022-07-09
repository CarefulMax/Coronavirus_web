from django.shortcuts import render

from stats.models import Regions, RegionalStats, RegionalRestrictions
from datetime import datetime


# Create your views here.

def regions_page(request):
    context = {'region': '',
               'date': '',
               'new_cases': '',
               'hospitalised': '',
               'died': '',
               'vac1': '',
               'vac_full': '',
               'immunity': '',
               'restrictions': ''}
    inregion = request.GET.get('region', '')
    print(inregion)
    indate = request.GET.get('date', '')
    context['inregion'] = inregion
    context['indate'] = indate
    # print(f"region -'{region}', date = '{date}'")
    if inregion != '' and indate != '':
        date = datetime.strptime(indate, '%Y-%m-%d').date()
        region = Regions.objects.filter(region=inregion)
        if region.count() == 0:
            context = {'region': inregion,
                       'date': date,
                       'new_cases': 'Нет данных',
                       'hospitalised': 'Нет данных',
                       'died': 'Нет данных',
                       'vac1': 'Нет данных',
                       'vac_full': 'Нет данных',
                       'immunity': 'Нет данных',
                       'restrictions': '',
                       'inregion': region,
                       'indate': indate,
                       }
        else:
            region = region[0]
            stats = RegionalStats.objects.filter(date=date, region=region)
            if stats.count() == 0:
                context = {'region': inregion,
                           'date': date,
                           'new_cases': 'Нет данных',
                           'hospitalised': 'Нет данных',
                           'died': 'Нет данных',
                           'vac1': 'Нет данных',
                           'vac_full': 'Нет данных',
                           'immunity': 'Нет данных',
                           'restrictions': '',
                           'inregion': region,
                           'indate': indate,
                           }
            else:
                stats = stats[0]
                context['region'] = region
                context['date'] = date
                context['new_cases'] = stats.new_cases
                context['hospitalised'] = stats.hospitalised
                context['died'] = stats.died
                context['vac1'] = stats.vaccinated_first_component_cumulative
                context['vac_full'] = stats.vaccinated_fully_cumulative
                context['immunity'] = stats.collective_immunity
                restrictions = RegionalRestrictions.objects.filter(date=date, region=region)
                restrictions = list(set([restr.restriction.description for restr in restrictions]))
                context['restrictions'] = restrictions
                print(restrictions)
    return render(request, 'regions/regions_page.html', context)
