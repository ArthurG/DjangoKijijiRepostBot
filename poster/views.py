from django.shortcuts import render
from django.http import HttpResponse

from poster.models import PostableItem
from poster.serializers import PostableItemSerializer
from django.http import Http404
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.parsers import FileUploadParser, MultiPartParser, FormParser, JSONParser
from rest_framework import status

import poster.actions as actions


# Create your views here.
class PostableItemList(generics.ListCreateAPIView):
    """
    List all postabli items
    or create a new postableitem
    """
    queryset = PostableItem.objects.all()
    serializer_class = PostableItemSerializer

class PostableItemDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrive, update or delete a postable item instance
    """
    queryset = PostableItem.objects.all()
    serializer_class = PostableItemSerializer

def post(request, pk):
    item = PostableItem.objects.get(pk=pk)
    try:
        actions.post(item)
    except Exception as e:
        #print(e)
        return HttpResponse(e)
        pass
    return HttpResponse("Success")

def repost(request, pk):
    item = PostableItem.objects.get(pk=pk)
    try:
        actions.delete(item)
        actions.post(item)
    except Exception as e:
        #print(e)
        return HttpResponse(e)
        pass
 
    return HttpResponse("Success")

def delete(request, pk):
    item = PostableItem.objects.get(pk=pk)
    try:
        actions.delete(item)
    except Exception as e:
        #print(e)
        return HttpResponse(e)
        pass
    return HttpResponse("Success")
