from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.hashers import make_password, check_password
from .models.product import Product
from .models.category import Category
from .models.customer import Customer
# Create your views here.


def index(request):
    products = None
    categories = Category.get_all_categories();
    categoryID = request.GET.get('category')


    if categoryID:
        products = Product.get_all_products_by_categoryid(categoryID)
    else:
        products = Product.get_all_products();
    data = {'products': products, 'categories': categories}

    return render(request, 'index.html', data)

def signup(request):
    if request.method == 'GET':
        return render(request, 'signup.html')
    else:
        postData = request.POST
        first_name = postData.get('firstname')
        last_name = postData.get('lastname')
        phone = postData.get('phone')
        email = postData.get('email')
        password = postData.get('password')

        # validation
        value = {
            'first_name' : first_name,
            'last_name': last_name,
            'phone': phone,
            'email': email,
        }
        error_message = None

        customer = Customer(first_name=first_name,
                                last_name=last_name,
                                phone=phone,
                                email=email,
                                password=password)


        if (not first_name):
            error_message = 'First name required !!'
        elif len(first_name) < 4:
            error_message = 'Must be of minimun 4 Characters'
        if (not last_name):
            error_message = 'last name required !!'
        elif len(last_name) < 4:
            error_message = 'Must be of minimun 4 Characters'
        elif customer.isExists():
            error_message = 'Email address is already registered'

        elif customer.isExists():
            error_message = 'email already registered'

        # saving
        if not error_message:
            print(first_name, last_name, phone, email, password)
            customer.password = make_password(customer.password)
            customer.register()
            return redirect('index')
        else:
            data = {
                'error': error_message,
                'values': value
            }
            return render(request, 'signup.html', data)


def login(request):
    if request.method == 'GET':
        return render(request, 'login.html')
    else:
        email = request.POST.get('email')
        password = request.POST.get('password')
        customer = Customer.get_customer_by_email(email)
        error_message = None
        if customer:
            flag = check_password(password, customer.password)
            if flag:
                return redirect('index')
            else:
                error_message = 'Email or Password is invalid...'

        print(email, password)
        return render(request, 'login.html', {'error' : error_message})