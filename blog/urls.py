from django.urls import path
from .views import *

urlpatterns = [
    path('featured', FeaturedView.as_view()),
    path('category', BlogPostCategoryView.as_view()),
    path('<slug>', BlogPostDetailView.as_view()),
    path('', BlogPostListView.as_view()),
]
