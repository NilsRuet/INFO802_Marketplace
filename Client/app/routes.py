from app import app
from app import soapClient
from app import mangopayClient
from app import graphQLClient
from app.forms import *
from flask import render_template, flash, redirect, session

@app.route("/")
@app.route("/index")
def index():
    products = graphQLClient.getProducts()
    return render_base_template("index.html",
        title="Welcome to the marketplace",
        length=len(products),
        products=[p["node"] for p in products]
    )

@app.route("/balance", methods=['GET','POST'])
def balance():
    if(not session.get("loggedUser", None)):
        return redirect("/login")

    error = None
    cForm = CreditCardForm()
    piForm = PayInForm()

    if(piForm.validate_on_submit()):
        amount = int(piForm.amount.data*100)
        payin = mangopayClient.payin(
            session["loggedUser"]["UserId"],
            session["loggedUser"]["WalletId"],
            session["loggedUser"]["CardId"],
            amount,
        )
        if(not payin):
            error = "an error occured"
        return redirect("/balance")

    if (cForm.validate_on_submit()):
        card = mangopayClient.registerCard(
            session["loggedUser"]["UserId"],
            cForm.cardNumber.data,
            cForm.expiration.data,
            cForm.cvx.data
        )
        if card:
            newUserInfos = graphQLClient.setCard(session["loggedUser"]["UserId"], card["CardId"])
            loggedUserCopy = session["loggedUser"]
            loggedUserCopy["CardId"] = newUserInfos["CardId"]
            session["loggedUser"] = loggedUserCopy
        else:
            error="An error occured."

    return render_base_template("balance.html",
        title="My balance",
        form=cForm,
        payForm=piForm
    )

@app.route("/product/<productId>", methods=['GET','POST'])
def viewProduct(productId):
    product = graphQLClient.getProduct(productId)
    form = BuyProductForm()

    if(form.validate_on_submit()):
        if(not session.get("loggedUser", None)):
            return redirect("/login")
        shippingCost = soapClient.getDeliveryCost(product["Weight"]/1000.0, form.shippingDistance.data)
        session["shippingCost"] = shippingCost*100
        return redirect(f"/product/{productId}/confirm")

    return render_base_template("product.html",
        title="View product - "+product["Name"],
        product = product,
        form = form
    )

@app.route("/product/<productId>/confirm", methods=['GET','POST'])
def buyProduct(productId):
    if(not session.get("loggedUser", None)):
            return redirect("/login")

    form = ConfirmBuyProductForm()
    shippingCost = session.get("shippingCost",0)
    product = graphQLClient.getProduct(productId)
    if(form.validate_on_submit()):
        cost = (shippingCost+product["Price"])
        session.pop("shippingCost",None)
        payement = mangopayClient.transfer(
            session["loggedUser"]["UserId"],
            cost,
            session["loggedUser"]["WalletId"],            
            product["Seller"]["WalletId"]
        )
        if(payement):
            graphQLClient.sellProduct(product["objectId"],session["loggedUser"]["objectId"])
            return redirect("/")

    currentBalance = mangopayClient.getFunds(session["loggedUser"]["WalletId"])
    newBalance = (currentBalance - (shippingCost+product["Price"]))/100.0
    return render_base_template("buy.html",
        title="Buy product - "+product["Name"],
        product = product,
        shippingCost = shippingCost,
        newBalance = newBalance,
        form=form
    )

@app.route("/login", methods=['GET','POST'])
def login():
    error = None
    loginForm = LoginForm()
    if loginForm.validate_on_submit():
        firstName = loginForm.fn.data
        lastName = loginForm.ln.data
        user = graphQLClient.connectUser(firstName, lastName)
        if(user):
            session["loggedUser"] = user
            return redirect("/")
        else:
            error = "Invalid credentials."
    return render_base_template('login.html', title="Log in", form = loginForm, error=error)

@app.route("/signup", methods=['GET','POST'])
def signUp():
    if(session.get("loggedUser", None)):
        return redirect("/login")
    error = None
    signUpForm = SignUpForm()
    if signUpForm.validate_on_submit():
        firstName = signUpForm.fn.data
        lastName = signUpForm.ln.data

        mangoUser = mangopayClient.createBuyer(fn=firstName, ln=lastName, tag="Production user")
        user = graphQLClient.createUser(
            mangoUser["FirstName"],
            mangoUser["LastName"],
            mangoUser["UserId"],
            mangoUser["WalletId"])
        if(user):
            print(user)
            session["loggedUser"] = user
            return redirect("/")
        else:
            error = "An error occured"
    return render_base_template('signup.html', title="Sign up", form = signUpForm, error=error)

@app.route("/createoffer", methods=['GET','POST'])
def createOffer():
    if(not session.get("loggedUser", None)):
        return redirect("/login")
    
    form = SellProductForm()
    if form.validate_on_submit():
        graphQLClient.createProduct(
            form.name.data,
            form.description.data,
            int(form.weight.data*1000),
            int(form.price.data*100),
            session["loggedUser"]["objectId"]
        )
        return redirect("/")

    return render_base_template("sell.html",
        title="Sell product",
        form = form
    )

@app.route("/logout", methods=['GET'])
def logout():
    session.pop("loggedUser", None)
    return redirect("/login")

@app.route("/clearcard", methods=['GET'])
def clearcard():
    if(not session.get("loggedUser", None)):
        return redirect("/login")
    graphQLClient.setCard(session["loggedUser"]["UserId"], None)
    loggedUserCopy = session["loggedUser"]
    loggedUserCopy.pop("CardId", None)
    session["loggedUser"] = loggedUserCopy
    return redirect("/balance")

def render_base_template(page,**content):
    if(session.get("loggedUser", None)):
        funds = mangopayClient.getFunds(session["loggedUser"]["WalletId"])
        content["balance"] = (funds/100.0)
    return render_template(page, **content)