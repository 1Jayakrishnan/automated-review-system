from rest_framework import serializers
from .ml_model import predict_rating
from . models import ReviewModel

class ReviewModelSerialization(serializers.ModelSerializer):
    class Meta:
        model = ReviewModel
        fields = "__all__"
        read_only_fields = ["rating", "added_at", "edited_at"]

    def create(self, validated_data):
        # Predict rating if not provided
        if not validated_data.get("rating"):
            review_text = validated_data.get("body", "") or ""
            validated_data["rating"] = predict_rating(review_text)
        return super().create(validated_data)

