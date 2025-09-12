from django.shortcuts import get_object_or_404
from .serializers import ReviewModelSerialization
from .models import ReviewModel
from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from django.db.models import Avg, Count

# import your ML predictor
from .ml_model import predict_rating


class ReviewAPIView(GenericAPIView):
    """List all reviews or create a new one"""

    def get(self, request):
        # sorting the reviews
        sort_option = request.query_params.get("sort", "newest")
        if sort_option == "oldest":
            reviews = ReviewModel.objects.all().order_by('added_at')
        else:
            reviews = ReviewModel.objects.all().order_by('-added_at')

        serialized_reviews = ReviewModelSerialization(reviews, many=True).data

        # Calculate average rating
        average = reviews.aggregate(avg=Avg('rating'))['avg'] or 0
        average = float(f"{average:.1f}")

        # Total number of ratings
        total_ratings = reviews.count()

        # Breakdown by rating
        breakdown_queryset = (
            reviews.values('rating')
            .annotate(count=Count('id'))
            .order_by('-rating')
        )
        breakdown = [
            {"stars": item['rating'], "count": item['count']}
            for item in breakdown_queryset
        ]

        return Response({
            "average": average,
            "totalRatings": total_ratings,
            "breakdown": breakdown,
            "reviews": serialized_reviews
        }, status=status.HTTP_200_OK)

    def post(self, request):
        # copy request data so we can modify it
        data = request.data.copy()

        # if no rating provided, predict from review text
        if not data.get('rating'):
            # adjust 'your_review' to the name of your field for review text
            review_text = data.get('your_review') or data.get('body', '')
            if review_text:
                data['rating'] = predict_rating(review_text)

        serializer = ReviewModelSerialization(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "status": "success",
                "message": "Your review posted successfully!",
                "data": serializer.data
            }, status=status.HTTP_201_CREATED)

        return Response({
            "status": "failed",
            "message": "Your review failed to post!",
            "error": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)