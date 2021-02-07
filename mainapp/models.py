from django.contrib.auth.models import User
from django.db import models

# Create your models here.

class grocery(models.Model):
    name = models.CharField(max_length=100)
    quantity = models.IntegerField()
    status = models.CharField(max_length=100)
    date = models.DateTimeField(null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name