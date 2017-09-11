from django.contrib.auth import update_session_auth_hash

from rest_framework import serializers

from tedbnb.models import tedbnbhouses,tedbnbrent,tedbnbuser

from tedbnb.permissions import (
    IsAccountOwner,
    IsUserVerified,
)

from rest_framework.permissions import (
    IsAdminUser,
    AllowAny,
    IsAuthenticated,
)
class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = tedbnbuser
        fields = ('id', 'email', 'username', 'created_at', 'updated_at',
                  'first_name', 'last_name', 'about', 'type', 'password',)
        read_only_fields = ('created_at', 'updated_at',)
        write_only_fields = ('password',)

        def create(self, instance, validated_data):
            id = validated_data('id')
            email = validated_data('email')
            created_at = validated_data('created_at')
            updated_at = validated_data('updated_at')
            first_name = validated_data('first_name')
            last_name = validated_data('last_name')
            about = validated_data('about')
            type = validated_data('type')
            password = validated_data('password')
            user_obj = tedbnbuser(
                id = id,
                email = email,
                created_at = created_at,
                updated_at = updated_at,
                first_name = first_name,
                last_name = last_name,
                about = about,
                type = type,
            )

            user_obj.setpassword(password)
            user_obj.save()

        def update(self, instance, validated_data):
            instance.username = validated_data.get('username', instance.username)
            instance.save()

            password = validated_data.get('password', None)

            instance.set_password(password)
            instance.save()

            update_session_auth_hash(self.context.get('request'), instance)

            return instance

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
        model = tedbnbhouses
        exclude = ('availablefrom','availableuntil',)
