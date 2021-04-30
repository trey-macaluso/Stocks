from django.shortcuts import render, redirect, HttpResponse
from login_app.models import User
from stocks_app.models import Stock, User_Stock
from django.contrib import messages
from decimal import *


def index(request):
    if 'user_id' in request.session:
        context={
            'user': User.objects.get(id=request.session['user_id'])
        }
        return render(request, 'index.html', context)
    return render(request, 'index.html')

def display_user_account(request):
    if 'user_id' not in request.session:
        messages.error(request, 'You must be logged in to view this page')
        return redirect('/')
    context = {
        'user': User.objects.get(id=request.session['user_id'])
    }
    return render(request, 'user_account.html', context)

def display_stock_page(request,stock_symb):
    # session stock would be declared by hyperlink call
    request.session['stock_symb'] = stock_symb
    print(request.session['stock_symb'])
    context = {
        # change id to variable, hardcoding for test purposes
        'curr_stock': Stock.objects.get(symb=stock_symb)
    }
    return render(request, 'stock_page.html', context)

def buy(request):
    curr_user = User.objects.get(id=request.session['user_id'])

    curr_stock = Stock.objects.get(symb=request.session['stock_symb'])

    # check if button was pressed without inputting quantity
    if request.POST['quantity'] == '':
        return redirect(f'/stock_page/{curr_stock.symb}')

    if int(request.POST['quantity']) * Stock.objects.get(symb = curr_stock.symb).curr_price > curr_user.balance:
        messages.error(request, 'Insufficient funds to complete buy request')

        return redirect(f'/stock_page/{curr_stock.symb}')

    stock = curr_stock
    user = curr_user
    purchase_price = stock.curr_price
    quantity_purchased = int(request.POST['quantity'])

    User_Stock.objects.create(stock=stock,user=user,purchase_price=purchase_price,quantity_purchased=quantity_purchased)

    curr_user.balance = curr_user.balance - (purchase_price * quantity_purchased)
    curr_user.save()
    print(curr_user.balance)

    return HttpResponse('buy path works <(^^<) <(^^)> (>^^)>')

def sell(request):
    # what happens if the sell quantity exceeds any given open trade's purchased quantity? figure out a way to write it so that the oldest trades close first, then if there is a remainder, begin closing them in that order. get a queryset of user_stock objects held in the current user's object, ordered by purchase date, then iterate through them as mentioned

    curr_user = User.objects.get(id=request.session['user_id'])
    curr_stock = Stock.objects.get(symb=request.session['stock_symb'])
    user_stock_list = curr_user.user_stocks.filter(stock=curr_stock).order_by('-quantity_purchased')

    # check if button was pressed without inputting quantity
    if request.POST['quantity'] == '':
        return redirect(f'/stock_page/{curr_stock.symb}')

    total_quantity = 0
    for user_stock in user_stock_list:
        total_quantity += user_stock.quantity_purchased
    
    if int(request.POST['quantity']) > total_quantity:
        messages.error(request, 'Insufficient quantity to complete sell request')

        return redirect(f'/stock_page/{curr_stock.symb}')

    # need main sell function

    return HttpResponse('sell path works <(^^<) <(^^)> (>^^)>')