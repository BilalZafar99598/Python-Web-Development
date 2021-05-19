from django.shortcuts import render, redirect
from store.models.customer import Customer
from django.contrib.auth.hashers import make_password
from django.views import View

class Signup(View):
    def get(self,request):
        return render(request, 'signup.html')

    def post(self,request):
        postData = request.POST
        first_name = postData.get('firstname')
        last_name = postData.get('lastname')
        phone = postData.get('phone')
        email = postData.get('email')
        password = postData.get('password')
        # print(first_name,last_name,phone,email,password)

        values = {
            'first_name': first_name,
            'last_name': last_name,
            'phone': phone,
            'email': email
        }

        # Validation
        error_message = None
        customer = Customer(first_name=first_name,
                            last_name=last_name,
                            phone=phone,
                            email=email,
                            password=password)
        error_message = self.validateCustomer(customer)
        # Saving
        if not error_message:

            customer.password = make_password(customer.password)
            customer.register()
            return redirect('homepage')
        else:
            data = {
                'values': values,
                'error': error_message
            }
            return render(request, 'signup.html', data)

    def validateCustomer(self,customer):
        error_message = None
        if not customer.first_name:
            error_message = 'First Name required'
        elif len(customer.first_name) < 4:
            error_message = 'First Name must be greater than 4 Character'
        if not customer.last_name:
            error_message = 'Last Name required'
        elif len(customer.last_name) < 4:
            error_message = 'Last Name must be greater than 4 Character'
        if not customer.phone:
            error_message = 'Phone required'
        elif len(customer.phone) < 8:
            error_message = 'Phone must be greater than 8 Character'
        if not customer.password:
            error_message = 'Password required'
        elif len(customer.password) < 5:
            error_message = 'Password must be greater than 5 Character'
        elif customer.isExists():
            error_message = "Email Already Exists"

        return error_message
