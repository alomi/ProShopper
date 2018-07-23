from django.shortcuts import render
from Scraper import scraper as sc


# Create your views here.
def index(request):
    # Render the HTML template index.html with the data in the context variable
    sc.scrape()

    return render(
        request,
        'index.html',
    )



