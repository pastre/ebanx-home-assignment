from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseNotFound

def successRequest(payload, status = 200): return HttpResponse(payload, status = status)
def malformedRequest(): return HttpResponseBadRequest()
def notFound(payload): return HttpResponseNotFound(payload)
