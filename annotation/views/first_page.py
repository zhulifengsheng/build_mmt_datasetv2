from django.shortcuts import render

from annotation.models import Caption

def first_page(request):
    Caption.objects

    return render(request, 'first_page.html')