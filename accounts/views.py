from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import *
from .form import *
from django.forms import inlineformset_factory
from .filters import *
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from .decorators import *
from django.contrib.auth import views as auth_views
from django.core.mail import EmailMessage
from django.conf import settings

def send_email(request):
    
    if request.method == 'POST':
        email = request.POST['email']
        message = request.POST['message']
        
        email_instance = EmailMessage(
            subject='test email',
            body= message,
            from_email=settings.EMAIL_HOST_USER,
            to=[email,]
        )
        
        email_instance.fail_silently = False
        
        email_instance.send()
        
        print('===========success=======================')
        print(f'email: {email}, message: {message}')
        print('===========success=======================')
    
    return render(request, 'accounts/send_email.html')

@unauthenticated_user
def loginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.info(request, 'username or password was incorrect')
    
    context = {}
    return render(request, 'accounts/login.html', context=context)


def logoutUser(request):
    logout(request)
    return redirect('login')
    
@unauthenticated_user
def register(request):
    form = CreateUserForm()
    
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()

            
            messages.success(request, f'account was created for {form.cleaned_data.get('username')}')
            return redirect('login')
            
    context = {'form':form}
    return render(request, 'accounts/register.html', context=context)



@login_required(login_url='login')
@admin_only
def home(request):
    orders = Order.objects.all()
    customers = Customer.objects.all()
    
    total_customers = customers.count()
    total_orders = orders.count()
    delivered_count = orders.filter(status='Delivered').count()
    pending_count = orders.filter(status='Pending').count()
    
    context = {'orders': orders, 'customers': customers, 
               'total_customers': total_customers, 'total_orders':total_orders, 
               'delivered_count':delivered_count, 'pending_count': pending_count}
    
    return render(request, 'accounts/dashboard.html', context=context)

@login_required(login_url='login')
@allowed_users(allowred_roles=['admin'])
def products(request):
    products = Product.objects.all()
    return render(request, 'accounts/products.html', context={'products': products})

@login_required(login_url='login')
@allowed_users(allowred_roles=['admin'])
def customer(request, pk):
    customer = Customer.objects.get(id=pk)
    orders = customer.order_set.all()
    orders_count = orders.count()
    
    myFilter = OrderFilter(request.GET, queryset=orders)
    orders = myFilter.qs
    
    context = {'customer':customer, 'orders': orders, 'orders_count': orders_count, 'myFilter': myFilter}
    return render(request, 'accounts/customer.html', context=context)


@login_required(login_url='login')
@allowed_users(allowred_roles=['admin'])
def createOrder(request, customer_id):
	OrderFormSet = inlineformset_factory(Customer, Order, fields=('product', 'status'), extra=10 )
	customer = Customer.objects.get(id=customer_id)
	formset = OrderFormSet(queryset=Order.objects.none(),instance=customer)
	#form = OrderForm(initial={'customer':customer})
	if request.method == 'POST':
		#print('Printing POST:', request.POST)
		#form = OrderForm(request.POST)
		formset = OrderFormSet(request.POST, instance=customer)
		if formset.is_valid():
			formset.save()
			return redirect('/')

	context = {'form':formset}
	return render(request, 'accounts/order_form.html', context)

@login_required(login_url='login')
@allowed_users(allowred_roles=['admin'])
def updateOrder(request, pk):
    order = Order.objects.get(id=pk)
    form = OrderForm(instance=order)
    if request.method == 'POST':
        form = OrderForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            return redirect('/')
    
    context = {'form':form}
    
    return render(request, 'accounts/order_form.html', context=context)

@login_required(login_url='login')
@allowed_users(allowred_roles=['admin'])
def delete(request, pk):
    order = Order.objects.get(id=pk)
    context = {'order':order}
    if request.method == 'POST':
        order.delete()
        return redirect('/')
    return render(request, 'accounts/delete.html', context=context)

@login_required(login_url='login')
@allowed_users(allowred_roles=['customer'])
def userPage(request):
    orders = request.user.customer.order_set.all()
    total_orders = orders.count()
    delivered_count = orders.filter(status='Delivered').count()
    pending_count = orders.filter(status='Pending').count()
    print('orders', orders)
    context = {'orders': orders,'total_orders':total_orders, 
               'delivered_count':delivered_count, 'pending_count': pending_count}
    return render(request, 'accounts/user.html', context=context)

@login_required(login_url='login')
@allowed_users(allowred_roles=['customer'])
def accountSettings(request):
    customer = request.user.customer
    form = CustomerForm(instance=customer)
    if request.method == 'POST':
        form = CustomerForm(request.POST, request.FILES, instance=customer)
        if form.is_valid():
            form.save()
        
    context = {'form': form}
    return render(request, 'accounts/account_setting.html', context=context)