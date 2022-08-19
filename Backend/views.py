import json
from django.http import HttpResponse
from Backend.Utilities.CouchBD import CouchBD
from django.views.decorators.csrf import csrf_exempt
# Create your views here.

def login(request, username, userpass):
    bd = CouchBD()
    loginSuccess = bd.login(username, userpass)
    if loginSuccess:
        return HttpResponse("Success")

    return  HttpResponse("Failed!")


def AddUser(request, type, id, name):
    bd = CouchBD()
    doc = {
        "type": type,
        "id": id,
        "name": name
    }
    
    bd.upsert_document(doc)
        
    return  HttpResponse("Exito")

@csrf_exempt
def PostR(request):
    if request.method == "POST":
        jsonData = json.loads(request.body)
        print(jsonData['data']['name'])

        return HttpResponse("This is POST")


