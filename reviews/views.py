from django.shortcuts import render, HttpResponse, redirect
import requests
from .models import Review
from .forms import ReviewForm
import pandas as pd
import os

from django.db.models import Count, Q
# Create your views here.

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

CSV_DIR = os.path.join(BASE_DIR, 'refined_review_ds')

def index(request):
    form = ReviewForm()

    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.save()
    
    return render(request, 'reviews/index.html', {'form':form})

def show_reviews(request, company):
    company_ds = {
        'mamledar-misal': os.path.join(CSV_DIR, 'mamledar-misal.csv'),
        'food-town': os.path.join(CSV_DIR, 'food-town.csv'),
        'hotel-mavlan': os.path.join(CSV_DIR, 'hotel-mavlan.csv'),
        'korum-mall': os.path.join(CSV_DIR, 'korum-mall.csv'),
        'viviana-mall': os.path.join(CSV_DIR, 'viviana-mall.csv'),
        'golds-gym': os.path.join(CSV_DIR, 'golds-gym.csv'),
        'decathlon-sports': os.path.join(CSV_DIR, 'decathlon-sports.csv'),
        'jupyter-hospital': os.path.join(CSV_DIR, 'jupyter-hospital.csv')
    }

    file_path = company_ds.get(company.lower())
    if not file_path:
        return HttpResponse('Company Not Found!', status=404)

    df = pd.read_csv(file_path)
    df.fillna("", inplace=True)

    for _, rows in df.iterrows():
        Review.objects.update_or_create(
            company=company,
            username=rows['name'],
            review=rows['reviews'],
            sentiment=rows['sentiment'],
            feedback1=rows['feedback1'],
            feedback2=rows['feedback2'],
            feedback3=rows['feedback3']
        )

    ## adding new reviews
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        user_review = request.POST.get('review')

        # sending user review to fastapi model server to get sentiment
        user_sentiment = requests.post(
            'http://127.0.0.1:8001/sentiment',
            json={'review':user_review}
        )
        sentiment = user_sentiment.json().get('sentiment', 'Error') 
        
        # sending user review to fastapi model server to get feedback
        user_feedbacks = requests.post(
            'http://127.0.0.1:8001/feedbacks',
            json={'review':user_review}
        )
        f1 = user_feedbacks.json().get('feedback1', 'Error')
        f2 = user_feedbacks.json().get('feedback2', 'Error')
        f3 = user_feedbacks.json().get('feedback3', 'Error')

        if form.is_valid():
            review = form.save(commit=False)
            review.company = company
            review.username = 'You'
            review.sentiment = sentiment
            review.feedback1, review.feedback2, review.feedback3 = f1, f2, f3
            review.save()
            return redirect('reviews', company=company)
    else:
        form = ReviewForm()
    
    entries = Review.objects.filter(company=company).order_by('-id')
    return render(request, 'reviews/show_reviews.html', {'entries':entries, 'form':form, 'company': company})

def show_dashboard(request, company):
    total_reviews = Review.objects.filter(company=company).aggregate(
        pos_reviews = Count('id', filter=Q(sentiment='POSITIVE')),
        neg_reviews = Count('id', filter=Q(sentiment='NEGATIVE')),
        neutral_reviews = Count('id', filter=Q(sentiment='NEUTRAL'))
    )

    return render(request, 'reviews/dashboard.html', {'total_reviews': total_reviews, 'company':company})