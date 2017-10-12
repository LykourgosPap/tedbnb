from django.contrib.auth.models import AbstractUser, PermissionsMixin
from django.db import models

# Create your models here.
class tedbnbuser(AbstractUser, PermissionsMixin):
    username = models.CharField(max_length=50, null=False, unique=True)
    first_name = models.CharField(max_length=50, null=False)
    last_name = models.CharField(max_length=50, null=False)
    email = models.EmailField(max_length=100, null=False, unique=True)
    password = models.CharField(max_length=50, null=False)
    type = models.IntegerField(null=False)
    is_superuser = models.BooleanField(default=False)
    about = models.TextField(default="", blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    photo = models.ImageField(upload_to='images/users/', null=True, blank=True)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', 'first_name', 'last_name', 'type', 'password']

    def create_superuser(self, username, email, first_name, last_name, password):
        u = self.create_user(username, email, first_name, last_name, password)
        u.type = 1
        u.is_superuser = True
        u.save(using=self._db)

        return u

    def __str__(self):
        return self.username

    def __unicode__(self):
        return '%s' % (self.username)

class tedbnbhouses(models.Model):
    userid = models.ForeignKey(tedbnbuser, on_delete=models.CASCADE)
    persons = models.IntegerField(null=False)
    type = models.CharField(max_length=30, null=False)
    bedrooms = models.IntegerField(null=False)
    bathrooms = models.IntegerField(null=False)
    rules = models.TextField(default="no rules specified")
    description = models.TextField(default="no description available")
    space = models.IntegerField(null=False)
    price = models.IntegerField(null=False)             #price per night
    mindays = models.IntegerField(null=False)           #minimum number of days for reservation
    daysdiscount = models.IntegerField(default=0)       #after this number of dates you get a discount
    discount = models.IntegerField(default=0)           #how much % discount you get
    amenities = models.TextField(default="no amenities")
    lat = models.FloatField()
    lng = models.FloatField()
    availablefrom = models.DateField(null=False)
    availableuntil = models.DateField(null=False)


    def __str__(self):
        return "house %d" %self.id

class tedbnbrent(models.Model):
    userid = models.ForeignKey(tedbnbuser, on_delete=models.SET(-1))
    houseid = models.ForeignKey(tedbnbhouses, on_delete=models.SET(-1))
    rentedfrom = models.DateField(null=False)
    renteduntil = models.DateField(null=False)
    finalprice = models.IntegerField(null=False)

class tedbnbhouseimages(models.Model):
    house = models.ForeignKey(tedbnbhouses, on_delete=models.CASCADE)
    photo = models.ImageField(upload_to='images/houses/', blank=True)


class tedbnbusercomments(models.Model):
    user = models.ForeignKey(tedbnbuser, on_delete=models.SET(-1))
    house = models.ForeignKey(tedbnbhouses, on_delete=models.CASCADE)
    comment = models.TextField(max_length=200)

class tedbnbhousereviews(models.Model):
    house = models.ForeignKey(tedbnbhouses, on_delete=models.CASCADE)
    star = models.IntegerField()
    review = models.TextField(max_length=200, blank=True, null=True)
    user = models.ForeignKey(tedbnbuser, related_name='author', on_delete=models.SET(-1))



