from django.contrib import admin
from midespensa.models import Item, Category, InventoryLog

admin.site.register(Item)
admin.site.register(Category)
admin.site.register(InventoryLog)
