import os
from django.template.loader import render_to_string
from django.db.models import Q
from django.shortcuts import HttpResponse, get_object_or_404, redirect, render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import (
    ListView,
    TemplateView,
    View
)

from asset.models import (
    StockItem,
    Category
)
from account.models import (
    Department,
    Profile
)

from .models import (
    RejectBillNote,
    RequestBill,
    RequestBillDetail,
    RequestItem
)
from .forms import RequestBillDetailForm, SelectStockForm
from cart.cart import Cart
from config.utils import generate_pdf

# Create your views here.

class ParcelHomeView(LoginRequiredMixin, TemplateView):
    """A class-based view for the home page of the parcel application."""

    template_name = 'parcel/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        all_bill = RequestBill.objects.all()
        context['all_bill'] = all_bill.filter(user=self.request.user)
        context['wait_approve'] = all_bill.filter(billdetail__approve_status=RequestBillDetail.ApproveStatus.WAIT)
        context['parcel_list'] = RequestItem.objects.filter(
            bill__in=all_bill,
            item__status=StockItem.Status.ON_HAND
        )

        # TODO: command context
        # for command views

        # for manager views
        context['stock_bills'] = all_bill.filter(
            stock=self.request.user.profile.department,
            status=RequestBill.BillStatus.REQUEST
        )
        context['stock_bills_wait'] = all_bill.filter(
            stock=self.request.user.profile.department,
            status=RequestBill.BillStatus.IN_PROGRESS,
            billdetail__approve_status=RequestBillDetail.ApproveStatus.WAIT
        )
        context['wait_paid'] = all_bill.filter(
            stock=self.request.user.profile.department,
            status=RequestBill.BillStatus.IN_PROGRESS,
            billdetail__approve_status=RequestBillDetail.ApproveStatus.APPROVED,
            is_done=False
        )
        context['all_stock_bills'] = all_bill.filter(
            Q(stock=self.request.user.profile.department) & ~Q(status=RequestBill.BillStatus.DRAFT),
        )

        # context['on_hand'] = Q(all_bill.billitems.filter(item.status==StockItem.Status.AVAILABLE)) & Q(all_bill.bill_detail.filter(is_paid=True))
        # context['on_hand'] = (Q(RequestItem.objects.filter(item__status=StockItem.Status.AVAILABLE, bill__in=all_bill)) & Q(
        #     all_bill.filter(billdetail__is_paid=True)
        # )).count()
        context['on_hand'] = RequestItem.objects.filter(
            item__status=StockItem.Status.AVAILABLE,
            bill__in=all_bill,
        ).filter(bill__is_done=True)
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


