from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
# from django.views.decorators.cache import cache_page

from products.views import (ProductsListView, basket_add_item,
                            basket_delete_items, basket_delete_one_item)

TIMEOUT = 30
app_name = 'products'

urlpatterns = [
    # path('', cache_page(TIMEOUT)(ProductsListView.as_view()), name='index'),
    path('', ProductsListView.as_view(), name='index'),
    path('<int:category_id>/', ProductsListView.as_view(), name='category'),
    path('page/<int:page>/', ProductsListView.as_view(), name='page'),
    path('basket-add-item/<int:product_id>/', basket_add_item, name='basket_add_item'),
    path('basket-delete-items/<int:id>/', basket_delete_items, name='basket_delete_items'),
    path('basket-delete-one-item/<int:product_id>/', basket_delete_one_item, name='basket_delete_one_item'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
