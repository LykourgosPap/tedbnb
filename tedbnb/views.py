from datetime import date, datetime
from django.db.models import Manager, Q
from django.views.generic import TemplateView
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import permissions, viewsets, status
from rest_framework.response import Response
from rest_framework.generics import (
    ListAPIView,
    RetrieveAPIView,
    UpdateAPIView,
    DestroyAPIView,
    CreateAPIView,
    RetrieveUpdateDestroyAPIView,
    ListCreateAPIView,
)

from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from rest_framework.views import APIView

from tedbnb.models import tedbnbuser,tedbnbhouses,tedbnbrent, tedbnbhousereviews, tedbnbhouseimages, tedbnbusercomments
from tedbnb.permissions import IsAccountOwner, IsUserVerified, IsHouseOwner
from tedbnb.serializers import UserSerializer, HouseSerializer, HouseEditSerializer, RentSerializer, UserLoginSerializer, ReviewSerializer, HouseImSerializer, CommentSerializer


class IndexView(TemplateView):
    template_name = 'tedbnb/index.html'



class UserViewSet(viewsets.ModelViewSet):
        lookup_field = 'username'
        queryset = tedbnbuser.objects.all()
        serializer_class = UserSerializer

        def get_permissions(self):

            if self.request.method == 'POST':
                return (permissions.AllowAny(),)

            if self.request.method in permissions.SAFE_METHODS:
                return (permissions.AllowAny(),)


            return (permissions.IsAuthenticated(), IsAccountOwner(),)

        def create(self, request):
            serializer = self.serializer_class(data=request.data)

            if serializer.is_valid():
                tedbnbuser.objects.create_user(**serializer.validated_data)

                return Response(serializer.validated_data, status=status.HTTP_201_CREATED)

            return Response({
                'status': 'Bad request',
                'message': 'Account could not be created with received data.'
            }, status=status.HTTP_400_BAD_REQUEST)


class LoginUserView(APIView):
    permission_classes = [AllowAny]
    serializer_class = UserLoginSerializer

    def post(self, request, *args, **kwargs):
        data = request.data
        serializer = UserLoginSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            new_data = serializer.validated_data
            return Response(new_data, status=HTTP_200_OK)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)


class HouseCreateApiView(CreateAPIView):
    permission_classes = [IsAuthenticated, IsUserVerified]
    queryset = tedbnbhouses.objects.all()
    serializer_class = HouseEditSerializer

    def perform_create(self, serializer):
        print(self.request.user)
        serializer.save(userid=self.request.user)

class HouseListApiView(ListAPIView):
    serializer_class = HouseSerializer
    permission_classes = [AllowAny]
    queryset = tedbnbhouses.objects.all()

    def get_queryset(self):
        user = self.request.user
        return tedbnbhouses.objects.filter(userid=user)

class HouseDetailApiView(RetrieveAPIView):
    queryset = tedbnbhouses.objects.all()
    serializer_class = HouseSerializer
    permission_classes = [AllowAny]

class HouseUpdateApiView(UpdateAPIView):
    permission_classes = [IsHouseOwner]
    queryset = tedbnbhouses.objects.all()
    serializer_class = HouseEditSerializer

class HouseDeleteApiView(DestroyAPIView):
    queryset = tedbnbhouses.objects.all()
    serializer_class = HouseEditSerializer


class RentCreateApiView(CreateAPIView):
    serializer_class = RentSerializer
    permission_classes = [IsAuthenticated]
    queryset = tedbnbrent.objects.all()

class RentListApiView(ListAPIView):
    serializer_class = HouseSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        date_from = self.request.query_params.get('startdate', None)
        date_from = date_from.replace("%27", "'")
        date_until = self.request.query_params.get('enddate', None)
        date_until = date_until.replace("%27", "'")
        start_date = datetime.strptime(date_until, "'%Y-%m-%d'")
        end_date = datetime.strptime(date_from, "'%Y-%m-%d'")
        days = abs((end_date - start_date).days)
        persons = self.request.query_params.get('persons',None)
        lng = self.request.query_params.get('lng', None)
        lat = self.request.query_params.get('lat', None)
        query = "SELECT * from tedbnb_tedbnbhouses h WHERE NOT EXISTS (SELECT * from tedbnb_tedbnbrent WHERE ((rentedfrom BETWEEN %s AND %s) OR (renteduntil BETWEEN %s AND %s)) AND  h.id=id) AND availablefrom<%s AND availableuntil>%s AND persons>=%d AND (lat BETWEEN %f AND %f) AND (lng BETWEEN %f AND %f) AND  %d>=mindays ORDER BY price" %(date_from,date_until,date_from,date_until,date_from,date_until,int(persons),float(lat)-0.2,float(lat)+0.2,float(lng)-0.2,float(lng)+0.2,int(days))
        queryset = tedbnbhouses.objects.raw(query)
        return queryset

class ReviewCreateApiView(ListCreateAPIView):
    permission_classes = [IsAuthenticated, IsUserVerified]
    queryset = tedbnbhousereviews.objects.all()
    serializer_class = ReviewSerializer
    filter_fields = ('house',)


class ReviewDetailApiView(RetrieveUpdateDestroyAPIView):
    permission_classes = [AllowAny]
    queryset = tedbnbhousereviews
    serializer_class = ReviewSerializer


class CommentCreateApiView(ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = tedbnbusercomments.objects.all()
    serializer_class = CommentSerializer
    filter_fields = ('user',)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class CommentDetailApiView(RetrieveUpdateDestroyAPIView):
    permission_classes = [AllowAny]
    queryset = tedbnbusercomments
    serializer_class = CommentSerializer

class PhotoCreateApiView(CreateAPIView):
    permission_classes = [IsAuthenticated, IsHouseOwner]
    queryset = tedbnbhouseimages.objects.all()
    serializer_class = HouseImSerializer
    filter_fields = ('house',)

class PhotoListApiView(ListAPIView):
    permission_classes = [AllowAny]
    queryset = tedbnbhouseimages.objects.all()
    serializer_class = HouseImSerializer
    filter_fields = ('house',)


class PhotoDetailApiView(RetrieveUpdateDestroyAPIView):
    permission_classes = [AllowAny]
    queryset = tedbnbhousereviews
    serializer_class = HouseImSerializer