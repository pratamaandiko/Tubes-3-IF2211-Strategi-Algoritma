from django.shortcuts import render

# Create your views here.
from django.shortcuts import render

from django.http.response import JsonResponse
from rest_framework.parsers import JSONParser
from rest_framework import status
import json
from .models import DaftarKata,Pengingat
from .pengelolaPesan import olahPesan

def homeView(request):
    return render(request,'landingPage.html')

def message(request):
    '''
    :param request:
    :return:

    JSON Input:
    {
        "message" : "your_message"
    }

    JSON Output // jika benar
    {
        "status" : "ok/error",
        "header" : "header daripesan / judul return"
        "pesan" : [
            "pesan 1",
            "pesan 2",
            .
            .
            "pesan n"
        ]
    }
    '''
    if request.method=="POST":
        ret = {}
        try:
            print(request.body)
            data = json.loads(request.body.decode('utf-8'))
            isipesan = data["message"]
            ret["status"] = "ok"
            ret.update(olahPesan(isipesan))
            return JsonResponse(ret, status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            ret["status"] = "error"
            ret["header"] = e
            return JsonResponse(ret, status=status.HTTP_403_FORBIDDEN)

def tambahKata(request):
    '''
    input json => {
        "list_kata" : [
            "kata1",
            "kata2",
            .
            .
            "kata.n"
        ]
    }
    '''
    if request.method=="POST":
        try:
            data = json.loads(request.body.decode('utf-8'))
            listKatabaru = data["list_kata"]
            for kata in listKatabaru:
                kataBaru = DaftarKata(kosakata=kata)
                kataBaru.save()
            return JsonResponse({"status" : "ok"}, status=status.HTTP_200_OK)
        except Exception as e:
            print(e)

        return JsonResponse({"status" : "error"}, status=status.HTTP_403_FORBIDDEN)

def mainpage(request):
    return render(request,'main.html')