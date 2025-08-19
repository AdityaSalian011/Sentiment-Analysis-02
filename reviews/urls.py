from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('reviews/<str:company>', views.show_reviews, name='reviews'),
    path('dashboard/<str:company>', views.show_dashboard, name='dashboard')
]