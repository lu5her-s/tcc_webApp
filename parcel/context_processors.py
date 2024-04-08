from .models import ParcelRequest, RequestBillDetail, RequestItem


def items_on_hand(request):
    try:
        all_bill = ParcelRequest.objects.all()
        items_on_hand = RequestItem.objects.filter(
            bill__in=all_bill.filter(
                user=request.user
            ),
        ).filter(bill__billdetail__paid_status=RequestBillDetail.PaidStatus.RECEIVED)
        return {'items_on_hand': items_on_hand}
    except:
        return {'items_on_hand': None}
