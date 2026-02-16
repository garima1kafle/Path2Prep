from rest_framework import serializers
from .models import Profile, MajorOption, CountryOption


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = '__all__'
        read_only_fields = ('user', 'created_at', 'updated_at')
    
    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)


class MajorOptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = MajorOption
        fields = ['id', 'name']


class CountryOptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = CountryOption
        fields = ['id', 'name']

