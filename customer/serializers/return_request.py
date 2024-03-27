from rest_framework import serializers

from customer.models import Return

from users.serializers import UserDataModelSerializer
from masterdata.serializers import ReturnReasonModelSerializerGET

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
    reason = ReturnReasonModelSerializerGET()
    product = serializers.SerializerMethodField()
    approved_user = UserDataModelSerializer()
    rejected_user = UserDataModelSerializer()

    def get_product(self, attrs):
        from product.serializers import VariantModelSerializer
        return VariantModelSerializer(attrs.product).data

    class Meta:
        model = Return
        fields = '__all__'


class ReturnApproveModelSerializer(serializers.ModelSerializer):
    approved_comment = serializers.CharField(required=False)

    class Meta:
        model = Return
        fields = (
            'approved_comment',
        )


class ReturnRejectModelSerializer(serializers.ModelSerializer):
    rejected_comment = serializers.CharField(required=True)

    class Meta:
        model = Return
        fields = (
            'rejected_comment',
        )


class UpdateReturnRefundDetailsModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Return
        fields = (
            'refund_tracking_id',
            'refund_shipping_agent',
            'refund_transaction_id',
        )




