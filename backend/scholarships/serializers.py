from rest_framework import serializers
from .models import Scholarship, Application, Bookmark


class ScholarshipSerializer(serializers.ModelSerializer):
    class Meta:
        model = Scholarship
        fields = '__all__'
        read_only_fields = ('scraped_at', 'created_at', 'updated_at')


class ApplicationSerializer(serializers.ModelSerializer):
    scholarship = ScholarshipSerializer(read_only=True)
    scholarship_id = serializers.PrimaryKeyRelatedField(
        queryset=Scholarship.objects.filter(is_approved=True, is_active=True),
        source='scholarship',
        write_only=True
    )
    
    class Meta:
        model = Application
        fields = '__all__'
        read_only_fields = ('user', 'created_at', 'updated_at')
    
    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)


class BookmarkSerializer(serializers.ModelSerializer):
    scholarship = ScholarshipSerializer(read_only=True)
    scholarship_id = serializers.PrimaryKeyRelatedField(
        queryset=Scholarship.objects.filter(is_approved=True, is_active=True),
        source='scholarship',
        write_only=True
    )
    
    class Meta:
        model = Bookmark
        fields = '__all__'
        read_only_fields = ('user', 'created_at')
    
    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)

