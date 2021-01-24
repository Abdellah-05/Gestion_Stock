from flask import Flask, render_template, request, redirect, session
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


@app.route('/', methods = ['GET'] )
def loginGet():    
    return render_template('login.html')

@app.route('/', methods = ['POST'] )
def loginPost():
    login = request.form['login']
    password = request.form['password']
    admin = mongo.db.admin.find_one({"gmail":login, "password": password})
    #session['administrateur'] = admin["prenom"] + ' ' + admin["nom"]
    #login_user(adminEmail)

    if isEmpty(admin): 
        return redirect('/')
    else :
<<<<<<< HEAD
        
=======
        session["prenom"] = admin["prenom"]
        session["nom"] = admin["nom"]
>>>>>>> d053e8c1926ae7502a59b1b1be70a6772fc535d7
        return redirect('/ourStock')
 

@app.route('/logout', methods = ['GET'] )
def logout():    
    return render_template('login.html')

@app.route('/ourStock', methods = ['GET'] )
def ourStock():
    produits = mongo.db.produit.find()
    admins = mongo.db.admin.find()
<<<<<<< HEAD
    
    #nomAdmin = session['administrateur']
    return render_template('home.html', produits = produits, admins = admins )
=======
    if "nom" and "prenom" in session:
        nomAdmin = session["nom"] + " " + session["prenom"]
    else:
        nomAdmin = "Admin"
    return render_template('home.html', produits = produits, admins = admins, nomAdmin = nomAdmin)
>>>>>>> d053e8c1926ae7502a59b1b1be70a6772fc535d7




if __name__ == "__main__" :
    app.run(debug=True)