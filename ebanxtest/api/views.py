from django.shortcuts import render
from django.view import View
import json

def requestToJson(request):
	print("BODY IS", request.body)
	return json.loads(request.body)

def stringToInt(i):
	try: return Int(i)
	except ValueError: return False

def onDeposit(destination, amount):
	pass # TODO


def malformedRequest(): return "TODO"

class Event(View) :

	def sanitizeEvent(event):
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

		event = asDict.get("event", False)
		if not event: return malformedRequest()

		sanitized = sanitizeEvent(event)
		if not sanitized: return malformedRequest()

		if event == "deposit": return onDeposit(sanitized["destination"], sanitized["amount"])




