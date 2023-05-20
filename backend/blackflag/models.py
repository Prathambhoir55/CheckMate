from django.db import models
from company.models import *

# Create your models here.

class BlackFlag(models.Model):
    emp = models.ForeignKey(Employee, on_delete=models.SET_NULL, blank=True, null=True)
    image_embeddings = models.CharField(max_length=3000)
    hr = models.ForeignKey(HR, on_delete=models.SET_NULL, blank=True, null = True)


class Reason(models.Model):
    flag = models.ForeignKey(BlackFlag, on_delete= models.CASCADE)
    text = models.CharField(max_length=200, blank=True)
