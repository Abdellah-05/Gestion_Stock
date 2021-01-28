from flask import Flask, render_template, request, redirect, session , url_for
#from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
import datetime
from flask_pymongo import PyMongo   # pip install Flask-PyMongo

app = Flask(__name__)
app.secret_key = 'ELAAROUB DAMOU'

app.config["MONGO_URI"] = "mongodb://localhost:27017/gestion_stock"
mongo = PyMongo(app)

def isEmpty(word):
    if word:
        return False
    return True

def getLastIdProduct():
    coll, d = mongo.db.produit.find(), {}
    for p in coll:
        pass
    d = p
    return int(d["_id"])

def getLastIdAdmin():
    coll, d = mongo.db.admin.find(), {}
    for p in coll:
        pass
    d = p
    return int(d["_id"])



@app.route('/', methods = ['GET'] )
def loginGet():    
    return render_template('login.html')

@app.route('/', methods = ['POST'] )
def loginPost():
    login = request.form['login']
    password = request.form['password']
    admin = mongo.db.admin.find_one({"gmail":login, "password": password})

    #login_user(adminEmail)

    if isEmpty(admin): 
        return redirect('/')
    else :
        
        session["prenom"] = admin["prenom"]
        session["nom"] = admin["nom"]
        session["img"] = admin["img"]
        return redirect('/ourStock')
 
def produitFaibless():
    prods = mongo.db.produit.find()
    faibles = []
    #comment = ''
    for e in prods:
            if int(e['Qte']) <= 50:
                faibles.append(e)
    return faibles

@app.route('/logout', methods = ['GET'] )
def logout():    
    return render_template('login.html')

@app.route('/ourStock', methods = ['GET'] )
def ourStock():
    produits = mongo.db.produit.find()
    admins = mongo.db.admin.find()
    
    if "nom" and "prenom" in session:
        nomAdmin = session["nom"] + " " + session["prenom"]
        imgAdmin = session["img"]
        faibless = produitFaibless()
        nbrNotifications = len(faibless)
    else:
        nomAdmin = "Admin"
    
    return render_template('home.html',imgAdmin = imgAdmin, produits = produits, admins = admins, nomAdmin = nomAdmin, faibless = faibless, nbrNotifications = nbrNotifications)


@app.route('/produit/<int:id>', methods = ['GET'])
def Prod(id) :
    idSelected = int(id)
    if request.method == 'GET':
        prod=mongo.db.produit.find_one({"_id":idSelected})
        nomAdmin = session["nom"] + " " + session["prenom"]
        imgAdmin = session["img"] 
        return render_template("showprod.html",produit=prod, nomAdmin = nomAdmin, imgAdmin = imgAdmin)


#----------------------------------------------------  add produit
@app.route('/addproduit', methods = ['POST'])
def addproduit():

    id  = getLastIdProduct() + 1
    categorie = request.form.get("categorie")
    nomProduit = request.form.get('nomProduit')
    img = request.form.get('img')
    Qte = request.form.get('Qte')
    prix = request.form.get('prix')
    description = request.form.get('description')
    print("------------------------------------------------")
    print(id)
    print(categorie)
    mongo.db.produit.insert_one({
        "_id": id,
        "categorie": categorie,
        "nomProduit": nomProduit,
        "img" : img,
        "Qte": Qte,
        "prix": prix,
        "description" : description
    })

    return redirect('/ourStock')


@app.route('/supProduit/<int:id>', methods = ['POST'])
def delProd(id) :
     if request.method == 'POST':
        idSelected = int(id)
        ID = request.form.get("idpro")
        ID = int(ID)
        if idSelected == ID :
            mongo.db.produit.delete_one({"_id": idSelected})
        return redirect('/ourStock')

@app.route('/editProduit/<int:id>', methods = ['POST'])
def editProd(id) :
    if request.method == 'POST':
        idSelected = int(id)
        ID = request.form.get("id")
        ID = int(ID)
        print(idSelected)
        print(ID)
        if idSelected == ID :
            
            categorie = request.form.get("categorie")
            nomProduit = request.form.get('nomProduit')
            img = request.form.get('img')
            Qte = request.form.get('Qte')
            prix = request.form.get('prix')
            description = request.form.get('description')

            mongo.db.produit.update_one({"_id" : idSelected},
            {
                "$set": {
                    "categorie": categorie,
                    "nomProduit": nomProduit,
                    "img" : img,
                    "Qte": Qte,
                    "prix": prix,
                    "description" : description
                }
            })

            return redirect('/ourStock')
        return redirect('/ourStock')
    

@app.route('/editAdmin/<int:id>', methods = ['POST'])
def editAdmin(id) :
    if request.method == 'POST':
        idSelected = int(id)
        admin = mongo.db.admin.find_one({"_id":idSelected})  #-- access to admin selected data
        emailAdmin = admin["gmail"]                          #-- get admin email
        gmail = request.form.get('gmail')                    #-- get email admin give us
        ID = request.form.get("id")                          #-- get id admin give us
        ID = int(ID)

        if idSelected == ID and gmail == emailAdmin:
            
            nom = request.form.get("nom")
            prenom = request.form.get('prenom')
            password = request.form.get('password')

            mongo.db.admin.update_one({"_id" : idSelected},
            {
                "$set": {
                    "nom": nom,
                    "prenom": prenom,
                    "gmail" : gmail,
                    "password": password                    
                }
            })

            return redirect('/ourStock')
        return redirect('/ourStock')

@app.route('/addAdmin', methods = ['POST'])
def addAdmin():

    id  = getLastIdAdmin() + 1
    nom = request.form.get("nom")
    prenom = request.form.get('prenom')
    gmail = request.form.get('gmail')
    password = request.form.get('password')
    
    mongo.db.admin.insert_one({
        "_id": id,
        "nom": nom,
        "prenom": prenom,
        "gmail" : gmail,
        "password": password
    })

    return redirect('/ourStock')

@app.route('/supAdmin/<int:id>', methods = ['POST'])
def delAdmin(id) :
     if request.method == 'POST':
        idSelected = int(id)
        ID = request.form.get("idadmin")
        password=request.form.get("password")
        ID = int(ID)
        admin = mongo.db.admin.find_one({"_id":idSelected})  #-- access to admin selected data
        passwordAdmin = admin["password"] 
        if idSelected == ID and password == passwordAdmin :
           mongo.db.admin.delete_one({"_id": idSelected})
        return redirect('/ourStock')

@app.route('/statistiques')
def statistique() :
    coll = mongo.db.produit.find()
    categories = []
    nbrExistance = []
    a = """'{"Task":"Hours per Day","""
    b = """'{"Move":"Percentage","""
    for c in coll:
        if c["categorie"] not in categories:
            categories.append(c["categorie"] )
            
    for e in categories:
        nbrExistance.append(mongo.db.produit.find({"categorie":e}).count())

    for i in range(len(categories)):
        b = b +'"'+categories[i]+'":'+str(nbrExistance[i])+','
        a = a +'"'+categories[i]+'":'+str(nbrExistance[i])+',' 
    b=b[:-1]+"}'"
    a=a[:-1]+"}'"    
    nomAdmin = session["nom"] + " " + session["prenom"]
    imgAdmin = session["img"] 
    return render_template("statistique.html", a = a, b = b, nomAdmin = nomAdmin, imgAdmin = imgAdmin)    




if __name__ == "__main__" :
    app.run(debug=True)
