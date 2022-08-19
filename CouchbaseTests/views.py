from django.shortcuts import render
from django.http import HttpResponse
from Backend.Utilities.CouchBD import CouchBD
# Create your views here.

def AddUser(request):
    bd = CouchBD
    
    doc = {
    "type": "tipo",
    "id": 89,
    "callsign": "CBS",
    "iata": None,
    "icao": None,
    "name": "name"
    }

    bd.upsert_document(doc)
    
    return  HttpResponse("Usuario agregado")

