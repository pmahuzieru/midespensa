from django.views.generic import ListView
from django.shortcuts import render
from midespensa.models import Item

# Create your views here.
class ItemListView(ListView):
    model = Item
    template_name = "items/item_list.html"
    context_object_name = "items"
    
    def get_queryset(self):
        status = self.request.GET.get("status")
        
        if status:
            return Item.objects.filter(purchase_status=status).all()
        return Item.objects.all()
            