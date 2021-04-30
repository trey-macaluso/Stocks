from django.urls import path

from . import views

urlpatterns = [
    path('', views.index),
    path('user_account', views.display_user_account),
    # need to modify to pass identity of specific stock to display_stock_page function, like hidden input
    path('stock_page/<str:stock_symb>', views.display_stock_page),
    path('buy', views.buy),
    path('sell', views.sell),
    ]