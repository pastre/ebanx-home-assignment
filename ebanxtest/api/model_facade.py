from api.models import Account

def getAccount(pk): return Account.objects.filter(pk = pk).first()
def createAccount(pk):
	new = Account.objects.create(pk = pk)
	new.save()
	return new
def getAndCreateAccountIfNeeded(pk):
	account = getAccount(pk)
	if not account: account = createAccount(pk)

	return account

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
def clear_db(): Account.objects.all().delete()
