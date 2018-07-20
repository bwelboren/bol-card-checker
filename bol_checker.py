# Imports
from bs4 import BeautifulSoup
import json
import requests

# Create BS4 parser to traverse HTML
bolHTML = requests.get('https://www.bol.com/nl/m/cadeaubon/bol-com-cadeaubonnen/index.html').text
soup = BeautifulSoup(bolHTML, 'html.parser')

# Returns a CSRF token to be used with the card checker
def getCSRFToken():
	return soup.find('input', {'class': 'js_giftcard_saldochecker_csrf_token'})['value']

# Checks a card with the card checker
# Returns true when the card is valid, false when it's not
def checkGiftcard(cardNumber):
	foundToken = getCSRFToken()
	requestURL = 'https://www.bol.com/nl/ajax/saldochecker.html?cardnumber={cardNumber}&csrfToken={foundToken}'.format(cardNumber=cardNumber, foundToken=foundToken)
	requestResponse = requests.get(requestURL).text
	requestResponse = json.loads(requestResponse)
	return (requestResponse['success'] == 'true')

# Check the card
if(checkGiftcard('X1234-5678-90123')):
	print('Card is VALID')
else:
	print('Card is not valid')