from asset.models import Category, StockItem
from django.http.response import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from .cart import Cart

# Create your views here.


@require_POST
def cart_add(request, category_id):
    """
    cart_add for add item to cart

    Args:
        request ():
        category_id ():

    Returns:

    """
    cart = Cart(request)
    # category = get_object_or_404(Category, pk=category_id)
    quantity = request.POST.get("quantity", 1)
    overide = request.POST.get("override", False)
    stock = request.POST.get("stock")
    cart.add(category_id=category_id, quantity=quantity, override_quantity=overide)
    return redirect("cart:cart_detail")


@require_POST
def update_cart(request, category_id):
    """
    update_cart for update item in cart

    Args:
        request ():
        category_id ():

    Returns:

    """
    cart = Cart(request)
    category = get_object_or_404(Category, pk=category_id)
    quantity = request.POST.get("quantity", 1)
    cart.update(category_id=category_id, quantity=quantity)
    return redirect("cart:cart_detail")


@require_POST
def cart_remove(request, category_id):
    """
    cart_remove for remove item from cart

    Args:
        request ():
        category_id ():

    Returns:

    """
    cart = Cart(request)
    product = get_object_or_404(Category, pk=category_id)
    cart.remove(category_id=category_id)
    return redirect("cart:cart_detail")


def cart_detail(request):
    """
    cart_detail for cart detail

    Args:
        request ():

    Returns:

    """
    cart = Cart(request)
    categories = Category.objects.all()
    stock = request.GET.get("stock", 0)
    context = {"cart": cart, "categories": categories, "stock": stock}
    return render(request, "cart/detail.html", context)


def remain_in_stock(request, category_id):
    """
    remain_in_stock for check remain in stock

    Args:
        request ():
        category_id ():

    Returns:

    """
    count = StockItem.objects.filter(category_id=category_id).count()
    return JsonResponse({"count": count})
