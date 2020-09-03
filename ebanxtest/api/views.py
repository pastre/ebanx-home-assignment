from django.shortcuts import render
from django.views import View
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseNotFound

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
	response = HttpResponse(payload, status = 201)

	return response

def notFound(payload): return HttpResponseNotFound(payload)
def getAccount(pk): return Account.objects.filter(pk = pk).first()

def getBalance(pk):
	account = getAccount(pk)
	if not account: return notFound('0')

	return HttpResponse(account.balance)
def onDeposit(destination, amount):
	account = getAccount(destination)
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

class Balance(View):
	def get(self, request):
		accountId = request.GET.get("account_id", False)
		if not accountId: return malformedRequest()

		return getBalance(accountId)


class Reset(View):

	def clear_db(self): Account.objects.all().delete()

	def post(self, request):
		self.clear_db()
		return HttpResponse("OK")



