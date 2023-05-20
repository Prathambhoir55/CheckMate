from django.db import models
from accounts.models import User

# Create your models here.
class HR(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)

class Employee(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    arrival_time = models.TimeField(blank=True, null=True)
    leaving_time = models.TimeField(blank=True, null=True)
    hr = models.ForeignKey(HR, on_delete=models.SET_NULL, blank=True, null = True)
    photo = models.URLField(max_length=500, blank=True)
    aadhar_card = models.URLField(max_length=500, blank=True)
    pan_card = models.URLField(max_length=500, blank = True)
    is_verified = models.BooleanField(blank=True, default=False)

class Flag(models.Model):
    punctuality = models.DecimalField(max_digits=3, decimal_places=1, blank=True, default=0)
    sociability = models.DecimalField(max_digits=3, decimal_places=1, blank=True, default=0)
    rating = models.DecimalField(max_digits=3, decimal_places=1, blank=True, default=0) #avg rating of Reviews
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
