from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from mysite.models import Customer
from mysite.serializers import CustomerSerializer
import json, requests


# Create your views here.
def index(request):
    """
    List all Customers in the database with it's columns.
    """

    if request.method == 'GET':
        customer = Customer.objects.all()
        serializer = CustomerSerializer(customer, many=True)
        return JsonResponse(serializer.data, safe=False)
    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = CustomerSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)

def chartpage(requests):
    myquery = Customer.objects.values_list('location', 'country_code', 'name', 'employees')[:4]
    responselist = []
    name = []
    employees = []
    colors = []
    for item in myquery:
        name.append(item[2])
        employees.append(item[3])
        response = consultApi(item[0], item[1])
        count = 0
        for i in response['list']:
            count += 1
            if(i['weather'][0]['main'] == 'Rain'):
                #responselist.append({'name':item[2], 'employees':item[3], 'color':'rgba(120, 166, 91, 0.6)'})
                colors.append('rgba(120, 166, 91, 0.6)')
                break
            if(count == len(response['list'])):
                #responselist.append({'name':item[2], 'employees':item[3], 'color':'rgba(188, 40, 29, 0.6)'})
                colors.append('rgba(188, 40, 29, 0.6)')
    responselist.append({'labels': name, 'datasets': {'label':'Number of Employees','data': employees, 'backgroundColor': colors}})
    return JsonResponse(responselist, safe=False)

def listpage(requests):
    myquery = Customer.objects.values_list('location', 'country_code', 'name', 'contact', 'number')
    responselist = []
    for item in myquery:
        response = consultApi(item[0], item[1])
        for i in response['list']:
            if(i['weather'][0]['main'] == 'Rain'):
                responselist.append({'name':item[2], 'contact':item[3], 'number':item[4], 'expected':i['dt_txt']})
                break
    return JsonResponse(responselist, safe=False)

def openWeatherApiKey():
    return 'ca8e9070d09d4eaf083dd8139131da26'

def consultApi(city, country):
    apikey = openWeatherApiKey()
    response = requests.get('https://api.openweathermap.org/data/2.5/forecast/?q={},{}&units=metrics&appid={}'.format(city, country, apikey))
    return response.json()