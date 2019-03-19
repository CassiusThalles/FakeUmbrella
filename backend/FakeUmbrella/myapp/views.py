from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from myapp.models import Company
from myapp.serializers import CompanySerializer
import json, requests

@csrf_exempt
def company_list(request):
    """
    List all Companies in the database with it's columns.
    """

    if request.method == 'GET':
        company = Company.objects.all()
        serializer = CompanySerializer(company, many=True)
        return JsonResponse(serializer.data, safe=False)
    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = CompanySerializer(data=data)
#        if serializer.is_valid():
#            serializer.save()
#            return JsonResponse(serializer.data, status=201)
#        return JsonResponse(serializer.errors, status=400)
        return JsonResponse(serializer, safe=False)

@csrf_exempt
def chartpage(request):
    myquery = Company.objects.values_list('location', 'country_code', 'name', 'num_of_employees')[:4]
    mylist = returndistinctvalue(myquery)
    is_raining = []
    for item in mylist:
        response = consultweatherapiforecast(item[0], item[1])
        is_raining.append((openweatherjsonverify(response, 'Rain')))
    color = []
    for item in is_raining:
        if(item == True):
            color.append('#78A65B')
        else:
            color.append('#BC281D')
    companies = []
    num_of_employees = []
    for item in myquery:
        companies.append(item[2])
        num_of_employees.append(item[3])
    jsonresponse = {'name':companies, 'value':num_of_employees, 'color':color}
    jsonresponse = json.dumps(jsonresponse)
    jsonresponse = json.loads(jsonresponse)
    return JsonResponse(jsonresponse, safe=False)

#@csrf_exempt
#def listpage(request):
#    myquery = Company.objects.values_list('location', 'country_code')
#    mylist = returndistinctvalue(myquery)
#    is_raining = []
#    for item in mylist:
#       response = consultweatherapiforecast(item[0], item[1])
#       is_raining.append([openweatherjsonverify(response, 'Rain'), item])
#    raining_locations = []
#    for item in is_raining:
#        if(item[0] == True):
#            raining_locations.append(item[1])
#        else:
#            continue
#    mylist = []
#    for i in raining_locations:
#        myquery = Company.objects.filter(location=i[0])
#        return HttpResponse(myquery)
#        mylist.append(myquery)
#    response = json.dumps(mylist)
#    response = json.loads(response)
#    return JsonResponse(response, safe=False)
#    return HttpResponse(mylist[2][0].location)

@csrf_exempt
def test(request):
    myquery = Company.objects.values_list('location', 'country_code')
    mylist = returndistinctvalue(myquery)
    is_raining = []
    for item in mylist:
        response = consultweatherapiforecast(item[0], item[1])
        is_raining.append((openweatherjsonverify(response, 'Rain')))

    #return JsonResponse(is_raining, safe=False)
    return HttpResponse(is_raining)

# The functions below will be used to make the code more readable
#I'll be using them in the API endpoints coded above


#This function will deal with the GET request to the OpenWeatherMap API. The api key that I have gives me just 
#two functionalities: Current Weather API and 5 days/3 hour forecast API. So I won't code this function to handle
#all functionalities given by the API, just the 5 days forecast.
def consultweatherapiforecast(city, country_code):
    #define the api key
    apikey = 'Open Weather API Key Here'
    #define the URL of the desired API endpoint
    URL = "https://api.openweathermap.org/data/2.5/forecast/?q={},{}&units=metrics&appid={}".format(city, country_code, apikey)
    #consume the OpenWeatherMap API using the GET request
    response = requests.get(URL)
    #return the result as a json
    return response.json()

#To this project I'll need to verify if a given location will have rain in the next 5 days
#So I'll use this function to run through the API response to check if the weather will have a given weather.
def openweatherjsonverify(jsonobj, weather):
    for items in jsonobj['list']:
        for jsonweather in items['weather']:
            if( jsonweather['main'] == weather):
                return True
    return False

#Because my attempts of getting unique values of 'location' and 'country_code' from the database using Django
#query methods, I'll use this function below to help me with this
def returndistinctvalue(queryresult):
    mylist = []
    for query in queryresult:
        if query in mylist:
            continue
        else:
            mylist.append(query)
    return mylist