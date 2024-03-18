from rest_framework import serializers

from customer.models import Cart
from customer.models import CartItem
from customer.models import WishList
from customer.models import Review
from customer.models import ReviewImage
from customer.models import Return

from users.serializers import UserDataModelSerializer


class CartModelSerializer(serializers.ModelSerializer):
    user = UserDataModelSerializer()
    created_by = UserDataModelSerializer()
    updated_by = UserDataModelSerializer()
    deleted_by = UserDataModelSerializer()
    items = serializers.SerializerMethodField()

    def get_items(self, attrs):
        items = attrs.cartitems.all()
        return CartItemModelSerializer(items, many=True).data

    class Meta:
        model = Cart
        fields = '__all__'


class CartItemModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = '__all__'


class AddToCartSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = (
            'product_variant',
            'quantity',
            'price',
        )

    def create(self, validated_data):
        cart = validated_data.pop('cart')
        obj = CartItem.objects.create(cart=cart, **validated_data)
        return obj


class WishListModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = WishList
        fields = (
            'product_variant',
        )

    def create(self, validated_data):
        user = validated_data.pop('user')
        obj = WishList.objects.create(user=user, **validated_data)
        return obj


class WishListGETSerializer(serializers.ModelSerializer):
    user = UserDataModelSerializer()
    product_variant = serializers.SerializerMethodField()

    def get_product_variant(self, attrs):
        from product.models import Variant
        from product.serializers import VariantModelSerializer
        return VariantModelSerializer(Variant.objects.get(id=attrs.product_variant))

    class Meta:
        model = WishList
        fields = '__all__'


class ReviewSerializerPOST(serializers.ModelSerializer):
    review_images = serializers.ListSerializer(
        child=serializers.FileField(max_length=1000000, allow_empty_file=False, use_url=False),
        write_only=True
    )

    class Meta:
        model = Review
        fields = (
            'product',
            'comment',
            'rating',
            'review_images'
        )

    def create(self, validated_data):
        review_images = validated_data.pop('review_images')
        review = Review.objects.create(**validated_data)

        for image in review_images:
            ReviewImage.objects.create(
                reviewe=review, file=image
            )

        return review


class ReviewSerializer(serializers.ModelSerializer):
    created_by = UserDataModelSerializer()
    images = serializers.SerializerMethodField()

    def get_images(self, attrs):
        return ReviewImageSerializer(ReviewImage.objects.filter(review_id=attrs.id), many=True).data

    class Meta:
        model = Review
        fields = '__all__'


class ReviewImageSerializer(serializers.ModelSerializer):

    class Meta:
        model = ReviewImage
        fields = '__all__'


class ReturnModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Return
        fields = (
            'reason',
            'product',
            'purchase_bill',
            'description',
            'refund_method',
        )


class ReturnTrackingUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Return
        fields = (
            'tracking_id',
            'shipping_agent',
        )


class ReturnModelSerializerGET(serializers.ModelSerializer):
    class Meta:
        model = Return
        fields = '__all__'

