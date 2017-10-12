from django.conf.urls import url, include
from django.conf.urls.static import static
from rest_framework_jwt.views import obtain_jwt_token, refresh_jwt_token, verify_jwt_token

from ted2017 import settings
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
    ReviewCreateApiView,
    ReviewDetailApiView,
    ReviewApiView,
    CommentCreateApiView,
    CommentDetailApiView,
    PhotoCreateApiView,
    PhotoDetailApiView,
    PhotoListApiView,
)

from . import views
from rest_framework import routers

app_name = 'tedbnb'

router = routers.SimpleRouter()
router.register(r'users', UserViewSet)


urlpatterns = [
    url(r'^api/login$', LoginUserView.as_view(), name='LoginApiView'),
    url(r'^api-token-auth/', obtain_jwt_token),
    url(r'^api-token-refresh/', refresh_jwt_token),
    url(r'^api-token-verify/', verify_jwt_token),
    url(r'^api/houses$', HouseListApiView.as_view(), name='HouseListApiView'),
    url(r'^api/houses/create$', HouseCreateApiView.as_view(), name='HouseCreateApiVew'),
    url(r'^api/houses/(?P<pk>\d+)/$', HouseDetailApiView.as_view(), name='HouseDetailApiView'),
    url(r'^api/houses/(?P<pk>\d+)/edit$', HouseUpdateApiView.as_view(), name='HouseUpdateApiView'),
    url(r'^api/houses/(?P<pk>\d+)/delete$', HouseDeleteApiView.as_view(), name='HouseDestroyApiView'),
    url(r'^api/reviews/create$', ReviewCreateApiView.as_view(), name='ReviewsCreateApiView'),
    url(r'^api/reviews$', ReviewApiView.as_view(), name='ReviewsCreateApiView'),
    url(r'^api/reviews/(?P<pk>\d+)/$', ReviewDetailApiView.as_view(), name='ReviewDetailApiView'),
    url(r'^api/comments$', CommentCreateApiView.as_view(), name='commentsCreateApiView'),
    url(r'^api/comments/(?P<pk>\d+)/$', CommentDetailApiView.as_view(), name='commentsDetailApiView'),
    url(r'^api/photos/create$', PhotoCreateApiView.as_view(), name='PhotosCreateApiView'),
    url(r'^api/photos$', PhotoListApiView.as_view(), name='PhotosListApiView'),
    url(r'^api/photos/(?P<pk>\d+)/$', PhotoDetailApiView.as_view(), name='PhotosDetailApiView'),
    url(r'^api/rent$', RentListApiView.as_view(), name='RentListApiView'),
    url(r'^api/rent/create$', RentCreateApiView.as_view(), name='RentCreateApiVew'),
    url(r'^api/', include(router.urls, namespace='api')),
    url(r'^rest-auth/', include('rest_auth.urls')),
    url(r'^$', views.IndexView.as_view(), name='index'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)