from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect
from .models import *
from .restapis import *
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from datetime import datetime
import logging
import json
from django.db import models
from django.core import serializers
from django.utils.timezone import now
import uuid

# Get an instance of a logger
logger = logging.getLogger(__name__)


# Create your views here.
def get_about(request):
    context = {}
    return render(request, 'djangoapp/about.html', context)


# Create a `contact` view to return a static contact page
def get_contact(request):
    context = {}
    return render(request, 'djangoapp/contact.html', context)

# Create a `login_request` view to handle sign in request
def login_request(request):
    context = {}
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['psw']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return render(request, 'djangoapp/index.html', context)
        else:
            context['message'] = "Invalid username or password."
            return render(request, 'djangoapp/index.html', context)
    else:
        context['message'] = "Invalid request."
        return render(request, 'djangoapp/index.html', context)


# Create a `logout_request` view to handle sign out request
def logout_request(request):
    print("Log out the user '{}'".format(request.user.username))
    logout(request)
    return redirect('djangoapp:index')

# Create a `registration_request` view to handle sign up request
def registration_request(request):
    context = {}
    if request.method == 'GET':
        return render(request, 'djangoapp/registration.html', context)
    elif request.method == 'POST':
        # Check if user exists
        username = request.POST['username']
        password = request.POST['psw']
        first_name = request.POST['firstname']
        last_name = request.POST['lastname']
        user_exist = False
        try:
            User.objects.get(username=username)
            user_exist = True
        except:
            logger.error("New user")
        if not user_exist:
            user = User.objects.create_user(username=username, first_name=first_name, last_name=last_name,
                                            password=password)
            user.is_superuser = True
            user.is_staff=True
            user.save()  
            login(request, user)
            return redirect("djangoapp:index")
        else:
            messages.warning(request, "The user already exists.")
            return redirect("djangoapp:registration")

# Update the `get_dealerships` view to render the index page with a list of dealerships
def get_dealerships(request):
    if request.method == "GET":
        context = {}
        url = "https://us-south.functions.appdomain.cloud/api/v1/web/3dc499df-22c6-4250-872c-435c1fbc7775/dealership-package/get-dealership"
        dealerships = get_dealers_from_cf(url)
        context["dealership_list"] = dealerships
        return render(request, 'djangoapp/index.html', context)

# Create a `get_dealer_details` view to render the reviews of a dealer
def get_dealer_details(request, dealer_id):
    if request.method == "GET":
        context = {}
        dealer_url = "https://us-south.functions.appdomain.cloud/api/v1/web/orgg1_djangoserver-space/dealership-package/get-dealership"
        dealer = get_dealer_by_id_from_cf(dealer_url, dealerId= dealer_id)
        context["dealer"] = dealer
    
        review_url = "https://us-south.functions.appdomain.cloud/api/v1/web/3dc499df-22c6-4250-872c-435c1fbc7775/dealership-package/get-review"
        reviews = get_dealer_reviews_from_cf(review_url, dealerId= dealer_id)
        print(reviews)
        context["reviews"] = reviews
        
        return render(request, 'djangoapp/dealer_details.html', context)




# Create a `add_review` view to submit a review
# def add_review(request, dealer_id):
# ...

