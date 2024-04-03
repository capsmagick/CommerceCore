from rest_framework import serializers

from customer.models import Cart
from customer.models import CartItem
from customer.models import WishList
from customer.models import Review
from customer.models import ReviewImage
from product.models import Variant

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

    def validate(self, attrs):
        product_variant = attrs.get('product_variant')
        quantity = attrs.get('quantity')

        if quantity < 1:
            raise serializers.ValidationError({
                'quantity': 'Quantity must be 1 or above.!'
            })

        if product_variant.stock < quantity:
            raise serializers.ValidationError({
                'product_variant': 'Only have limited stock.!'
            })

        return attrs

    def create(self, validated_data):
        cart = validated_data.pop('cart')
        obj = CartItem.objects.create(cart=cart, **validated_data)
        return obj


class UpdateCartProductSerializer(serializers.Serializer):
    product_variant = serializers.SlugRelatedField(
        slug_field='id',
        queryset=Variant.objects.all(),
        required=True,
    )
    quantity = serializers.IntegerField(min_value=-1, max_value=1)

    def validate(self, attrs):
        product_variant = attrs.get('product_variant')
        quantity = attrs.get('quantity')

        obj = Variant.objects.get(pk=product_variant)

        stock_check = obj.stock + quantity

        if stock_check < 0:
            raise serializers.ValidationError({
                'quantity': 'Only have limited quantity'
            })

        return attrs


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
        from product.serializers import VariantModelSerializerGET
        return VariantModelSerializerGET(attrs.product_variant).data

    class Meta:
        model = WishList
        fields = '__all__'


class ReviewSerializerPOST(serializers.ModelSerializer):
    review_images = serializers.ListField(
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
        review_images = validated_data.pop('review_images', [])
        review = Review.objects.create(**validated_data)

        for image in review_images:
            review.review_image.create(**{
                'file': image,
                'name': image.name
            })

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

