from django.shortcuts import redirect
from django.http import HttpResponse, HttpRequest
from db_updater.updater import update


# Create your views here.
def parse(request: HttpRequest):
    print(request.method)
    print('Начат процесс парсинга')
    print(request.path)
    print(request.path_info)
    update()
    return redirect('/admin/stats/lastparsed/')
