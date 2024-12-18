from django.contrib import admin
from midespensa.models import Item, Category, InventoryLog

admin.site.register(Category)
admin.site.register(InventoryLog)

@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ['name', 'purchase_status']
