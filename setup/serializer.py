from rest_framework import serializers


class ImportSerializer(serializers.Serializer):
    model = serializers.CharField(required=True)
    import_file = serializers.FileField(required=True)




