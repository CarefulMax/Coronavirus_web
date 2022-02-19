from django.shortcuts import render


# Create your views here.
def create_report_page(request):
    context = {}
    return render(request, 'reports/create_report_page.html', context)
