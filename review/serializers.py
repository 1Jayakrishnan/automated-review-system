from rest_framework import serializers
from .ml_model import predict_rating
from . models import ReviewModel
import re

class ReviewModelSerialization(serializers.ModelSerializer):
    class Meta:
        model = ReviewModel
        fields = "__all__"
        read_only_fields = ["rating", "createdAt"]

    def validate_author(self, value):
        value = value.strip()
        if not value:
            raise serializers.ValidationError("Author cannot be empty")
        if len(value) < 2:
            raise serializers.ValidationError("Characters should contain at least 2")
        if len(value) > 50:
            raise serializers.ValidationError("Characters should not exceed 50")
        if not re.fullmatch(r"[A-Za-z ]+", value):
            raise serializers.ValidationError("Only letters and spaces allowed")
        if not re.search(r"[A-Za-z]", value):
            raise serializers.ValidationError("Must have at least one letter")
        if not re.search(r"[aeiouAEIOU]", value):
            raise serializers.ValidationError("Must have at least one English vowel")
        if re.fullmatch(r"^(.)\1+$", value):
            raise serializers.ValidationError("Author looks invalid (repeated characters).")
        return value

    def validate_title(self, value):
        value = value.strip()
        if not value:
            raise serializers.ValidationError("Title can’t be empty")
        if len(value) < 5 or len(value) > 100:
            raise serializers.ValidationError("Title must be 5–100 characters")
        if not re.fullmatch(r"[A-Za-z ]+", value):
            raise serializers.ValidationError("Only letters and spaces allowed")
        if not re.search(r"[A-Za-z]", value):
            raise serializers.ValidationError("Must have at least one letter")
        if not re.search(r"[aeiouAEIOU]", value):
            raise serializers.ValidationError("Must have at least one English vowel")
        if re.fullmatch(r"^(.)\1+$", value):
           raise serializers.ValidationError("Title looks invalid (repeated characters).")
        if value.lower() in ["test", "abcde"]:
            raise serializers.ValidationError("Title too generic/placeholder")
        return value

    def validate_body(self, value):
        value = value.strip()
        if len(value) < 10:
            raise serializers.ValidationError("Body must be at least 10 characters")
        if not re.search(r"[aeiouAEIOU]", value):
            raise serializers.ValidationError("Must have at least one English vowel")
        if not re.fullmatch(r"[A-Za-z0-9 .]+", value):
            raise serializers.ValidationError("Only letters, numbers, spaces and periods allowed")
        if re.fullmatch(r"^(.)\1+$", value):
            raise serializers.ValidationError("Body looks invalid (repeated characters).")
        if value.lower() in ["abcdef", "12345"]:
            raise serializers.ValidationError("Body is placeholder/sequential text")
        return value

    def create(self, validated_data):
        # Predict rating if not provided
        if not validated_data.get("rating"):
            review_text = validated_data.get("body", "") or ""
            validated_data["rating"] = predict_rating(review_text)
        return super().create(validated_data)

