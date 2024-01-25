from django.http.response import JsonResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.views.decorators.http import require_POST
from asset.models import Category, StockItem

from .cart import Cart

# Create your views here.

@require_POST
def cart_add(request, category_id):
    cart = Cart(request)
    # category = get_object_or_404(Category, pk=category_id)
    quantity = request.POST.get('quantity', 1)
    overide = request.POST.get('override', False)
    stock = request.POST.get('stock')
    cart.add(
        category_id=category_id,
        quantity=quantity,
        override_quantity=overide
    )
    return redirect('cart:cart_detail')

@require_POST
def update_cart(request, category_id):
    cart = Cart(request)
    category = get_object_or_404(Category, pk=category_id)
    quantity = request.POST.get('quantity', 1)
    cart.update(
        category_id=category_id,
        quantity=quantity
    )
    return redirect('cart:cart_detail')


# @require_POST
# def cart_add(request, category_id):
#     cart = Cart(request)
#     # category = get_object_or_404(Category, pk=category_id)
#     if request.method == 'POST':
#         data = request.POST
#         cart.add(
#             category_id=category_id,
#             quantity=data['quantity'],
#             override_quantity=data['override']
#         )
#     return redirect('cart:cart_detail')


@require_POST
def cart_remove(request, category_id):
    cart = Cart(request)
    product = get_object_or_404(Category, pk=category_id)
    cart.remove(
        category_id=category_id
    )
    return redirect('cart:cart_detail')


def cart_detail(request):
    cart = Cart(request)
    categories = Category.objects.all()
    stock = request.GET.get('stock', 0)
    context = {
        'cart': cart,
        'categories': categories,
        'stock': stock
    }
    return render(request, 'cart/detail.html', context)


def remain_in_stock(request, category_id):
    count = StockItem.objects.filter(category_id=category_id).count()
    return JsonResponse({'count': count})
