from flask import *
import jsonpickle

app = Flask(__name__)

configFile = open("config.json",mode="r")
configDict = jsonpickle.decode(configFile.read())
configFile.close()

app.config['SECRET_KEY'] = configDict["flaskEncryptionKey"]
SOAP_URL = configDict["soapWsdlUrl"]
MANGOPAY_CLIENT_ID = configDict["mangopayClientId"]
MANGOPAY_API_KEY = configDict["mangopayApiKey"]
BACK4APP_APP_ID = configDict["back4appAppId"]
BACK4APP_MASTER_KEY = configDict["back4appMasterKey"]
BACK4APP_CLIENT_KEY = configDict["back4appClientKey"]

from app import routes