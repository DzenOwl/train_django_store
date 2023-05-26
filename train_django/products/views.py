from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import HttpResponseRedirect
# from django.urls import reverse
from django.views.generic.base import TemplateView
from django.views.generic.list import ListView
from django.core.cache import cache

from common.views import TitleMixin
from products.models import BasketItem, Product, ProductCategory

# from django.core.paginator import Paginator

# Create your views here.


class IndexView(TitleMixin, TemplateView):
    template_name = 'products/index.html'
    title = 'Store'


class ProductsListView(TitleMixin, ListView):
    model = Product
    template_name = 'products/products.html'
    paginate_by = 3
    title = 'Store - Products'

    def get_queryset(self, **kwargs):
        queryset = super(ProductsListView, self).get_queryset()
        category_id = self.kwargs.get('category_id')

        return queryset.filter(category_id=category_id) if category_id else queryset

    def get_context_data(self, **kwargs):
        context = super(ProductsListView, self).get_context_data(**kwargs)
        categories = cache.get('categories')
        if not categories:
            timeout = 30
            context['categories'] = ProductCategory.objects.all()
            cache.set('categories', context['categories'], timeout)
        else:
            context['categories'] = categories
        return context


# не переводим в класс, т.к. это избыточно: слишком много надо переопределять
@login_required
def basket_add_item(request, product_id):
    user = request.user
    current_page = HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    product = Product.objects.get(id=product_id)
    basket_items = BasketItem.objects.filter(user=user, product=product)

    if not basket_items.exists():
        BasketItem.objects.create(user=user, product=product, quantity=1)
        return current_page
    else:
        basket_item = basket_items.first()
        basket_item.quantity += 1
        basket_item.save()
        return current_page


@login_required
def basket_delete_items(request, id):
    # user = request.user
    current_page = HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    basket_item = BasketItem.objects.get(id=id)
    basket_item.delete()
    return current_page


@login_required
def basket_delete_one_item(request, product_id):
    user = request.user
    current_page = HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    product = Product.objects.get(id=product_id)
    basket_items = BasketItem.objects.filter(user=user, product=product)

    if not basket_items.exists():
        # BasketItem.objects.create(user=user, product=product, quantity=1)
        messages.error(request, "Item doesn't exist")
        print(messages)
        return current_page
    else:
        basket_item = basket_items.first()
        if basket_item.quantity == 1:
            basket_item.delete()
        else:
            basket_item.quantity -= 1
            basket_item.save()
        return current_page

# def index(request):
#     context = {
#         'title': 'Store'
#     }
#     return render(request, 'products/index.html', context)


# def products(request, category_id=None, page=1):
#     context = {
#         'title': 'Products',
#         'categories': ProductCategory.objects.all(),
#     }
#
#     if category_id:
#         current_products = Product.objects.filter(category_id=category_id)
#     else:
#         current_products = Product.objects.all()
#
#     paginator = Paginator(current_products, 3)
#     products_paginator = paginator.page(page)
#     context.update({'products': products_paginator})
#
#     return render(request, 'products/products.html', context)


# def test_context(request):
#     context = {
#         'title': 'Test',
#         'header': 'Welcome!',
#         'username': 'John Doe',
#         'products': [
#             {'name': "Product1", 'price': 100500.0},
#             {'name': "Product2", 'price': 100600.0},
#             {'name': "Product3", 'price': 100700.0},
#         ],
#         # 'promotion': True,
#         'promoted_products': [
#             # {'name': "Promo1", 'old_price': 100500.0, 'price': 100400},
#             # {'name': "Promo2", 'old_price': 100500.0, 'price': 100400},
#         ]
#     }
#     return render(request, 'products/test-context.html', context)
