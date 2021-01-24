from flask import Flask, render_template, request, redirect, session
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
import datetime
from flask_pymongo import PyMongo

app = Flask(__name__)

app.config["MONGO_URI"] = "mongodb://localhost:27017/gestion_stock"
mongo = PyMongo(app)

admin1 = mongo.db.admin.find_one_or_404({"_id": 1})
admin2 = mongo.db.admin.find_one_or_404({"_id": 2})
print('---------------------------------------------------')
print('test connexion database  ---- ')
print("admin1 --->  "+ admin1["nom"]+ ' ' + admin1["prenom"])
print("admin2 --->  "+ admin2["nom"]+ ' ' + admin2["prenom"]) 
 
