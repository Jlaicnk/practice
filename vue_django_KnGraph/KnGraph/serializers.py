from rest_framework import serializers

class FormDataSerializer(serializers.Serializer):
    entity1 = serializers.CharField(max_length=100, required=False)
    relation = serializers.CharField(max_length=100, required=False)
    entity2 = serializers.CharField(max_length=100, required=False)
    min_l = serializers.IntegerField(min_value=0, required=False)
    max_l = serializers.IntegerField(min_value=0, required=False)
    limit = serializers.IntegerField(min_value=0, required=False)
