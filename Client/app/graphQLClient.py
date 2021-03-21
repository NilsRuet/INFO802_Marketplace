import requests
import jsonpickle
from app import BACK4APP_APP_ID,BACK4APP_MASTER_KEY,BACK4APP_CLIENT_KEY
httpheaders = {
    "Content-type": "application/json",
    "X-Parse-Application-Id": BACK4APP_APP_ID,
    "X-Parse-Master-Key": BACK4APP_MASTER_KEY,
    "X-Parse-Client-Key": BACK4APP_CLIENT_KEY,
}

getProductsQuery = """
query GetProducts
{
    products(where:{Status:{equalTo: "ONSALE"}}){
        count,
        edges{
            node{
              objectId,
              Name,
              Price,
              Seller{
                FirstName
                LastName
                WalletId
              }
            }
        }
    }
}
"""

getProductByIdQuery = """
query getProduce($objectId: ID!)
{
    product(id:$objectId){
        objectId,
        Name,
        Description,
        Price,
        Weight,
        Seller{
            FirstName
            LastName
            UserId
            WalletId            
        }
        Status
    }
}
"""

createProductQuery = """
mutation CreateProduct(
  $Name: String!,
  $Price: Float!,
  $Weight: Float!,
  $Desc: String,
  $Seller: ID!
) {
  createProduct(
    input: {
      fields: {
        Name: $Name,
        Seller: {
          link:$Seller
        }
        Price: $Price,
        Weight: $Weight,
        Description: $Desc,
        Status: "ONSALE"
      }
    }
  ) {
    product {
      objectId
    }
  }
}
"""

sellProductQuery = """
mutation sellProduct(
  $objectId: ID!
  $buyerId: ID!
) {
  updateProduct(
    input: {
      id: $objectId
      fields: {
        Buyer: {
            link: $buyerId
        }
        Status: "SOLD"
      }
    }
  ) {
    product {
      objectId
      Status
    }
  }
}
"""

getUserByIdQuery = """
query FindUserByUserId($UserId: String!)
{
    myUsers(where:{ UserId:{equalTo:$UserId} }){
        count,
        edges{
            node{
                objectId
            }
        }
    }
}
"""

getUserByNameQuery = """
query FindUserByUserId($FirstName: String!, $LastName: String!)
{
    myUsers(where:{AND:{
        FirstName:{ equalTo: $FirstName}
        LastName:{ equalTo: $LastName}
        }}){
        count,
        edges{
            node{
                objectId
                FirstName
                LastName
                WalletId
                UserId
                CardId
            }
        }
    }
}
"""

createUserQuery = """
mutation CreateMyUser(
  $FirstName: String!
  $LastName: String!
  $UserId: String!
  $WalletId: String!
) {
  createMyUser(
    input: {
      fields: {
        FirstName: $FirstName
        LastName: $LastName
        UserId: $UserId
        WalletId: $WalletId
      }
    }
  ) {
    myUser {
      objectId
      FirstName
      LastName
      UserId
      WalletId
      CardId
    }
  }
}
"""

addCreditCardQuery = """
mutation AddCardToUser(
  $objectId: ID!
  $NewCardId: String
) {
  updateMyUser(
    input: {
      id: $objectId
      fields: {
        CardId: $NewCardId
      }
    }
  ) {
    myUser {
      objectId
      updatedAt
      CardId
    }
  }
}
"""

def createUser(firstName, lastName, userId, walletId):
    params = {
        "FirstName": firstName,
        "LastName": lastName,
        "UserId": userId,
        "WalletId": walletId,
    }
    return submitRequest(createUserQuery, params)["data"]["createMyUser"]["myUser"]

def connectUser(firstName, lastName):
    params={"FirstName":firstName, "LastName":lastName}
    response = submitRequest(getUserByNameQuery, params)
    count = response["data"]["myUsers"]["count"]
    if(count>0):
        return response["data"]["myUsers"]["edges"][0]["node"]
    else:
        return None

def setCard(userId, cardId):
    paramsGet = {"UserId": userId}
    matchingUsers = submitRequest(getUserByIdQuery, paramsGet)

    matchingObjectId = matchingUsers["data"]["myUsers"]["edges"][0]["node"]["objectId"]
    params = {"objectId": matchingObjectId, "NewCardId": cardId}
    res = submitRequest(addCreditCardQuery, params)
    if res:
        return res["data"]["updateMyUser"]["myUser"]
    else:
        return None

def clearCard(objectId):
    params = {"objectId": userId}
    return submitRequest(deleteCardQuery, params)

def getProducts():
    params = {}
    res = submitRequest(getProductsQuery, params)["data"]["products"]["edges"]
    return res

def getProduct(productId):
    params = {"objectId":productId}
    return submitRequest(getProductByIdQuery, params)["data"]["product"]

def createProduct(name,desc,weight,price,sellerId):
    params = {
        "Name": name,
        "Price": price,
        "Weight": weight,
        "Desc": desc,
        "Seller": sellerId
    }
    return submitRequest(createProductQuery, params)["data"]["createProduct"]["product"]

def sellProduct(objectId,buyerId):
    params = {
        "objectId": objectId,
        "buyerId": buyerId,
    }
    return submitRequest(sellProductQuery, params)["data"]["updateProduct"]["product"]

def submitRequest(query, params):
    response = requests.post(
        "https://parseapi.back4app.com/graphql",
        headers=httpheaders,
        json={"query": query, "variables": params},
    )
    print("GraphQL query : "+str(response.status_code))
    if response.status_code == 200:
        return jsonpickle.decode(response.content)
    else:
        print(response.__dict__)
        return None
