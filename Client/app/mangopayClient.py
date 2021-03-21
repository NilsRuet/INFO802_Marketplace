import requests
import base64
import jsonpickle
from app import MANGOPAY_CLIENT_ID,MANGOPAY_API_KEY

clientId = MANGOPAY_CLIENT_ID
apiKEY = MANGOPAY_API_KEY
serverURL = "https://api.sandbox.mangopay.com"
version = "v2.01"
apiBase = serverURL + "/" + version + "/"

headerBytes = base64.b64encode((clientId+":"+apiKEY).encode('ascii'))
authHeader = "Basic "+headerBytes.decode('ascii') 

def getRequest(endPoint, body):
    apiURL = apiBase + endPoint
    response = requests.get(
        apiURL,
        headers={"content-type":"application/json",
                 "Authorization":authHeader},
        data=body
        )
    print("get "+endPoint+": "+str(response))
    if(response.status_code != 200 and response.status_code!=204):
        print(response.__dict__)
    return response

def postRequest(endPoint, body):
    apiURL = apiBase + endPoint
    response = requests.post(
        apiURL,
        headers={"content-type":"application/json",
                 "Authorization":authHeader},
        data=body
        )
    print("post "+endPoint+": "+str(response))
    if(response.status_code != 200 and response.status_code!=204):
        print(response.__dict__)
    return response

def putRequest(endPoint, body):
    apiURL = apiBase + endPoint
    response = requests.put(
        apiURL,
        headers={"content-type":"application/json",
                 "Authorization":authHeader},
        data=body
        )
    print("put "+endPoint+": "+str(response))
    if(response.status_code != 200):
        print(response.__dict__)
    return response

def getDefaultKyc():
    file = open("resources/kycDefault.txt",mode="r")
    kyc = file.read()
    file.close()
    return kyc

class Address:
        def __init__(self,
                    l1="1 rue du Test",
                    l2="",
                    city="Chambéry",
                    reg="Auvergnes-Rhônes-Alpes",
                    pcode="73000",
                    country="FR"):
            self.AddressLine1 = l1
            self.AddressLine2 = l2
            self.City = city
            self.Region = reg
            self.PostalCode = pcode
            self.Country = country

class User:
    def __init__(self,
                fn,
                ln,
                addr = Address(),
                birthday = 0,
                nat = "FR",
                country = "FR",
                email="",
                cap="Normal",
                tag="Test user"):
        if(email==""):
            #Generating placeholder valid email, to make a test user easily
            #visible in mangopay's dashboard
            email=fn.lower().strip()+ln.lower().strip()
            mailList = list(email)
            for i in range(len(mailList)):
                c = mailList[i]
                if(not((c>='a' and c<='z') or (c>='0' and c<='9'))):
                    mailList[i]='a'
            email = ("".join(mailList))+"@gmail.com"

        self.FirstName = fn
        self.LastName = ln
        self.Address = addr
        self.Birthday = birthday
        self.Nationality = nat
        self.CountryOfResidence = country
        self.Email = email
        self.Capacity = cap
        self.Tag = tag

    def createUser(self):
        endPoint = f"/{clientId}/users/natural"
        data = jsonpickle.encode(self, unpicklable=False)
        response = postRequest(endPoint, data)
        if(response.status_code == 200):
            createdUser = jsonpickle.decode(response.content)
            return createdUser
        else:
            return None

class Wallet:
    def __init__(self, owners, desc="Test wallet", curr="EUR", tag="Test wallet"):
        self.Owners = [owners]
        self.Description = desc
        self.Currency = curr
        self.Tag = tag

    def createWallet(self):
        endPoint = f"/{clientId}/wallets"
        data = jsonpickle.encode(self, unpicklable=False)
        response = postRequest(endPoint, data)
        if(response.status_code == 200):
            createdWallet = jsonpickle.decode(response.content)
            return createdWallet
        else:
            return None

