from django.conf import settings
from asset.models import Category, StockItem


class Cart:
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart

    def add(self, category_id, quantity=1, override_quantity=False):
        category_id = str(category_id)
        if category_id not in self.cart:
            self.cart[category_id] = {'quantity': 0}
        if override_quantity:
            self.cart[category_id]['quantity'] = int(quantity)
        else:
            self.cart[category_id]['quantity'] += int(quantity)
        self.save()

    def update(self, category_id, quantity):
        self.cart[str(category_id)] = quantity
        self.save()

    def remove(self, category_id):
        if str(category_id) in self.cart:
            del self.cart[str(category_id)]
            self.save()

    def clear(self):
        del self.session[settings.CART_SESSION_ID]
        self.save()

    def save(self):
        self.session.modified = True

    def __iter__(self):
        category_ids = self.cart
        category_ids = [int(category_id) for category_id in category_ids]
        categories = Category.objects.filter(pk__in=category_ids)
        cart = self.cart.copy()
        for category in categories:
            available_quantity = 0
            for item in category.stockitem_set.filter(status=StockItem.Status.AVAILABLE):
                available_quantity += item.quantity
            cart[str(category.id)]['category'] = category
            cart[str(category.id)]['available_quantity'] = available_quantity
            yield cart[str(category.id)]


    def __len__(self):
        return sum(int(item['quantity']) for item in self.cart.values())
