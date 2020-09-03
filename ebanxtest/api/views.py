from django.shortcuts import render
from django.views import View
import json

from api.utils import requestToJson,stringToInt
from api.response_wrappers import successRequest, malformedRequest, notFound
from api.model_facade import getAccount, createAccount, getAndCreateAccountIfNeeded, deposit, withdraw, clear_db

class Event(View) :
	def onDeposit(self, event):
		destination = event.get('destination', False)
		if not destination: return malformedRequest()

		amount = event.get('amount', False)
		if not amount: return malformedRequest()

		return successRequest(json.dumps({
			"destination": deposit(destination, amount).toDict()
			}), status = 201)
	def onWithdraw(self, event):
		origin = event.get('origin', False)
		if not origin: return malformedRequest()

		amount = event.get('amount', False)
		if not amount: return malformedRequest()

		success = withdraw(origin, amount)
		if not success: return notFound("0")

		return successRequest(json.dumps({
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

		return successRequest(json.dumps ({
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

		return successRequest(account.balance)


	def get(self, request):
		accountId = request.GET.get("account_id", False)
		if not accountId: return malformedRequest()

		return self.getBalance(accountId)
class Reset(View):
	def post(self, request):
		clear_db()
		return successRequest("OK")