class BankAccount:
    def __init__(self,
                ownerName = "Test account owner",
                addr = Address(),
                iban = "FR7611808009101234567890147",
                bic = "CMBRFR2B",
                tag = "Test bank account"):
        self.OwnerName = ownerName
        self.OwnerAddress = addr
        self.IBAN = iban 
        self.BIC = bic 
        self.Tag = tag

    def register(self, userId):
        endPoint = f"/{clientId}/users/{userId}/bankaccounts/iban"
        data = jsonpickle.encode(self, unpicklable=False)
        response = postRequest(endPoint, data)
        if(response.status_code == 200):
            createdAccount = jsonpickle.decode(response.content)
            return createdAccount
        else:
            return None

class KYCDocument:
    def __init__(self, tag = "Test kyc doc", docType = "IDENTITY_PROOF"):
        self.Tag = tag
        self.Type = docType
    
    def createDocument(self, userId):
        endPoint = f"/{clientId}/users/{userId}/kyc/documents/"
        data = jsonpickle.encode(self, unpicklable=False)
        response = postRequest(endPoint, data)
        if(response.status_code == 200):
            createdDoc = jsonpickle.decode(response.content)
            return createdDoc
        else:
            return None
    
    def submit(self, userId, docId, tag = "Test kyc doc", status = "VALIDATION_ASKED"):
        self.Tag = tag
        self.Status = status

        endPoint = f"/{clientId}/users/{userId}/kyc/documents/{docId}"
        data = jsonpickle.encode(self, unpicklable=False)
        response = putRequest(endPoint, data)
        if(response.status_code == 200):
            submittedDoc = jsonpickle.decode(response.content)
            return submittedDoc
        else:
            return None

class KYCPage:
    def __init__(self, file=getDefaultKyc()):
        self.File = file

    def create(self, userId, docId):
        endPoint = f"/{clientId}/users/{userId}/kyc/documents/{docId}/pages"
        data = jsonpickle.encode(self, unpicklable=False)
        response = postRequest(endPoint, data)
        if(response.status_code == 200):
            createdPage = jsonpickle.decode(response.content)
            return createdPage
        else:
            return None

class CardRegistration:
    def __init__(self, userId, curr="EUR", cardType="CB_VISA_MASTERCARD"):
        self.UserId = userId
        self.Currency = curr
        self.CardType = cardType

    def register(self):
        endPoint = f"/{clientId}/CardRegistrations"
        data = jsonpickle.encode(self, unpicklable=False)
        response = postRequest(endPoint, data)
        if(response.status_code == 200):
            createdRegistration = jsonpickle.decode(response.content)
            return createdRegistration
        else:
            return None

    def complete(self, cardRegId, registrationData):
        dataDic = {}
        dataDic["RegistrationData"] = registrationData
        data = jsonpickle.encode(dataDic, unpicklable=False)
        endPoint = f"/{clientId}/CardRegistrations/{cardRegId}"
        response = putRequest(endPoint, data)
        if(response.status_code == 200):
            createdRegistration = jsonpickle.decode(response.content)
            return createdRegistration
        else:
            return None


class Fund:
    def __init__(self, curr, amount):
        self.Currency = curr
        self.Amount = amount

class CardDirectPayin:
    def __init__(self,
                authorId,
                debitedFunds,
                creditedWalletId,
                cardId,
                secureModeURL="http://test.com/",
                secureMode="DEFAULT",
                fees = Fund("EUR",0),
                tag = "Test direct payin",
                statementDesc = "Test"):
        self.AuthorId = authorId
        self.DebitedFunds = debitedFunds
        self.Fees = fees
        self.CreditedWalletId = creditedWalletId
        self.SecureModeReturnURL = secureModeURL
        self.CardID = cardId
        self.Tag = tag
        self.StatementDescriptor = statementDesc

    def apply(self):
        endPoint = f"/{clientId}/payins/card/direct"
        data = jsonpickle.encode(self, unpicklable=False)
        response = postRequest(endPoint, data)
        if(response.status_code == 200):
            payIn = jsonpickle.decode(response.content)
            return payIn
        else:
            return None


