from .models import Category

def menu_links(request):   
    return {"categories": Category.objects.all()}
    #or
    #links= Category.objects.all()
    #return dict(links=links)
    
