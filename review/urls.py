from django.urls import path
from . import views

urlpatterns = [
    # path for fetch all reviews and post review
    path('reviews/', views.ReviewAPIView.as_view(), name='review')
]