from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.contrib.auth.models import User
from django.contrib.auth import logout, login, authenticate
from django.contrib import messages
from datetime import datetime
import json
import logging
from django.views.decorators.csrf import csrf_exempt
from .models import CarMake, CarModel # Імпортуємо твої нові моделі
from .restapis import get_request, analyze_review_sentiments, post_review # Ці функції знадобляться пізніше

# Отримуємо екземпляр логера
logger = logging.getLogger(__name__)

# --- ФУНКЦІЇ АВТЕНТИФІКАЦІЇ ---

@csrf_exempt
def login_user(request):
    data = json.loads(request.body)
    username = data['userName']
    password = data['password']
    
    user = authenticate(username=username, password=password)
    data = {"userName": username}
    
    if user is not None:
        login(request, user)
        data = {"userName": username, "status": "Authenticated"}
        
    return JsonResponse(data)

def logout_request(request):
    logout(request)
    data = {"userName": ""}
    return JsonResponse(data)

@csrf_exempt
def registration(request):
    data = json.loads(request.body)
    username = data['userName']
    password = data['password']
    first_name = data['firstName']
    last_name = data['lastName']
    email = data['email']
    username_exist = False
    
    try:
        User.objects.get(username=username)
        username_exist = True
    except:
        logger.debug("{} is new user".format(username))

    if not username_exist:
        user = User.objects.create_user(
            username=username, 
            first_name=first_name, 
            last_name=last_name, 
            password=password, 
            email=email
        )
        login(request, user)
        data = {"userName": username, "status": "Authenticated"}
        return JsonResponse(data)
    else:
        data = {"userName": username, "error": "Already Registered"}
        return JsonResponse(data)

# --- ЗАВДАННЯ ПО РОБОТІ З ДИЛЕРАМИ ТА ВІДГУКАМИ ---

# Отримання списку дилерів
def get_dealerships(request, state="All"):
    if state == "All":
        endpoint = "/fetchDealers"
    else:
        endpoint = "/fetchDealers/" + state
    dealerships = get_request(endpoint)
    return JsonResponse({"status": 200, "inventory": dealerships})

# Отримання відгуків про конкретного дилера
def get_dealer_reviews(request, dealer_id):
    if dealer_id:
        endpoint = "/fetchReviews/dealer/" + str(dealer_id)
        reviews = get_request(endpoint)
        for review_detail in reviews:
            response = analyze_review_sentiments(review_detail['review'])
            review_detail['sentiment'] = response['sentiment']
        return JsonResponse({"status": 200, "reviews": reviews})
    else:
        return JsonResponse({"status": 400, "message": "Bad Request"})

# Отримання деталей дилера за його ID
def get_dealer_details(request, dealer_id):
    if dealer_id:
        endpoint = "/fetchDealer/" + str(dealer_id)
        status = get_request(endpoint)
        return JsonResponse({"status": 200, "dealer": status})
    else:
        return JsonResponse({"status": 400, "message": "Bad Request"})

# Додавання відгуку
def add_review(request):
    if not request.user.is_anonymous:
        data = json.loads(request.body)
        try:
            post_review(data)
            return JsonResponse({"status": 200})
        except Exception as e:
            return JsonResponse({"status": 401, "message": "Error in posting review"})
    else:
        return JsonResponse({"status": 403, "message": "Unauthorized"})
        # Функція для отримання списку автомобілів
def get_cars(request):
    count = CarMake.objects.filter().count()
    print(count)
    if(count == 0):
        # Якщо база порожня, додамо кілька тестових записів для перевірки
        initiate()
    
    car_models = CarModel.objects.select_related('car_make')
    cars = []
    for car in car_models:
        cars.append({"CarModel": car.name, "CarMake": car.car_make.name})
    
    return JsonResponse({"CarModels": cars})