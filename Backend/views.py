import json
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

    loginSuccess, response = DataBaseManager().login(username, password)
    if loginSuccess: 
        success = "true"
    else:
        success = "false"

    jsonData = {
                "response" : response,
                "data" : {
                   "success" : success
                    }
                }
    
    return JsonResponse(jsonData)

@csrf_exempt
def logout(request):
    print("Logout")

@csrf_exempt
def addUser(request):
    userInfo = json.loads(request.body)
    upsertSuccess = DataBaseManager().insert_user(userInfo)
    
    if upsertSuccess:
        response = "User added succesfully"  
        success = "true"
    else:
        response = "Failed to added user "
        success = "false"


    jsonData = { 
                "response" : response,
                "data" : {
                    "success" : success
                    }
                }

    return  JsonResponse(jsonData)

