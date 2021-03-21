from app import app
from zeep import Client
from app import SOAP_URL

def getDeliveryCost(weight, distance):
    try:
        client = Client(SOAP_URL)
        result = client.service.getDeliveryCost(weight, distance)
        return result
    except:
        return 0