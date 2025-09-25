from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('reviews/<str:company>', views.show_reviews, name='reviews'),
    path('dashboard/<str:company>', views.show_dashboard, name='dashboard'),
    path('pos_reviews/<str:company>', views.show_positive_reviews, name='pos_reviews'),
    path('neg_reviews/<str:company>', views.show_negative_reviews, name='neg_reviews'),
    path('neu_reviews/<str:company>', views.show_neutral_reviews, name='neu_reviews')
]