from django.conf.urls import url

from . import views

app_name='poster'
urlpatterns = [
        url(r'^$', views.PostableItemList.as_view()) ,
        url(r'^(?P<pk>[0-9]+)/$', views.PostableItemDetail.as_view()) ,
        url(r'^(?P<pk>[0-9]+)/post$', views.post) ,
        url(r'^(?P<pk>[0-9]+)/repost$', views.repost) ,
        url(r'^(?P<pk>[0-9]+)/delete$', views.delete) ,
        ]
