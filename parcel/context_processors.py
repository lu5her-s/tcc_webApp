from .models import ParcelRequest, RequestBillDetail

def items_on_hand(request):
    try:
        items_on_hand = ParcelRequest.objects.filter(
            user=request.user,
            bill__billdetail__paid_status=RequestBillDetail.PaidStatus.RECEIVED
        )
        return {'items_on_hand': items_on_hand}
    except:
        return {'items_on_hand': None}
