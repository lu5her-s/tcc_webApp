from .models import ParcelRequest, RequestBillDetail, RequestItem
from asset.models import StockItem, ItemOnHand
from itertools import chain


def items_on_hand(request):
    try:
        # all_bill = ParcelRequest.objects.all()
        # items_on_hand = RequestItem.objects.filter(
        #     bill__in=all_bill.filter(
        #         user=request.user,
        #     ),
        #     item__status=StockItem.Status.ON_HAND,
        # ).filter(bill__billdetail__paid_status=RequestBillDetail.PaidStatus.RECEIVED)
        # item_remove = ItemOnHand.objects.filter(user=request.user, item__status=StockItem.Status.ON_HAND)
        # all_on_hand = list(chain(items_on_hand, item_remove))
        all_on_hand = ItemOnHand.objects.filter(user=request.user, item__status=StockItem.Status.ON_HAND)
        return {'items_on_hand': all_on_hand}
    except:
        return {'items_on_hand': None}
