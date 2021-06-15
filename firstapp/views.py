from django.shortcuts import render
from django.http import JsonResponse ## For Sending Json Responses
from django.views import View ## Allows our class to act as a view
from .helpers import GetBody
from .models import Todo
from django.core.serializers import serialize
from json import loads


class FirstView(View):
  #since the methods name is "get" it will run on "get" requests
  def get(self, request):
    return JsonResponse({"hello":"world", "method": request.method})

  #since the methods name is "post" it will run on "post" requests
  def post(self, request):
    return JsonResponse({"hello":"world", "method": request.method})

  #since the methods name is "put" it will run on "put" requests
  def put(self, request):
    return JsonResponse({"hello":"world", "method": request.method})

  #since the methods name is "delete" it will run on "delete" requests
  def delete(self, request):
    return JsonResponse({"hello":"world", "method": request.method})

class SecondView(View):
  def get(self, request, param):
    query = request.GET.get("query", "no query") ## Grab query from url query
    return JsonResponse({"param": param, "query": query})

  def post(self, request, param):
    query = request.GET.get("query", "no query")
    return JsonResponse({"param": param, "query": query})

  def put(self, request, param):
    query = request.GET.get("query", "no query")
    return JsonResponse({"param": param, "query": query})

  def delete(self, request, param):
    query = request.GET.get("query", "no query")
    return JsonResponse({"param": param, "query": query})

class ThirdView(View):
  def post(self, request):
    return JsonResponse(GetBody(request))

def HelloWorld(request):
  return JsonResponse({"hello": "world"})

# def index(request):
#   # all = Todo.objects.all()
#   # alljson = serialize("json", all)
#   # final = loads(alljson)
#   # return JsonResponse(final, safe=False)
#   all = loads(serialize("json",Todo.objects.all()))
#   return JsonResponse(all, safe=False)


# def show(request, item):
#   one = loads(serialize("json", Todo.objects.filter(item=item)))
#   return JsonResponse(one, safe=False)

class TodoView(View):
  def get(self, request):
    # Serialize the data into JSON then turn the JSON into a dict
    all = loads(serialize('json', Todo.objects.all()))
    # Send the JSON response
    return JsonResponse(all, safe=False)

  def post(self, request):
    # Turn the body into a dict
    body = loads(request.body.decode("utf-8"))
    #create the new item
    newrecord = Todo.objects.create(item=body['item'])
    # Turn the object to json to dict, put in array to avoid non-iterable error
    data = loads(serialize('json', [newrecord]))
    # send json response with new object
    return JsonResponse(data, safe=False)

class OneTodoView(View):
  def get(self, request, param):
    # Filter and find a single item then serialize the data into JSON then turn the JSON into a dict
    one = loads(serialize("json", Todo.objects.filter(item=param)))
    # Send the JSON response
    return JsonResponse(one, safe=False)

  def put(self, request, param):
    # Turn the body into a dict
    body = loads(request.body.decode("utf-8"))
    # update the item
    Todo.objects.filter(item=param).update(item=body['item'])
    newrecord = Todo.objects.filter(item=param)
    # Turn the object to json to dict, put in array to avoid non-iterable error
    data = loads(serialize('json', newrecord))
    # send json response with updated object
    return JsonResponse(data, safe=False)

  def delete(self, request, param):
    # delete the item, get all remaining records for response
    Todo.objects.filter(item=param).delete()
    newrecord = Todo.objects.all()
    # Turn the results to json to dict, put in array to avoid non-iterable error
    data = loads(serialize('json', newrecord))
    # send json response with updated object
    return JsonResponse(data, safe=False)