from rest_framework import serializers
from .models import User, AcademicInfo, CareerPreferences, ProfileCompletion
from django.contrib.auth.password_validation import validate_password

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])

    class Meta:
        model = User
        fields = ('id','username','email','password','full_name','country','age')

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user

class AcademicSerializer(serializers.ModelSerializer):
    class Meta:
        model = AcademicInfo
        fields = ('education_level','field_of_study','gpa','graduation_year','institution')

class CareerPrefsSerializer(serializers.ModelSerializer):
    class Meta:
        model = CareerPreferences
        fields = ('career_interests','preferred_destinations')

class ProfileCompletionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProfileCompletion
        fields = ('skills','financial_need','career_goals','agreed_to_terms')
