from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .models import User

# Create your views here.
@csrf_exempt
def login(request):
    data = json.loads(request.body.decode('utf-8'))
    email = data.get('email')
    password = data.get('password')

    if(email == None or password == None):
        return JsonResponse({'status': 400 ,'message':'Bad Request'})
    if(email == "" or password == ""):
        return JsonResponse({'status': 400 ,'message':'Bad Request'})
    
    try:
        user = User.objects.get(email=email)
    except:
        return JsonResponse({'status': 404 ,'message':'User not found'})
    
    if(user.password != password):
        return JsonResponse({'status': 401 ,'message':'Unauthorized'})
    # django sessions

    request.sessions["login_id"] =  {'name': user.name, 'email': user.email, 'phone': user.phone, 'address': user.address, 'panCard': user.panCard, 'aadharCard': user.aadharCard, 'balance': user.balance}


    return JsonResponse({'status': 200 ,'message':'Successfully Logged In', 'data': {'name': user.name, 'email': user.email, 'phone': user.phone, 'address': user.address, 'panCard': user.panCard, 'aadharCard': user.aadharCard, 'balance': user.balance}})
    

@csrf_exempt
def signup(request):
    print("signup called")
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        name = data.get('name')
        email = data.get('email')
        password = data.get('password')
        phone = data.get('phone')
        address = data.get('address')
        panCard = data.get('panCard')
        aadharCard = data.get('aadharCard')
        balance = 0
        print(name, email, password, phone, address, panCard, aadharCard)

        if(name == None or email == None or password == None or phone == None or address == None or panCard == None or aadharCard == None):
            return JsonResponse({'status': 400 ,'message':'Bad Request'})
        if(name == "" or email == "" or password == "" or phone == "" or address == "" or panCard == "" or aadharCard == ""):
            return JsonResponse({'status': 400 ,'message':'Bad Request'})
        
        if(len(panCard) != 10):
            return JsonResponse({'status': 400 ,'message':'Bad Request'})
        if(len(aadharCard) != 12):
            return JsonResponse({'status': 400 ,'message':'Bad Request'})
        if(len(str(phone)) != 10):
            return JsonResponse({'status': 400 ,'message':'Bad Request'})
        
        user = User(name=name, email=email, password=password, phone=phone, address=address, panCard=panCard, aadharCard=aadharCard, balance=balance)
        user.save()
        print("user saved successfully")
        return JsonResponse({'status': 200 ,'message':'Successfully Signed Up', 'data': {'name': name, 'email': email, 'phone': phone, 'address': address, 'panCard': panCard, 'aadharCard': aadharCard, 'balance': balance}, "Extra Message": "Please Login to continue"})
    else:
        return JsonResponse({'status': 400 ,'message':'Bad Request'})
