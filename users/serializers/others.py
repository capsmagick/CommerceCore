from django.core import exceptions
import django.contrib.auth.password_validation as validators
from rest_framework import serializers
from users.models.other import AddressRegister
from users.models import User


class UserSignupModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'username',
            'password',

            'first_name',
            'last_name',
            'email',
            'mobile_number',
            'date_of_birth',
            'gender',

            'profile_picture',
        )

        extra_kwargs = {'password': {'write_only': True}}

    def validate(self, data):
        # here data has all the fields which have validated values
        # so we can create a User instance out of it
        user = User(**data)

        # get the password from the data
        password = data.get('password')

        errors = dict()
        try:
            # validate the password and catch the exception
            validators.validate_password(password=password, user=user)

        # the exception raised here is different than serializers.ValidationError
        except exceptions.ValidationError as e:
            errors['password'] = list(e.messages)

        if errors:
            raise serializers.ValidationError(errors)

        return super(UserSignupModelSerializer, self).validate(data)

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
            instance.is_customer = True
        instance.save()
        return instance


class UserDataModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'username',

            'first_name',
            'last_name',
            'email',
            'mobile_number',
            'date_of_birth',
            'gender',

            'profile_picture',
            'is_customer',
            'customer_id',
            'is_suspended',

            'is_superuser',
            'store_manager',
        )


class AddressRegisterModelSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField(read_only=True)

    def get_user(self, attrs):
        return UserDataModelSerializer(attrs.user).data

    def create(self, validated_data):
        from setup.middleware.request import CurrentRequestMiddleware
        user = CurrentRequestMiddleware.get_request().user
        obj = AddressRegister.objects.create(**validated_data)
        obj.user = user
        obj.save()
        return obj

    class Meta:
        model = AddressRegister
        exclude = (
            'created_by',
            'created_at',
            'updated_by',
            'updated_at',
            'deleted',
            'deleted_at',
            'deleted_by',
        )


class AddressRegisterModelSerializerGET(serializers.ModelSerializer):
    user = serializers.SerializerMethodField(read_only=True)

    def get_user(self, attrs):
        return UserDataModelSerializer(attrs.user).data

    class Meta:
        model = AddressRegister
        fields = '__all__'


class StoreManagerModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = (
            'username',
            'password',

            'first_name',
            'last_name',
            'email',
            'mobile_number',
            'date_of_birth',

            'profile_picture',
        )

        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
            instance.store_manager = True
        instance.save()
        return instance


class UserModelSerializerGET(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = (
            'password',
        )

