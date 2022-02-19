from django.shortcuts import redirect


# Create your views here.
def index_to_stats_redirect(request):
    response = redirect('/stats/')
    return response
