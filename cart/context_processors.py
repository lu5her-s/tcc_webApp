from django.conf import settings

from cart.models import CartItem


def cart_session(request):
    cart_items_count = CartItem.objects.filter(cart__user=request.user).count()
    return {
        "cart_session": request.session.get(settings.CART_SESSION_ID),
        "cart_items_count": cart_items_count,
    }
