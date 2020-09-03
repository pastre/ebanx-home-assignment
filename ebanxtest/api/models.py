from django.db import models

class Account(models.Model):

	balance = models.IntegerField(default=0)