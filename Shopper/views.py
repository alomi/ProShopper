from django.shortcuts import render
from Shopper.models import Product

# Create your views here.
def index(request):
    # Render the HTML template index.html with the data in the context variable

    alla = Product.objects.all()
    for i in alla:
        print(i.get_title())
    return render(
        request,
        'index.html',
    )



