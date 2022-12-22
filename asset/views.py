from django.shortcuts import get_list_or_404, get_object_or_404, redirect, render, reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import (
    CreateView,
    ListView,
    DetailView,
    TemplateView,
)
from asset.forms import StockItemForm

from asset.models import (
    Category,
    Manufacturer,
    Network,
    StockItem,
    StockItemImage,
)

# Create your views here.


class StockItemListView(LoginRequiredMixin, ListView):
    """
    StockItemListView.
    Listing Stock item all
    """

    model = StockItem
    template_name = 'asset/stockitem_list.html'

    def get_queryset(self):
        return StockItem.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'แสดงรายการทรัพย์สิน'
        return context


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


class AssetHomeView(LoginRequiredMixin, TemplateView):
    template_name = 'asset/stockitem_home.html'

    def get_context_data(self, **kwargs):
        # return categories from Category model
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['stockitems'] = StockItem.available.all()
        return context


class StockItemCreateView(LoginRequiredMixin, CreateView):
    model = StockItem
    form_class = StockItemForm
    template_name = 'asset/stockitem_form.html'

    def get_success_url(self):
        # return detail of stock item
        return reverse('asset:stockitem_detail', kwargs={'pk': self.object.pk})

    def get_context_data(self):
        context = super().get_context_data()
        context['title'] = self.request.user.profile.department.name
        return context

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, request.FILES)
        if form.is_valid():
            images = request.FILES.getlist('images')
            # save images to StockItemImage
            stockitem = form.save(commit=False)
            stockitem.save()
            for image in images:
                StockItemImage.objects.create(stock_item=stockitem, images=image)
            return redirect(self.get_success_url())
        else:
            return self.render_to_response(self.get_context_data())


class StockAssetListView(LoginRequiredMixin, ListView):
    model = StockItem
    template_name = 'asset/stockitem_list.html'

    def get_queryset(self):
        # return stock item filter by department = user profile department
        return StockItem.objects.filter(department=self.request.user.profile.department)


# TODO: make list separate from stock asset name from user profile department
def categories_list(request, pk):
    """categories_list.

    :param request:
    :param pk: for get category
    """
    # items = StockItem.objects.filter(category__pk=pk)
    items = get_list_or_404(StockItem, category__pk=pk)
    context = {
        'object_list': items,
        'h_title': Category.objects.get(pk=pk).name
    }
    return render(request, 'asset/condition_list.html', context)


def manufacturer_list(request, pk):
    """manufacturer_list.

    :param request:
    :param pk:
    """
    items = get_list_or_404(StockItem, manufacturer__pk=pk)
    context = {
        'object_list': items,
        'h_title': Manufacturer.objects.get(pk=pk).name
    }
    return render(request, 'asset/condition_list.html', context)


def network_list(request, pk):
    """network_list.

    :param request:
    :param pk:
    """
    items = get_list_or_404(StockItem, network__pk=pk)
    context = {
        'object_list': items,
        'h_title': Network.objects.get(pk=pk).name
    }
    return render(request, 'asset/condition_list.html', context)
