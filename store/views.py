from django.shortcuts import render
from django.http import JsonResponse
import json
import datetime
from .models import * 
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from .utils import cookieCart, cartData, guestOrder
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm

def store(request):
	data = cartData(request)

	cartItems = data['cartItems']
	order = data['order']
	items = data['items']

	products = Product.objects.all()
	context = {'products':products, 'cartItems':cartItems}
	return render(request, 'store/store.html', context)



def home(request):
    return render(request, 'store/theRow.html')


def loginPage(request):
    if request.user.is_authenticated:
        return render(request,'store/members.html')
        
    else:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(request, username = username, password = password)

            if user is not None:
                login(request, user)
                return render(request,'store/members.html')
            else: 
                messages.info(request, 'Username OR Password is incorrect')
           


    context={}
    return render(request, 'store/loginPage.html', context)



def cart(request):
	data = cartData(request)

	cartItems = data['cartItems']
	order = data['order']
	items = data['items']

	context = {'items':items, 'order':order, 'cartItems':cartItems}
	return render(request, 'store/cart.html', context)

def checkout(request):
	data = cartData(request)
	
	cartItems = data['cartItems']
	order = data['order']
	items = data['items']

	context = {'items':items, 'order':order, 'cartItems':cartItems}
	return render(request, 'store/checkout.html', context)

def updateItem(request):
	data = json.loads(request.body)
	productId = data['productId']
	action = data['action']
	print('Action:', action)
	print('Product:', productId)

	customer = request.user.customer
	product = Product.objects.get(id=productId)
	order, created = Order.objects.get_or_create(customer=customer, complete=False)

	orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

	if action == 'add':
		orderItem.quantity = (orderItem.quantity + 1)
	elif action == 'remove':
		orderItem.quantity = (orderItem.quantity - 1)

	orderItem.save()

	if orderItem.quantity <= 0:
		orderItem.delete()

	return JsonResponse('Item was added', safe=False)

def processOrder(request):
	transaction_id = datetime.datetime.now().timestamp()
	data = json.loads(request.body)

	if request.user.is_authenticated:
		customer = request.user.customer
		order, created = Order.objects.get_or_create(customer=customer, complete=False)
	else:
		customer, order = guestOrder(request, data)

	total = float(data['form']['total'])
	order.transaction_id = transaction_id

	if total == order.get_cart_total:
		order.complete = True
	order.save()

	if order.shipping == True:
		ShippingAddress.objects.create(
		customer=customer,
		order=order,
		address=data['shipping']['address'],
		city=data['shipping']['city'],
		state=data['shipping']['state'],
		zipcode=data['shipping']['zipcode'],
		)

	return JsonResponse('Payment submitted..', safe=False)



def new_products(request):
	data = cartData(request)

	cartItems = data['cartItems']
	order = data['order']
	items = data['items']
	
	new = New.objects.all()
	context = {'new':new, 'cartItems':cartItems}
	return render(request, 'store/newProducts.html', {'new': new, 'cartItems':cartItems})


def members(request):
    return render(request, 'store/exclusive.html')


@login_required(login_url='loginPage')
def exclusive(request):
    return render(request, 'store/members.html')



def register(request):
    if request.user.is_authenticated:
        return render(request, 'store/loginPage.html')
    else:
        form = UserCreationForm()

        if request.method == 'POST':
                form = UserCreationForm(request.POST)
                if form.is_valid():
                    form.save()
                    user = form.cleaned_data.get('username')
                    messages.success(request, 'Account was created for ' + user)
                    return render(request,'store/loginPage.html',context)
                    



        context = {'form': form}
        return render(request, 'store/register.html', context)


def logoutUser(request):
    logout(request)
    return render(request,'store/loginPage.html')