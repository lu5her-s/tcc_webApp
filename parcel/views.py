#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# File              : views.py
# Author            : lu5her <lu5her@mail>
# Date              : Thu Apr, 18 2024, 20:38 109
# Last Modified Date: Thu Apr, 18 2024, 20:39 109
# Last Modified By  : lu5her <lu5her@mail>
# -----
import os
from itertools import chain
from django.template.loader import render_to_string
from django.db.models import Q
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
    ItemHistory,
    ItemOnHand,
    StockItem,
    Category
)
from account.models import (
    Department,
    Profile
)

from .models import (
    ParcelRequestNote,
    ParcelRequest,
    ParcelReturn,
    ParcelReturnDetail,
    ParcelReturnItem,
    RejectBillNote,
    RequestBillDetail,
    RequestItem
)
from .forms import RequestBillDetailForm, SelectStockForm, ReturnBillDetailForm
from cart.cart import Cart
from config.utils import generate_pdf

# Create your views here.

class ParcelHomeView(LoginRequiredMixin, TemplateView):
    """A class-based view for the home page of the parcel application."""

    template_name = 'parcel/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        all_bill = ParcelRequest.objects.all()
        context['all_bill'] = all_bill.filter(user=self.request.user)
        context['wait_approve'] = all_bill.filter(billdetail__approve_status=RequestBillDetail.ApproveStatus.WAIT)
        context['bill_draft'] = all_bill.filter(status=ParcelRequest.RequestStatus.DRAFT)
        context['parcel_list'] = RequestItem.objects.filter(
            bill__in=all_bill.filter(
                user=self.request.user
            ),
            item__status=StockItem.Status.ON_HAND
        )

        # TODO: command context
        # for command views

        # for manager views
        context['stock_bills'] = all_bill.filter(
            stock=self.request.user.profile.department,
            status=ParcelRequest.RequestStatus.REQUEST,
        )
        context['stock_bills_wait'] = all_bill.filter(
            stock=self.request.user.profile.department,
            status=ParcelRequest.RequestStatus.IN_PROGRESS,
            billdetail__approve_status=RequestBillDetail.ApproveStatus.WAIT
        )
        context['wait_paid'] = all_bill.filter(
            stock=self.request.user.profile.department,
            status=ParcelRequest.RequestStatus.IN_PROGRESS,
            billdetail__approve_status=RequestBillDetail.ApproveStatus.APPROVED,
            is_done=False,
        ).exclude(billdetail__paid_status=RequestBillDetail.PaidStatus.RECEIVED)
        context['all_stock_bills'] = all_bill.filter(
            Q(stock=self.request.user.profile.department) & ~Q(status=ParcelRequest.RequestStatus.DRAFT),
        )

        # context['on_hand'] = Q(all_bill.billitems.filter(item.status==StockItem.Status.AVAILABLE)) & Q(all_bill.bill_detail.filter(is_paid=True))
        # context['on_hand'] = (Q(RequestItem.objects.filter(item__status=StockItem.Status.AVAILABLE, bill__in=all_bill)) & Q(
        #     all_bill.filter(billdetail__is_paid=True)
        # )).count()
        context['on_hand'] = RequestItem.objects.filter(
            bill__in=all_bill.filter(
                user=self.request.user
            ),
        ).filter(bill__billdetail__paid_status=RequestBillDetail.PaidStatus.RECEIVED)
        
        # for return parcel bill
        all_return = ParcelReturn.objects.filter(user=self.request.user)
        context['all_return'] = all_return
        context['return_draft'] = all_return.filter(status=ParcelReturn.Status.DRAFT)
        context['return_wait_approve'] = ParcelReturnDetail.objects.filter(
            bill__in=all_return.filter(
                user=self.request.user
            ),
            approve_status=RequestBillDetail.ApproveStatus.WAIT
        )
        return context