class BillManagerListView(LoginRequiredMixin, ListView):
    template_name = 'parcel/bill_list.html'
    model = RequestBill

    def queryset(self):
        return self.model.objects.filter(
            stock=self.request.user.profile.department,
            status=RequestBill.BillStatus.REQUEST
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'รายการใบเบิกรอตรวจสอบ'
        return context


class BillWaitApproveListView(LoginRequiredMixin, ListView):
    template_name = 'parcel/bill_list.html'
    model = RequestBill

    def get_queryset(self):
        return self.model.objects.filter(
            stock=self.request.user.profile.department,
            status=RequestBill.BillStatus.IN_PROGRESS,
            billdetail__approve_status=RequestBillDetail.ApproveStatus.WAIT
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'รายการใบเบิกรออนุมัติ'
        return context


class BillWaitPaidListView(LoginRequiredMixin, ListView):
    template_name = 'parcel/bill_list.html'
    model = RequestBill

    def get_queryset(self):
        return self.model.objects.filter(
            stock=self.request.user.profile.department,
            status=RequestBill.BillStatus.IN_PROGRESS,
            billdetail__approve_status=RequestBillDetail.ApproveStatus.APPROVED,
            is_done=False
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'รายการใบเบิกรอจ่าย'
        return context


class ManagerAllBillListView(LoginRequiredMixin, ListView):
    template_name = 'parcel/bill_list.html'
    model = RequestBill

    def get_queryset(self):
        return self.model.objects.filter(
            Q(stock=self.request.user.profile.department) & ~Q(status=RequestBill.BillStatus.DRAFT),
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'รายการใบเบิกทั้งหมด'
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

    # def get(self, request):
    #     form = BillCreateForm()
    #     return render(request, 'parcel/bill_create.html', {'form': form})


class BillDetailView(LoginRequiredMixin, View):
    def get(self, request, pk):
        bill = get_object_or_404(RequestBill, pk=pk)
        recievers = Profile.objects.exclude(user=bill.user)
        items = RequestItem.objects.filter(bill=bill)
        bill_detail, _ = RequestBillDetail.objects.get_or_create(bill=bill)
        context = {
            'bill': bill,
            'items': items,
            'bill_detail': bill_detail,
            'recievers': recievers,
            'bill_detail_form': RequestBillDetailForm(instance=bill_detail),
        }
        return render(request, 'parcel/bill_detail2.html', context)

    # # TODO: get item from serail or pk and set item status to HOLD
    # def post(self, request, pk):
    #     bill = get_object_or_404(RequestBill, pk=pk)
    #     data = request.POST
    #     print(data)
    #     serials = data.getlist('serial_no')
    #     for serial in serials:
    #         try:
    #             item = StockItem.objects.get(serial=serial)
    #             print(item)
    #         except ObjectDoesNotExist:
    #             print("item not found")
    #             continue
    #     return redirect(reverse_lazy('parcel:bill_detail', kwargs={'pk': bill.pk}))


# def set_serail_item(request, pk):
#     bill = get_object_or_404(RequestBill, pk=pk)
#     items = RequestItem.objects.filter(bill=bill)
#     if request.method == 'POST':
#         for item in items:
#             item.serial_no = request.POST.get('serail_no')
#             item.save()
#         return redirect(reverse_lazy('parcel:bill_detail', kwargs={'pk': bill.pk}))


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


def paid_item(request, pk):
    bill = get_object_or_404(RequestBill, pk=pk)
    bill.billdetail.paid = True
    bill.billdetail.save()
    return redirect(reverse_lazy('parcel:bill_detail', kwargs={'pk': pk}))


def recieve_items(request, pk):
    bill = get_object_or_404(RequestBill, pk=pk)
    items = RequestItem.objects.filter(bill=bill)

    print(items)
    return redirect(reverse_lazy('parcel:bill_detail', kwargs={'pk': pk}))
    # for item in items:
    #     item.mark_as_received()
    #     item.status = StockItem.Status.ON_HAND
    #     item.save()
    # bill.mark_as_recieved()
    # bill.save()
    # bill.billdetail.received_at = datetime.date.today()
    # bill.billdetail.save()
    # return redirect(reverse_lazy('parcel:bill_detail', kwargs={'pk': pk}))


def parcel_list(request):
    items = RequestItem.objects.filter(
        bill__user=request.user,
    ).select_related('bill__user')
    context = {
        'object_list': items,
        'title': 'Parcel List'
    }
    return render(request, 'parcel/parcel_list.html', context)


# TODO: refactor and make set item to form submit all in form save all[template]
def set_serial_item(request, pk):
    bill = get_object_or_404(RequestBill, pk=pk)
    items = RequestItem.objects.filter(bill=bill)
    if request.method == 'POST':
        serials_no = request.POST.getlist('serial_no')
        stock_items = StockItem.objects.filter(serial__in=serials_no)
        item_serial_mapping = {item: serial_no for item, serial_no in zip(items, serials_no)}
        stock_item_mapping = {stock_item.serial: stock_item for stock_item in stock_items}
        for item, serial_no in item_serial_mapping.items():
            stock_item = stock_item_mapping.get(serial_no)
            if stock_item:
                item.item = stock_item
                item.serial_no = serial_no
                item.save()
        return redirect(reverse_lazy('parcel:bill_detail', kwargs={'pk': bill.pk}))
    return HttpResponse("Error")


def request_approve(request, pk):
    bill = get_object_or_404(RequestBill, pk=pk)
    bill.status = RequestBill.BillStatus.IN_PROGRESS
    bill.billdetail.approve_status = RequestBillDetail.ApproveStatus.WAIT
    bill.save()
    return redirect(reverse_lazy('parcel:bill_detail', kwargs={'pk': pk}))


def approve_bill(request, pk):
    bill = get_object_or_404(RequestBill, pk=pk)
    bill.billdetail.approve_status = RequestBillDetail.ApproveStatus.APPROVED
    bill.save()
    return redirect(reverse_lazy('parcel:bill_detail', kwargs={'pk': pk}))


def bill_to_pdf(request: HttpResponse, pk: int):
    bill = RequestBill.objects.get(pk=pk)
    items = RequestItem.objects.filter(bill=bill)
    bill_detail = RequestBillDetail.objects.get(bill=bill)
    # bill_detail = bill.billdetail
    context = {
        'bill': bill,
        'items': items,
        'bill_detail': bill_detail
    }
    temp_html = 'parcel/temp.html'
    with open(temp_html, 'w') as f:
        f.write(render_to_string('parcel/bill_pdf.html', {'context': context}))
    pdf = generate_pdf(data={'context': context}, template_path='parcel/bill_pdf.html')
    os.remove(temp_html)

    response = HttpResponse(pdf, content_type='application/pdf')

    return response


def save_draft(request, pk):
    bill = get_object_or_404(RequestBill, pk=pk)
    data = request.POST
    bill_detail = RequestBillDetail.objects.get(bill=bill)
    bill_detail.request_case = data.get('request_case')
    bill_detail.item_type = data.get('item_type')
    bill_detail.item_control = data.get('item_control')
    bill_detail.money_type = data.get('money_type')
    bill_detail.job_no = data.get('job_no')
    bill_detail.request_reference = data.get('request_reference')
    if data.get('receiver'):
        bill_detail.receiver = get_object_or_404(Profile, pk=data.get('receiver'))
    else:
        bill_detail.receiver = None
    bill_detail.save()
    return redirect(reverse_lazy('parcel:bill_detail', kwargs={'pk': pk}))


def request_bill(request, pk):
    RequestBill.objects.filter(pk=pk).update(status=RequestBill.BillStatus.REQUEST)
    return redirect(reverse_lazy('parcel:bill_detail', kwargs={'pk': pk}))


def request_approve(request, pk):
    if request.method == 'POST':
        bill = get_object_or_404(RequestBill, pk=pk)
        entered_pin = request.POST.get('pin')
        user = request.user
        if user.check_password(entered_pin):
            bill.status = RequestBill.BillStatus.IN_PROGRESS
            bill.billdetail.approve_status = RequestBillDetail.ApproveStatus.WAIT
            bill.billdetail.agent = request.user
            bill.billdetail.add_request_approve_date()
            bill.billdetail.save()
            bill.save()
            return redirect(reverse_lazy('parcel:bill_detail', kwargs={'pk': pk}))
        else:
            return redirect(reverse_lazy('parcel:bill_detail', kwargs={'pk': pk}))


def validate_pin(request, pk):
    """
    Validate pin for approve bill
    use password check to approve bill
    """
    if request.method == 'POST':
        bill = get_object_or_404(RequestBill, pk=pk)
        entered_pin = request.POST.get('pin')
        user = request.user
        if user.check_password(entered_pin):
            bill.billdetail.approve_status = RequestBillDetail.ApproveStatus.APPROVED
            bill.save()
        return redirect(reverse_lazy('parcel:bill_detail', kwargs={'pk': pk}))


def reject_bill(request, pk):
    if request.method == 'POST':
        bill = get_object_or_404(RequestBill, pk=pk)
        note = request.POST.get('note')
        bill_reject = RejectBillNote.objects.create(
            bill=bill,
            user=request.user,
            note=note
        )
        bill.billdetail.approve_status = RequestBillDetail.ApproveStatus.UNAPPROVED
        bill.save()
        return redirect(reverse_lazy('parcel:bill_detail', kwargs={'pk': pk}))
