from rest_framework import serializers
from . import Task
"""
{
    "_id": "59dc9506f9499f00017168d5",
    "subservice": "/",
    "service": "OpenIOT",
    "apikey": "801230BJKL23Y9090DSFL123HJK09H324HV8732",
    "resource": "/iot/d",
    "attributes": [
        {
            "name": "status",
            "type": "Boolean"
        }
    ],
    "lazy": [
        {
            "name": "luminescence",
            "type": "Lumens"
        }
    ],
    "commands": [
        {
            "name": "wheel1",
            "type": "Wheel"
        }
    ],
    "entity_type": "SensorMachine",
    "internal_attributes": [],
    "static_attributes": []
}
"""
class ServiceSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    apikey = serializers.CharField(max_length=256)
    service = serializers.CharField(max_length=256)
    subservice = serializers.CharField(max_length=256)
    resource = serializers.CharField(max_length=256)
    entity_type = serializers.CharField(max_length=256)
    attibute = serializers.CharField(max_length=256)
    lazy = serializers.CharField(max_length=256)
    commands = serializers.CharField(max_length=256)
    internal_attributes = serializers.CharField(max_length=256)
    static_attributes = serializers.CharField(max_length=256)

    def create(self, validated_data):
        return Task(id=None, **validated_data)

    def update(self, instance, validated_data):
        for field, value in validated_data.items():
            setattr(instance, field, value)
        return instance
