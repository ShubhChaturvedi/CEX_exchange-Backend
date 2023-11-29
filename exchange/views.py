from django.shortcuts import render
from django.http import JsonResponse
import json
from django.views.decorators.csrf import csrf_exempt
from auth_cex.models import User
from .models import Exchange, PermissionToSpendViaChild

# Create your views here.
@csrf_exempt
def tokenExchange(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        sendersID = data.get('sendersID')
        ReceiversID = data.get('ReceiversID')
        amount = int(data.get('amount'))
        print(sendersID , " sends money = INR " , amount , " to " , ReceiversID)

        if(sendersID == None or ReceiversID == None or amount == None):
            return JsonResponse({'status': 400 ,'message':'Bad Request'})
        if(sendersID == "" or ReceiversID == "" or amount == ""):
            return JsonResponse({'status': 400 ,'message':'Bad Request'})
        # check the balance of sender

        sender = User.objects.get(email=sendersID)

        if(sender.balance < amount):
            return JsonResponse({'status': 400 ,'message':'Insufficient Balance'})
        
        Receiver = User.objects.get(email=ReceiversID)

        sender.balance = sender.balance - amount

        Receiver.balance = Receiver.balance + amount

        sender.save()
        Receiver.save()

        exchage = Exchange(senders_id=sender, receivers_id=Receiver, amount=amount)

        exchage.save()

    return JsonResponse({
        "status": 200,
        "message": "Successfully Exchanged Tokens",
    })

@csrf_exempt
def givePermissionToChild(request):
    if request.method == "POST":
        data = json.loads(request.body.decode('utf-8'))
        parentID = data.get('parentID')
        childID = data.get('childID')
        amount = data.get('amount')
        print(parentID , " gives permission to " , childID , " to spend INR " , amount)

        if(parentID == None or childID == None or amount == None):
            return JsonResponse({'status': 400 ,'message':'Bad Request'})
        if(parentID == "" or childID == "" or amount == ""):
            return JsonResponse({'status': 400 ,'message':'Bad Request'})
        # check the balance of sender

        parent = User.objects.get(email=parentID)
        
        child = User.objects.get(email=childID)

        permission = PermissionToSpendViaChild(parent_id=parent, child_id=child, amount=amount)

        permission.save()

    return JsonResponse({
        "status": 200,
        "message": "Successfully Gave Permission",
    })

@csrf_exempt
def spendFromParentAccount(request):
    if request.method == "POST":
        data = json.loads(request.body.decode('utf-8'))
        childID = data.get('childID')
        senderID = data.get("senderID")
        amount = data.get('amount')

        if(childID == None or amount == None):
            return JsonResponse({'status': 400 ,'message':'Bad Request'})
        if(childID == "" or amount == ""):
            return JsonResponse({'status': 400 ,'message':'Bad Request'})
        # check the balance of sender

        permission = PermissionToSpendViaChild.objects.get(child_id=childID)

        if(permission==None):
            return JsonResponse({'status': 400 ,'message':'Bad Request'})

        if(permission.amount < amount):
            return JsonResponse({'status': 400 ,'message':'Insufficient Balance'})
        
        if(permission.parent_id.balance < amount):
            return JsonResponse({'status': 400 ,'message':'Insufficient Balance'})
        
        sender = User.objects.get(email = senderID)

        parent = User.objects.get(email=permission.parent_id)

        parent.balance -= parent.balance

        sender.balance += sender.balance

        return JsonResponse({
            "status" : 200,
            "message" : "Money sended from parent account successfully"
        }) 
    

        
