from django.db import models
from login_app.models import User

class StockManager(models.Manager):
    # insert validator info
    pass

class Stock(models.Model):
    symb = models.CharField(max_length = 5)
    comp_name = models.CharField(max_length = 64)

    # users following
    users = models.ManyToManyField(User, related_name='stocks')

    objects = StockManager()
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

class UserStockManager(models.Manager):
    # insert validator info
    pass

class User_Stock(models.Model):
    # all stock info (symb, name, price, etc) can be imported from Stock class
    stock = models.ForeignKey(Stock, related_name='user_stocks', on_delete = models.CASCADE)

    user = models.ForeignKey(User, related_name='user_stocks', on_delete = models.CASCADE)
    date_purchased = models.DateTimeField(auto_now_add = True)
    purchase_price = models.DecimalField(max_digits = 15, decimal_places = 2)
    quantity_purchased = models.IntegerField()

    # date_sold = *how to use DateTimeField here?
    sold_price = models.DecimalField(max_digits = 15, decimal_places = 2, null=True)
    gain_loss = models.DecimalField(max_digits = 15, decimal_places = 2, null=True)
    percent_gain = models.DecimalField(max_digits = 9, decimal_places = 2, null=True)

    objects = UserStockManager()
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)