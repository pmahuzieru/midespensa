from django.urls import path
from midespensa.views import ItemListView

urlpatterns = [
    path("items/", ItemListView.as_view(), name="item-list"),
]