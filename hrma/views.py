from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db import IntegrityError
from django.contrib.auth.forms import PasswordResetForm
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.forms import SetPasswordForm
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth import get_user_model, authenticate, login
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.forms import SetPasswordForm
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_str
from django.conf import settings
from .models import *
from django.contrib import messages
# Create your views here.
def index(request):
    message = "Hello, this is a message from the view!"
    return render(request, 'index.html', {"message":message})

def user_login(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
    
        user = authenticate(username=username, password=password)
        
        print('This is user', user)
        if user:
            if user.is_active:
                login(request, user)
                messages.success(request, "Login successful")
                return HttpResponseRedirect(reverse('landing'))
            else:
                return HttpResponse("Account not active")
        else:
            print("Someone tried to login and failed")
            print("Username: {} and password {}".format(username, password))
            return render(request, 'login1.html', {})
    else:
        return render(request, 'login1.html', {})


@login_required
def landing(request):
    print(request.user)
    context = {}
    if request.user.is_authenticated:       
        user = Employee.objects.all()
        unique_designations = set()
        unique_departments = set()
        for i in user:
            unique_designations.add(i.designation)
            unique_departments.add(i.department)
        context = {'user':user, 'unique_designations': unique_designations, 'unique_departments': unique_departments}
        return render(request, 'landing.html', context)
    else:
        redirect("/user_login")

def filter_employees(request):
    if request.method == 'POST':
        gender = request.POST.get('gender')
        designation = request.POST.get('designation')
        department = request.POST.get('department')

        # Apply filters to the queryset
        queryset = Employee.objects.all()

        if gender and gender != 'Select Gender':
            queryset = queryset.filter(gender=gender)
        if designation:
            queryset = queryset.filter(designation=designation)
        if department:
            queryset = queryset.filter(department=department)

        # Pass the filtered queryset to the template
        context = {'user': queryset}
        return render(request, 'landing.html', context)

    # Handle GET request or other cases
    return render(request, 'landing.html')


@login_required
def updateEmployee(request, employee_id):
    if request.method == "POST":
        # Retrieve form data
        name = request.POST.get('username')
        employee_id = request.POST.get('employeeId')
        gender = request.POST.get('gender')
        date_of_birth = request.POST.get('dob')
        designation = request.POST.get('designation')
        department = request.POST.get('department')
        appointment_date = request.POST.get('appointment_date')

        # Validate the form data
        if name and employee_id and gender and designation and department :
            try:
                # Retrieve the existing employee
                employee = Employee.objects.get(employee_id=employee_id)
                # Update the existing employee with the new data
                employee.name = name
                employee.gender = gender
                employee.date_of_birth = date_of_birth
                employee.designation = designation
                employee.department = department
                employee.appointment_date = appointment_date
                employee.save()
                messages.success(request, "Update successful")
                return redirect('landing')  # Redirect to the 'landing' URL
            except Employee.DoesNotExist:
                return HttpResponse("Employee does not exist")  # Display an error message if the employee does not exist

    # If the request is not a POST or the form data is invalid,
    # you can handle it accordingly, for example, display an error message or render a form again.
    return HttpResponse("Invalid request")  # Modify this line according to your needs

@login_required
def addEmployee(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        employee_id = request.POST.get('employee_id')
        gender = request.POST.get('gender')
        date_of_birth = request.POST.get('dob')
        designation = request.POST.get('designation')
        department = request.POST.get('department')
        appointment_date = request.POST.get('appointmentDate')

        # Validate the form data
        if name and employee_id and gender and date_of_birth and designation and department and appointment_date:
            # Create a new employee object
            employee = Employee(
                name=name,
                employee_id=employee_id,
                gender=gender,
                date_of_birth=date_of_birth,
                designation=designation,
                department=department,
                appointment_date=appointment_date
            )
            employee.save()
            messages.success(request, "Employee added successfully")
            return redirect('landing')  # Redirect to a success page or another URL

    # Return a default response if the request method is not POST or the form data is invalid
    return HttpResponse("Invalid request")


def employee(request):
    user = Employee.objects.all()
    print(user)
    context = {'user':user}
    return render(request, 'employee.html', context)



@login_required
def delete_user(request, pid):
    employe = Employee.objects.get(id=pid)
    if request.method == "GET":
        employe.delete()
        messages.success(request, "Successfully deleted an employee")
        return redirect("landing")

def user_logout(request):
    logout(request)
    return redirect("/")

