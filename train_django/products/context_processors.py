from products.models import BasketItem


def basket_items(request):
    user = request.user

    def sum_params(first, second):
        return first.sum() + second.sum(), first.quantity + second.quantity

    items = BasketItem.objects.filter(user=user) if user.is_authenticated else None
    total_sum = sum(item.sum() for item in items) if items else 0
    total_quantity = sum(item.quantity for item in items) if items else 0

    return {
        'basket_items': items,
        'total_sum': total_sum,
        'total_quantity': total_quantity,
    }
