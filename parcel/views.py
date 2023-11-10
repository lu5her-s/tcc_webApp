from datetime import datetime
from django.shortcuts import HttpResponse, get_object_or_404, redirect, render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import (
    DetailView,
    ListView,
    TemplateView,
    View
)

from asset.models import (
    StockItem,
    Category
)
from account.models import (
    Department
)

from .models import (
    RequestBill,
    RequestBillDetail,
    RequestItem
)
from .forms import SelectStockForm, BillCreateForm
from cart.cart import Cart

# Create your views here.

class ParcelHomeView(LoginRequiredMixin, TemplateView):
    """A class-based view for the home page of the parcel application."""

    template_name = 'parcel/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        all_bill = RequestBill.objects.filter(user=self.request.user)
        context['all_bill'] = all_bill
        context['wait_approve'] = all_bill.filter(billdetail__approved=False)
        context['parcel_list'] = RequestItem.objects.filter(bill__in=all_bill)
        # context['on_hand'] = Q(all_bill.billitems.filter(item.status==StockItem.Status.AVAILABLE)) & Q(all_bill.bill_detail.filter(is_paid=True))
        # context['on_hand'] = (Q(RequestItem.objects.filter(item__status=StockItem.Status.AVAILABLE, bill__in=all_bill)) & Q(
        #     all_bill.filter(billdetail__is_paid=True)
        # )).count()
        context['on_hand'] = RequestItem.objects.filter(
            item__status=StockItem.Status.AVAILABLE,
            bill__in=all_bill,
        ).filter(bill__billdetail__is_done=True)
        return context


class BillListView(LoginRequiredMixin, ListView):
    template_name = 'parcel/bill_list.html'
    model = RequestBill

    def get_queryset(self):
        return self.model.objects.filter(user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'รายการใบเบิก'
        return context


class SelectStockView(LoginRequiredMixin, View):
    template_name = 'parcel/select_stock.html'
    form_class = SelectStockForm

    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            stock_id = form.cleaned_data['department'].id
            stock = get_object_or_404(Department, pk=stock_id)
            return redirect('parcel:select_item', pk=stock.pk)
        return render(request, self.template_name, {'form': form})


# TODO: review/edit this to create bill for store item category.
# prepare to manager set serail number of item in detail bill page
class SelecItemView(LoginRequiredMixin, View):
    template_name = 'parcel/select_item.html'

    def get(self, request, pk):
        stock = get_object_or_404(Department, pk=pk)
        items = StockItem.objects.filter(
            location=stock,
            status=StockItem.Status.AVAILABLE
        )
        categories = Category.objects.filter(stockitem__in=items).distinct()
        context = {
            'stock': stock,
            'items': items,
            'categories': categories,
        }
        return render(request, self.template_name, context)


class BillCreateView(LoginRequiredMixin, View):
    def post(self, request):
        cart = Cart(request)
        bill = RequestBill.objects.create(
            user=request.user,
            stock=request.POST.get('stock')
        )
        for item in cart:
            RequestItem.objects.create(
                bill=bill,
                category=item['category'],
                quantity=item['quantity']
            )
        RequestBillDetail.objects.create(
            bill=bill,
        )
        cart.clear()
        return redirect(reverse_lazy('parcel:bill_detail', kwargs={'pk': bill.pk}))

    def get(self, request):
        form = BillCreateForm()
        return render(request, 'parcel/bill_create.html', {'form': form})


class BillDetailView(LoginRequiredMixin, View):
    def get(self, request, pk):
        bill = get_object_or_404(RequestBill, pk=pk)
        items = RequestItem.objects.filter(bill=bill)
        bill_detail = RequestBillDetail.objects.filter(bill=bill) if bill.billdetail else RequestBillDetail.objects.create(
            bill=bill
        )
        context = {
            'bill': bill,
            'items': items,
            'bill_detail': bill_detail
        }
        return render(request, 'parcel/bill_detail.html', context)

    def post(self, request, pk):
        pass


def test_create_bill(request):
    if request.method == 'POST':
        cart = Cart(request)
        bill_id = "test/001"
        user = request.user
        created_at = datetime.now()
        department = request.user.profile.department.name
        items = []
        for item in cart:
            items.append({
                'category': item['category'].name,
                'quantity': item['quantity']
            })
        print(f"""
                        bill_id: {bill_id}
                        user: {user}
                        created_at: {created_at}
                        department: {department}
        """)
        count = 1
        for item in items:
            if int(item['quantity']) > 1:
                for _ in range(int(item['quantity'])):
                    print(f"""
                        --------------------
                        Count: {count}
                        Category: {item['category']}
                        Items Can Add : {StockItem.objects.filter(
                            category__name=item['category'],
                            status=StockItem.Status.AVAILABLE,
                            location__name__startswith="คลัง"
                            )}
                        Quantity: {item['quantity']}
                        --------------------
                      """)
                    count += 1
            else:
                print(f"""
                      --------------------
                      Count: {count}
                      Category: {item['category']}
                        Items Can Add : {StockItem.objects.filter(
                            category__name=item['category'],
                            status=StockItem.Status.AVAILABLE,
                            location__name__startswith="คลัง"
                            )}
                      Quantity: {item['quantity']}
                      --------------------
                  """)
                count += 1

        return HttpResponse(bill_id)