class BillListView(LoginRequiredMixin, ListView):
    template_name = 'parcel/bill_list.html'
    model = ParcelRequest

    def get_queryset(self):
        return self.model.objects.filter(user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'รายการใบเบิก'
        return context


class BillManagerListView(LoginRequiredMixin, ListView):
    template_name = 'parcel/bill_list.html'
    model = ParcelRequest

    def queryset(self):
        return self.model.objects.filter(
            stock=self.request.user.profile.department,
            status=ParcelRequest.RequestStatus.REQUEST
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'รายการใบเบิกรอตรวจสอบ'
        return context


class BillWaitApproveListView(LoginRequiredMixin, ListView):
    template_name = 'parcel/bill_list.html'
    model = ParcelRequest

    def get_queryset(self):
        return self.model.objects.filter(
            stock=self.request.user.profile.department,
            status=ParcelRequest.RequestStatus.IN_PROGRESS,
            billdetail__approve_status=RequestBillDetail.ApproveStatus.WAIT
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'รายการใบเบิกรออนุมัติ'
        return context


class BillWaitPaidListView(LoginRequiredMixin, ListView):
    template_name = 'parcel/bill_list.html'
    model = ParcelRequest

    def get_queryset(self):
        return self.model.objects.filter(
            stock=self.request.user.profile.department,
            status=ParcelRequest.RequestStatus.IN_PROGRESS,
            billdetail__approve_status=RequestBillDetail.ApproveStatus.APPROVED,
            is_done=False
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'รายการใบเบิกรอจ่าย'
        return context


class ManagerAllBillListView(LoginRequiredMixin, ListView):
    template_name = 'parcel/bill_list.html'
    model = ParcelRequest

    def get_queryset(self):
        return self.model.objects.filter(
            Q(stock=self.request.user.profile.department) & ~Q(status=ParcelRequest.RequestStatus.DRAFT),
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
            stock_control=stock,
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
        stock = request.POST.get('stock')
        stock = get_object_or_404(Department, pk=stock)
        print(stock)
        bill = ParcelRequest.objects.create(
            user=request.user,
            stock=stock,
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
        # return HttpResponse(stock)

    # def get(self, request):
    #     form = BillCreateForm()
    #     return render(request, 'parcel/bill_create.html', {'form': form})


class BillDetailView(LoginRequiredMixin, DetailView):
    template_name = 'parcel/bill_detail2.html'
    # template_name = 'parcel/detail.html'
    model = ParcelRequest

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        bill = self.get_object()
        # bill = get_object_or_404(ParcelRequest, pk=object.pk)
        recievers = Profile.objects.exclude(user=bill.user)
        items = RequestItem.objects.filter(bill=bill)
        replace_item = StockItem.objects.all().exclude(id__in=items)
        bill_detail, _ = RequestBillDetail.objects.get_or_create(bill=bill)
        locations = Department.objects.all().order_by('name')
        context = {
            'bill': bill,
            'items': items,
            'bill_detail': bill_detail,
            'recievers': recievers,
            'bill_detail_form': RequestBillDetailForm(instance=bill_detail),
            'locations': locations,
            'replace_item': replace_item
        }
        return context

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


class ParcelListView(ListView):
    model = RequestItem
    template_name = 'parcel/parcel_list.html'
    context_object_name = 'object_list'

    def get_queryset(self):
        return RequestItem.objects.filter(
            bill__user=self.request.user,
            bill__billdetail__paid_status=RequestBillDetail.PaidStatus.RECEIVED
        ).select_related('bill__user')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Parcel List'
        context['replace_item'] = StockItem.objects.all().exclude(id__in=self.get_queryset())
        context['locations'] = Department.objects.all().order_by('name')
        return context


# TODO: refactor and make set item to form submit all in form save all[template]
def set_serial_item(request, pk):
    bill = get_object_or_404(ParcelRequest, pk=pk)
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


# def request_approve(request, pk):
#     bill = get_object_or_404(ParcelRequest, pk=pk)
#     bill.status = ParcelRequest.RequestStatus.IN_PROGRESS
#     bill.billdetail.approve_status = RequestBillDetail.ApproveStatus.WAIT
#     bill.save()
#     return redirect(reverse_lazy('parcel:bill_detail', kwargs={'pk': pk}))


# def approve_bill(request, pk):
#     bill = get_object_or_404(RequestBill, pk=pk)
#     bill.billdetail.approve_status = RequestBillDetail.ApproveStatus.APPROVED
#     bill.save()
#     return redirect(reverse_lazy('parcel:bill_detail', kwargs={'pk': pk}))


def bill_to_pdf(request: HttpResponse, pk: int):
    bill = ParcelRequest.objects.get(pk=pk)
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
    bill = get_object_or_404(ParcelRequest, pk=pk)
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
    ParcelRequest.objects.filter(pk=pk).update(status=ParcelRequest.RequestStatus.REQUEST)
    return redirect(reverse_lazy('parcel:bill_detail', kwargs={'pk': pk}))


def request_approve(request, pk):
    if request.method == 'POST':
        bill = get_object_or_404(ParcelRequest, pk=pk)
        entered_pin = request.POST.get('pin')
        user = request.user
        if user.check_password(entered_pin):
            bill.status = ParcelRequest.RequestStatus.IN_PROGRESS
            bill.billdetail.approve_status = RequestBillDetail.ApproveStatus.WAIT
            bill.billdetail.agent = request.user
            bill.billdetail.add_request_approve_date()
            bill.billdetail.save()
            bill.save()
            return redirect(reverse_lazy('parcel:bill_detail', kwargs={'pk': pk}))
        else:
            return redirect(reverse_lazy('parcel:bill_detail', kwargs={'pk': pk}))


def approve_bill(request, pk):
    """
    Validate pin for approve bill
    use password check to approve bill
    """
    if request.method == 'POST':
        bill = get_object_or_404(ParcelRequest, pk=pk)
        entered_pin = request.POST.get('pin')
        user = request.user
        if user.check_password(entered_pin):
            bill.billdetail.approve_status = RequestBillDetail.ApproveStatus.APPROVED
            bill.billdetail.mark_as_approved(user)
            # bill.billdetail.save()
            # bill.save()
        return redirect(reverse_lazy('parcel:bill_detail', kwargs={'pk': pk}))


def reject_bill(request, pk):
    if request.method == 'POST':
        bill = get_object_or_404(ParcelRequest, pk=pk)
        note = request.POST.get('note')
        RejectBillNote.objects.create(
            bill=bill,
            user=request.user,
            note=note
        )
        bill.billdetail.approve_status = RequestBillDetail.ApproveStatus.UNAPPROVED
        bill.billdetail.save()
        bill.save()
        return redirect(reverse_lazy('parcel:bill_detail', kwargs={'pk': pk}))


class CommandWaitApproveListView(LoginRequiredMixin, ListView):
    model = ParcelRequest
    template_name = 'parcel/bill_list.html'
    # context_object_name = 'bills'

    def get_queryset(self):
        return self.model.objects.filter(
            billdetail__approve_status=RequestBillDetail.ApproveStatus.WAIT,
            status=ParcelRequest.RequestStatus.IN_PROGRESS
        )


class PaidItemView(LoginRequiredMixin, DetailView):
    model = ParcelRequest
    template_name = 'parcel/bill_detail.html'

    def post(self, request, *args, **kwargs):
        bill = self.get_object()
        entered_pin = request.POST.get('pin')
        user = request.user
        if user.check_password(entered_pin):
            bill.billdetail.mark_as_paid(user)
            RequestItem.objects.filter(bill=bill).update(paid=True)
        return redirect(reverse_lazy('parcel:bill_detail', kwargs={'pk': bill.pk}))


# class PaidItemView(View):
#     def post(self, request, pk):
#         bill = get_object_or_404(ParcelRequest, pk=pk)
#         entered_pin = request.POST.get('pin')
#         user = request.user
#
#         if user.check_password(entered_pin):
#             bill.billdetail.mark_as_paid(user)
#             RequestItem.objects.filter(bill=bill).update(paid=True)
#
#         return redirect(reverse_lazy('parcel:bill_detail', kwargs={'pk': pk}))



class RecieveItemsView(LoginRequiredMixin, DetailView):
    model = ParcelRequest
    template_name = 'parcel/bill_detail.html'

    def post(self, request, pk):
        bill = self.get_object()
        entered_pin = request.POST.get('pin')
        user = request.user

        if user.check_password(entered_pin):
            items = RequestItem.objects.filter(bill=bill)
            item_on_hand = []
            for item in items:
                item.mark_as_received()
                item_on_hand.append(ItemOnHand(item=item.item, user=user))
            ItemOnHand.objects.bulk_create(item_on_hand)
            bill.billdetail.mark_as_received()
            print(item_on_hand)
        else:
            # show alert
            print("wrong pin")
            return HttpResponse("wrong pin")
        return redirect(reverse_lazy('parcel:bill_detail', kwargs={'pk': pk}))

    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


class ParcelDetailView(LoginRequiredMixin, DetailView):
    model = RequestItem
    template_name = 'parcel/parcel_detail.html'
    context_object_name = 'parcel'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        parcel = self.get_object()
        bill = get_object_or_404(ParcelRequest, pk=parcel.bill.pk)
        location = Department.objects.all()
        items = StockItem.objects.all()
        context['bill'] = bill
        context['location'] = location
        context['items'] = items
        return context


class SetItemLocationView(LoginRequiredMixin, View):
    def post(self, request):
        pin = request.POST.get('pin-set-item')
        user = request.user
        if user.check_password(pin):
            item_pk = request.POST.get('item_pk')
            location = request.POST.get('location')
            item = StockItem.objects.get(pk=item_pk)
            location = get_object_or_404(Department, pk=location)
            item.location_install = location
            item.status = StockItem.Status.IN_USE
            item.itenonhand.is_done = True
            item.itemonhand.save()
            item.save()

            # create ItemHistory
            description = f'{item.item_name} set in {location}'
            ItemHistory.objects.create(
                item=item,
                user=user,
                description=description
            )

            return redirect(reverse_lazy('parcel:bill_detail', kwargs={'pk': item.bill.pk}))
        else:
            return HttpResponse("wrong pin")

    def get(self):
        return HttpResponse("Error")

class ReplaceItemLocationView(LoginRequiredMixin, View):
    def post(self, request):
        pin = request.POST.get('pin-replace-item')
        user = request.user
        if user.check_password(pin):
            replace_item = request.POST.get('replace_item')
            replace_item = get_object_or_404(StockItem, pk=replace_item)
            location = replace_item.location_install
            replace_item.location_install = None
            replace_item.status = StockItem.Status.ON_HAND
            replace_item.save()

            new_item = request.POST.get('new_item')
            new_item = get_object_or_404(StockItem, pk=new_item)
            new_item.location_install = location
            new_item.status = StockItem.Status.IN_USE
            new_item.itemonhand.is_done = True
            new_item.itemonhand.save()
            new_item.save()

            # create ItemHistory for this
            description = f'Replace item {replace_item.name} with {new_item.name}'
            ItemHistory.objects.create(
                item=replace_item,
                user=user,
                description=description
            )
            description = f'{new_item.name} Set in {location}'
            ItemHistory.objects.create(
                item=new_item,
                user=user,
                description=description
            )

            return redirect(reverse_lazy('parcel:bill_detail', kwargs={'pk': new_item.bill.pk}))
        else:
            return HttpResponse("wrong pin")

    def get(self):
        return HttpResponse("Error")


class ItemOnHandListView(LoginRequiredMixin, ListView):
    template_name = 'parcel/item_on_hand_list.html'

    def get_queryset(self):
        # all_parcel_request = RequestItem.objects.filter(bill__user=self.request.user, bill__billdetail__paid_status=RequestBillDetail.PaidStatus.RECEIVED).select_related('bill__user')
        on_hand = ItemOnHand.objects.filter(user=self.request.user, item__status=StockItem.Status.ON_HAND)
        # stock_on_hand = StockItem.objects.filter(status=StockItem.Status.ON_HAND, itemonhand__user=self.request.user)
        return on_hand

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        items = self.get_queryset()
        replace_item = StockItem.objects.all().exclude(id__in=items)
        locations = Department.objects.all().order_by('name')
        context = {
            'items': items,
            'locations': locations,
            'replace_item': replace_item
        }
        return context


class ReturnParcelCreateView(LoginRequiredMixin, View):
    def post(self, request):
        # items = request.POST.getlist('return_item')
        items = StockItem.objects.filter(pk__in=request.POST.getlist('return_item'))
        # location_set = set(StockItem.objects.filter(pk__in=items).values_list('location', flat=True))
        location_set = items.values_list('stock_control', flat=True).distinct()
        # item_location = ItemOnHand.objects.filter(item__location__in=location_set)
        item_location = ItemOnHand.objects.prefetch_related('item').filter(item__stock_control__in=location_set, user=request.user)

        for location in location_set:
            items_on = item_location.filter(item__stock_control=location)
            stock = Department.objects.get(pk=location)
            return_parcel = ParcelReturn.objects.create(
                stock=stock,
                user=request.user
            )
            ParcelReturnDetail.objects.create(
                bill=return_parcel,
            )
            # print(f'Stock : {stock} --  Have {items.count()} items')
            # ParcelReturnItem.objects.bulk_create([
            #     ParcelReturnItem(
            #         bill=return_parcel,
            #         item=item.item
            #     )
            #     for item in items
            # ])
            for item in items_on:
                ParcelReturnItem.objects.create(
                    bill=return_parcel,
                    item=item.item
                )
                item.item.status = StockItem.Status.CHECK
                item.item.save()
            # StockItem.objects.filter(pk__in=items.values_list('pk', flat=True)).update(status=StockItem.Status.CHECK)

                # print(f' = {item} -- {item.item.status}')

        return redirect(reverse_lazy('parcel:return_parcel_list'))


class ParcelReturnListView(LoginRequiredMixin, ListView):
    model = ParcelReturn
    template_name = 'parcel/parcel_return_list.html'

    def get_queryset(self):
        return ParcelReturn.objects.filter(user=self.request.user)


class ParcelReturnDraftListView(LoginRequiredMixin, ListView):
    model = ParcelReturn
    template_name = 'parcel/parcel_return_draft_list.html'

    def get_queryset(self):
        return ParcelReturn.objects.filter(user=self.request.user, status=ParcelReturn.Status.DRAFT)


class ReturnParcelDetailView(LoginRequiredMixin, DetailView):
    '''
    This view is a detail view for the ParcelReturn model.
    It is used to display the details of a specific parcel return.
    '''
    model = ParcelReturn
    template_name = 'parcel/parcel_return_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'ใบส่งคืน'
        context['bill'] = self.object
        context['items'] = ParcelReturnItem.objects.filter(bill=self.object)
        context['bill_detail_form'] = ReturnBillDetailForm(instance=self.object.billdetail)
        return context


def save_return_draft(request, pk):
    if request.method == 'POST':
        data = request.POST
        bill = ParcelReturn.objects.get(pk=pk)
        bill_detail = bill.billdetail
        bill_detail.return_case = data.get('return_case')
        bill_detail.item_type = data.get('item_type')
        bill_detail.item_control = data.get('item_control')
        bill_detail.money_type = data.get('money_type')
        bill_detail.job_no = data.get('job_no')
        bill_detail.return_no = data.get('return_no')
        bill_detail.save()
    return redirect(reverse_lazy('parcel:return_parcel_detail', kwargs={'pk': pk}))


def return_item(request, pk):
    if request.method == 'POST':
        ParcelReturn.objects.filter(pk=pk).update(status=ParcelReturn.Status.REQUEST)
    return redirect(reverse_lazy('parcel:return_parcel_detail', kwargs={'pk': pk}))


class AllDraftListView(LoginRequiredMixin, View):
    '''
    View for list all draft return bill
    '''
    template_name = 'parcel/all_draft_list.html'

    def get_queryset(self):
        request_bill = ParcelRequest.objects.filter(user=self.request.user, status=ParcelRequest.RequestStatus.DRAFT)
        return_bill = ParcelReturn.objects.filter(user=self.request.user, status=ParcelReturn.Status.DRAFT)
        all_draft = list(chain(request_bill, return_bill))
        return all_draft


# for render location list for select to get item remove from this
class LocationListView(LoginRequiredMixin, ListView):
    model = Department
    template_name = 'parcel/location_list.html'


class ItemOnLocationView(LoginRequiredMixin, View):
    template_name = 'parcel/remove_item.html'

    def get(self, request, pk):
        context = {
            'object_list' : StockItem.objects.filter(location_install__pk=pk),
            'location' : Department.objects.get(pk=pk)
        }
        return render(self.request, self.template_name, context)


class RemoveItemView(LoginRequiredMixin, View):

    def post(self, request):
            remove_items = request.POST.getlist('remove_item')
            items_to_create = []
            for item_id in remove_items:
                items_to_create.append(ItemOnHand(item_id=item_id, user=request.user))

            ItemOnHand.objects.bulk_create(items_to_create)

            StockItem.objects.filter(pk__in=remove_items).update(status=StockItem.Status.ON_HAND, location_install=None)

            return redirect(reverse_lazy('parcel:location_list'))
