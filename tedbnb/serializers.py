from django.contrib.auth import update_session_auth_hash
from drf_extra_fields.fields import Base64ImageField

from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.serializers import CharField,EmailField
from tedbnb.models import tedbnbhouses,tedbnbrent,tedbnbuser,tedbnbhouseimages,tedbnbhousereviews,tedbnbusercomments
from django.db.models import Q


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=False)
    image = Base64ImageField(required=False)

    class Meta:
        model = tedbnbuser
        fields = ('id', 'email', 'username', 'created_at', 'updated_at',
                  'first_name', 'last_name', 'about', 'type', 'password', 'image')
        read_only_fields = ('created_at', 'updated_at',)
        write_only_fields = ('password',)

        def create(self, validated_data):
            id = validated_data('id')
            email = validated_data('email')
            created_at = validated_data('created_at')
            updated_at = validated_data('updated_at')
            first_name = validated_data('first_name')
            last_name = validated_data('last_name')
            about = validated_data('about')
            type = validated_data('type')
            password = validated_data('password')
            image = validated_data('image')
            user_obj = tedbnbuser(
                id = id,
                email = email,
                created_at = created_at,
                updated_at = updated_at,
                first_name = first_name,
                last_name = last_name,
                about = about,
                type = type,
                photo = image,
            )
            user_obj.setpassword(password)
            user_obj.save()

        def update(self, instance, validated_data):
            instance.username = validated_data.get('username', instance.username)
            instance.save()

            password = validated_data.get('password', None)
            image = validated_data.get('image', None)
            instance.photo = image
            instance.set_password(password)
            instance.save()

            update_session_auth_hash(self.context.get('request'), instance)

            return instance


class UserLoginSerializer(serializers.ModelSerializer):
    token = CharField(allow_blank=True, read_only=True)
    email = EmailField(required=False, allow_blank=True)
    username = CharField(required=False, allow_blank=True)

    class Meta:
        model = tedbnbuser
        fields = [
            'username',
            'email',
            'password',
            'token',
        ]
        extra_kwargs = {"password":
                            {"write_only": True}
                       }

    def validate(self, data):
        email = data.get("email", None)
        username = data.get("username", None)
        password = data.get("password", None)
        print(email, username)

        if (not email) and (not username):
            raise ValidationError("Username or Email is required for logging in.")

        user = tedbnbuser.objects.filter(Q(username=username) | Q(email=email)).distinct()

        if user.exists() and user.count() == 1:
            user_obj = user.first()
        else:
            raise ValidationError("This username/email is not Valid.")

        if user_obj:
            if not user_obj.check_password(password):
                raise ValidationError("Incorrect credentials,please try again.")

        data['token'] = "SOME RANDOM TOKEN"

        return data


class HouseSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True, required=False)

    class Meta:
        model = tedbnbhouses
        fields = '__all__'

class HouseEditSerializer(serializers.ModelSerializer):

    class Meta:
        model = tedbnbhouses
        exclude = ('userid',)

class RentSerializer(serializers.ModelSerializer):

    class Meta:
        model = tedbnbrent
        fields = '__all__'

class ReviewSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(read_only=True, required=False, slug_field='username')

    class Meta:
        model = tedbnbhousereviews
        fields = ('house', 'star', 'review', 'user')
        read_only_fields = ('user',)

class ReviewCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = tedbnbhousereviews
        fields = '__all__'

class CommentSerializer(serializers.ModelSerializer):

    class Meta:
        model = tedbnbusercomments
        fields = '__all__'

class HouseImSerializer(serializers.ModelSerializer):
    image = Base64ImageField(required=False)

    class Meta:
        model = tedbnbhouseimages
        fields = ('house', 'image', 'photo')

    def create(self, validated_data):
        house = validated_data['house']
        if not validated_data['photo']:
            photo = validated_data['image']
        else:
            photo = validated_data['photo']
        houseimage = tedbnbhouseimages(
            house = house,
            photo = photo,
        )
        houseimage.save()
        return houseimage

