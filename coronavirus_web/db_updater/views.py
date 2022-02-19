from django.shortcuts import render
import logging
from stats.models import Regions, RegionalStats, LastParsed


# Create your views here.
def parse(request):
    logging.debug('Сейчас парсить буду')
