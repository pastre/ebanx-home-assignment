import json
def requestToJson(request): return json.loads(request.body.decode('utf-8'))
def stringToInt(i):
	try: return int(i)
	except ValueError: return False
