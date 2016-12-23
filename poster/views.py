from django.shortcuts import render
from django.http import HttpResponse

from poster.models import PostableItem
from poster.serializers import PostableItemSerializer
from django.http import Http404
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status

import poster.KijijiApi as K_Api
import requests
import json


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

def getAddressMap(address):
    data={'address': address}
    endpoint = 'https://maps.googleapis.com/maps/api/geocode/json'
    resp = requests.get(endpoint,params=data)

    ans = {}
    latlng = json.loads(resp.text)['results'][0]['geometry']['location']

    ans['lat'] = str(latlng['lat'])
    ans['lng'] = str(latlng['lng'])
    postalCode = [item for item in json.loads(resp.text)['results'][0]['address_components'] if "postal_code" in item['types'] ][0]['short_name']
    city = [item for item in json.loads(resp.text)['results'][0]['address_components'] if "locality" in item['types'] ][0]['short_name']
    province = [item for item in json.loads(resp.text)['results'][0]['address_components'] if "administrative_area_level_1" in item['types'] ][0]['short_name']
    ans['postal_code'] = postalCode
    ans['city'] = city
    ans['province'] = province
    return ans


def convertData(item):
    data = {}
    address = getAddressMap(item.address)
    data['postAdForm.geocodeLat']=address['lat']
    data['postAdForm.geocodeLng']=address['lng']
    data['postAdForm.city']=address['city']
    data['postAdForm.province']=address['province']
    data['PostalLat']=address['lat']
    data['PostalLng']=address['lng']
    data['categoryId']=item.categoryId
    data['postAdForm.adType']=item.get_adType_display()
    data['postAdForm.priceType']=item.get_priceType_display()
    data['postAdForm.priceAmount']=str(item.priceAmount)
    attrs = item.attr.all()
    for attr in attrs:
        print(attr)
        data['postAdForm.attributeMap[{}]'.format(attr.key)]=attr.val
    data['postAdForm.title']=item.title
    data['postAdForm.description']=item.description
    data['postAdForm.locationId']=item.locationId
    data['postAdForm.locationLevel0']=item.locationId
    data['postAdForm.postalCode']=address['postal_code']
    data['submitType']='saveAndCheckout'
    data['featuresForm.topAdDuration']="7"

    return data

def post(request, pk):
    item = PostableItem.objects.get(pk=pk)
    data=convertData(item)
    print(data)
    try:
        api = K_Api.KijijiApi()
        print(item.username, item.password)
        api.login(item.username, item.password)
        api.postAdUsingData(data, [])
    except Exception as e:
        #print(e)
        return HttpResponse(e)
        pass


    return HttpResponse("Hi")
def repost(request):
    return HttpResponse("Hi")
def delete(request):
    return HttpResponse("Hi")
