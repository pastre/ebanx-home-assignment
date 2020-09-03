from django.shortcuts import render
from django.views import View
from django.http import HttpResponse, HttpResponseBadRequest

from api.models import Account
import json

def requestToJson(request):
	print("BODY IS", request.body)
	return json.loads(request.body.decode('utf-8'))

def stringToInt(i):
	try: return int(i)
	except ValueError: return False

def createAccount(pk):
	new = Account.objects.create(pk = pk)
	new.save()
	return new

def code201(payload): 
	response = HttpResponse(payload)

	response.statusCode = 201

	return response



def onDeposit(destination, amount):
	account = Account.objects.filter(pk = destination).first()
	if not account:
		account = createAccount(destination)

	account.balance += amount
	account.save()

	return code201(json.dumps(account.toDict()))



def malformedRequest(): return HttpResponseBadRequest()

class Event(View) :

	def sanitizeEvent(self, event):
		minimumKeys = ["destination", "amount"]
		intKeys = ["amount", "balance"]

		for key in minimumKeys: 
			if not key in event.keys(): return False

		for key, value in event.items():
			if key in intKeys:
				number = stringToInt(value)
				if not number: return False
				event[key] = number

		return event


	def post(self, request):
		asDict = requestToJson(request)


		event = asDict.get("type", False)
		print("--->", event)

		if not event: return malformedRequest()

		sanitized = self.sanitizeEvent(asDict)
		if not sanitized: return malformedRequest()

		if event == "deposit": return onDeposit(sanitized["destination"], sanitized["amount"])

		return malformedRequest()



