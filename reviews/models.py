from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# Create your models here.

class Review(models.Model):
    company = models.CharField(max_length=100, default='X')
    username = models.CharField(max_length=255, default='Anonymous')
    # user = models.ForeignKey(User, on_delete=models.CASCADE)
    review = models.CharField(max_length=512)
    # time = models.DateField(default=timezone.now)
    sentiment = models.CharField(max_length=20, default='')
    feedback1 = models.CharField(max_length=512, default='')
    feedback2 = models.CharField(max_length=512, default='', blank=True, null=True)
    feedback3 = models.CharField(max_length=512, default='', blank=True, null=True)

    def __str__(self):
        return f'{self.user} said, {self.review[:12]}...' 