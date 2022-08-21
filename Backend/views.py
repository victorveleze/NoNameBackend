import json
from urllib import response
from django.http import JsonResponse
from Backend.Utilities.DataBaseManager import DataBaseManager
from django.views.decorators.csrf import csrf_exempt
# Create your views here.

@csrf_exempt
def login(request):
    jsonData = json.loads(request.body)
    username = jsonData["username"]
    password = jsonData["password"]

    if not username or not password:
        jsonData = { "respose" : "Login failed" }
        return  JsonResponse(jsonData)

    loginSuccess = DataBaseManager().login(username, password)
    response = "Login success" if loginSuccess else "Login failed"
    jsonData = { "respose" : response }
    return JsonResponse(jsonData)

@csrf_exempt
def logout(request):
    print("Logout")

@csrf_exempt
def addUser(request):
    userInfo = json.loads(request.body)
    upsertSuccess = DataBaseManager().insert_user(userInfo)
    
    response = "User added succesfully" if upsertSuccess else "Failed to added user "
    jsonData = { "response" : response }
    return  JsonResponse(jsonData)

