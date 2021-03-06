from django.db import models

class Account(models.Model):

	balance = models.IntegerField(default=0)

	def toDict(self):
		return {
			"id": str(self.pk),
			"balance": self.balance,
		}