from django.conf.urls import url, include

from tedbnb.views import (
    UserViewSet,
    HouseListApiView,
    HouseDetailApiView,
    HouseUpdateApiView,
    HouseDeleteApiView,
    HouseCreateApiView,
    RentCreateApiView,
    RentListApiView,
    LoginUserView,
)

from . import views
from rest_framework import routers

app_name = 'tedbnb'

router = routers.SimpleRouter()
router.register(r'users', UserViewSet)


urlpatterns = [
    url(r'^api/login$', LoginUserView.as_view(), name='LoginApiView'),
    url(r'^api/houses$', HouseListApiView.as_view(), name='HouseListApiView'),
    url(r'^api/houses/create$', HouseCreateApiView.as_view(), name='HouseCreateApiVew'),
    url(r'^api/houses/(?P<pk>\d+)/$', HouseDetailApiView.as_view(), name='HouseDetailApiView'),
    url(r'^api/houses/(?P<pk>\d+)/edit$', HouseUpdateApiView.as_view(), name='HouseUpdateApiView'),
    url(r'^api/houses/(?P<pk>\d+)/delete$', HouseDeleteApiView.as_view(), name='HouseDestroyApiView'),
    url(r'^api/rent$', RentListApiView.as_view(), name='RentListApiView'),
    url(r'^api/rent/create$', RentCreateApiView.as_view(), name='RentCreateApiVew'),
    url(r'^api/', include(router.urls, namespace='api')),
    url(r'^$', views.IndexView.as_view(), name='index'),
]