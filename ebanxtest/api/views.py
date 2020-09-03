from django.shortcuts import render
from django.views import View
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseNotFound

from api.models import Account
import json

def requestToJson(request): return json.loads(request.body.decode('utf-8'))
def stringToInt(i):
	try: return int(i)
	except ValueError: return False

def getAccount(pk): return Account.objects.filter(pk = pk).first()
def createAccount(pk):
	new = Account.objects.create(pk = pk)
	new.save()
	return new
def getAndCreateAccountIfNeeded(pk):
	account = getAccount(pk)
	if not account: account = createAccount(pk)

	return account

def malformedRequest(): return HttpResponseBadRequest()
def notFound(payload): return HttpResponseNotFound(payload)

def deposit(accountId, amount):
	account = getAndCreateAccountIfNeeded(accountId)
	account.balance += amount
	account.save()

	return account
def withdraw(accountId, amount):
	account = getAccount(accountId)
	if not account: return False

	account.balance -= amount
	account.save()

	return account



class Event(View) :
	def onDeposit(self, event):
		destination = event.get('destination', False)
		if not destination: return malformedRequest()

		amount = event.get('amount', False)
		if not amount: return malformedRequest()

		return HttpResponse(json.dumps({
			"destination": deposit(destination, amount).toDict()
			}), status = 201)
	def onWithdraw(self, event):
		origin = event.get('origin', False)
		if not origin: return malformedRequest()

		amount = event.get('amount', False)
		if not amount: return malformedRequest()

		success = withdraw(origin, amount)
		if not success: return notFound("0")

		return HttpResponse(json.dumps({
			"origin": success.toDict()
			}), status = 201)
	def onTransfer(self, event):
		originId = event.get('origin', False)
		if not originId: return malformedRequest()

		destinationId = event.get('destination', False)
		if not destinationId: return malformedRequest()

		amount = event.get('amount', False)
		if not amount: return malformedRequest()

		originAccount = withdraw(originId, amount)
		if not originAccount: return notFound('0')

		destinationAccount = deposit(destinationId, amount)

		return HttpResponse(json.dumps ({
			"origin": originAccount.toDict(),
			"destination": destinationAccount.toDict(),
			}), status = 201)

	def post(self, request):
		asDict = requestToJson(request)

		event = asDict.get("type", False)
		if not event: return malformedRequest()

		if event == "deposit": return self.onDeposit(asDict)
		if event == "withdraw": return self.onWithdraw(asDict)
		if event == "transfer": return self.onTransfer(asDict)

		return malformedRequest()
class Balance(View):
	def getBalance(self, pk):
		account = getAccount(pk)
		if not account: return notFound('0')

		return HttpResponse(account.balance)


	def get(self, request):
		accountId = request.GET.get("account_id", False)
		if not accountId: return malformedRequest()

		return self.getBalance(accountId)
class Reset(View):

	def clear_db(self): Account.objects.all().delete()

	def post(self, request):
		self.clear_db()
		return HttpResponse("OK")



