from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import (
    ListView,
    DetailView,
)

from asset.models import (
    StockItem,
)

# Create your views here.

class StockItemListView(LoginRequiredMixin, ListView):
    """
    StockItemListView.
    Listing Stock item is available all
    """

    model = StockItem
    template_name = 'asset/stockitem_list.html'

    def get_queryset(self):
        return StockItem.available.all()

# class for detail view StockItemDetailView
class StockItemDetailView(LoginRequiredMixin, DetailView):
    """
    StockItemDetailView.
    Detail view for StockItem
    """
    model = StockItem
    template_name = 'asset/stockitem_detail.html'

    def get_queryset(self):
        qs = StockItem.available.get(pk=self.kwargs['pk'])
        return qs