class Transfer():
    def __init__(self,
                authorId,
                debitedFund,
                debitedWalletId,
                creditedWalletId,
                fees=Fund("EUR",0),
                tag="Test transfer"):
        self.AuthorId = authorId
        self.DebitedFunds = debitedFund
        self.Fees = fees
        self.DebitedWalletId = debitedWalletId
        self.CreditedWalletId = creditedWalletId
        self.Tag = tag

    def apply(self):
        endPoint = f"/{clientId}/transfers"
        data = jsonpickle.encode(self, unpicklable=False)
        response = postRequest(endPoint, data)
        if(response.status_code == 200):
            transfer = jsonpickle.decode(response.content)
            return transfer
        else:
            return None

class Payout():
    def __init__(self,
                authorId,
                debitedFunds,
                debitedWalletId,
                bankAccountId,
                fees=Fund("EUR",0),
                bankWireRef="Test payout from mangopay"):
        self.AuthorId = authorId
        self.DebitedFunds = debitedFunds
        self.Fees = fees
        self.DebitedWalletId = debitedWalletId
        self.BankAccountId = bankAccountId
        self.BankWireRef = bankWireRef

def createSeller(fn="Seller", ln="Test", tag="Create seller test"):
    sellerReq = User(fn, ln, tag=tag)
    seller = sellerReq.createUser()
    if(seller != None):
        sellerWalletReq = Wallet(seller["Id"], tag=tag)
        sellerWallet = sellerWalletReq.createWallet()
        
        # Seller specific stuff
        bankReq = BankAccount(ownerName = seller["FirstName"]+" "+seller["LastName"], tag=tag)
        bankReq.register(seller["Id"])
        kycReq = KYCDocument(tag=tag)
        kycDoc = kycReq.createDocument(seller["Id"])
        kycPageReq = KYCPage()
        kycPage = kycPageReq.create(seller["Id"], kycDoc["Id"])
        kycReq.submit(seller["Id"], kycDoc["Id"])

def createBuyer(fn="Buyer", ln="Test", tag="Create buyer test"):
    buyerReq = User(fn, ln, tag=tag)
    buyer = buyerReq.createUser()
    if(buyer != None):
        buyerWalletReq = Wallet(buyer["Id"], tag=tag)
        buyerWallet = buyerWalletReq.createWallet()
        return {
        "UserId":buyer["Id"],
        "WalletId":buyerWallet["Id"],
        "FirstName":fn,
        "LastName":ln
        }
    else:
        return None
    
def getFunds(walletId):
    endPoint = f"/{clientId}/wallets/{walletId}"
    res = getRequest(endPoint, {})
    data = jsonpickle.decode(res.content)["Balance"]["Amount"]
    return data

def registerCard(userId, cardNumber, cardExpiration, cardCvx):
    cardRegistrationReq = CardRegistration(userId)
    cardRegistration = cardRegistrationReq.register()
    preData = cardRegistration["PreregistrationData"]
    accesskey = cardRegistration["AccessKey"]
    registrationUrl = cardRegistration["CardRegistrationURL"]

    data = {
        "data":preData,
        "accessKeyRef":accesskey,
        "cardNumber":cardNumber,
        "cardExpirationDate":cardExpiration,
        "cardCvx":cardCvx
    }

    response = requests.post(registrationUrl,data=data)
    registrationData = response.content.decode('ascii')
    completedCardRegistration = cardRegistrationReq.complete(cardRegistration["Id"],registrationData)
    return completedCardRegistration

def payin(userId, walletId, cardId, amount):
    cardPayinReq = CardDirectPayin(userId, Fund("EUR",amount), walletId, cardId)
    cardPayin = cardPayinReq.apply()
    return cardPayin

def transfer(author, amount, debitedWalletId, creditedWalletId):
    transferReq = Transfer(author, Fund("EUR", amount), debitedWalletId, creditedWalletId)
    transfer = transferReq.apply()
    return transfer