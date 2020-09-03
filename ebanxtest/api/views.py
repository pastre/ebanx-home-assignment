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
def onDeposit(event):
	destination = event.get('destination', False)
	if not destination: return malformedRequest()

	amount = event.get('amount', False)
	if not amount: return malformedRequest()

	account = getAccount(destination)
	if not account:
		account = createAccount(destination)

	account.balance += amount
	account.save()

	return code201(json.dumps(account.toDict("destination")))

def onWithdraw(event):

	origin = event.get('origin', False)
	if not origin: return malformedRequest()

	amount = event.get('amount', False)
	if not amount: return malformedRequest()

	account = getAccount(origin)
	if not account: return notFound("0")

	account.balance -= amount
	account.save()
	return code201(json.dumps(account.toDict("origin")))

def malformedRequest(): return HttpResponseBadRequest()

class Event(View) :

	def post(self, request):
		asDict = requestToJson(request)

		event = asDict.get("type", False)
		if not event: return malformedRequest()

		if event == "deposit": return onDeposit(asDict)
		if event == "withdraw": return onWithdraw(asDict)
		
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



