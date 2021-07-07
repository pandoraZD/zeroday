from flask import Flask, render_template, request, session, escape, flash, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from werkzeug.security import generate_password_hash, check_password_hash

# configuracion de la app y de la base de datos#
app= Flask(__name__)
Bootstrap(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database/database.db'
db = SQLAlchemy(app)

# sistema de registro mediante formulario 
class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(80), nullable=False)

@app.route("/signup.html", methods=["GET", "POST"])
def signup():
        if request.method == "POST":
            hashed_pw = generate_password_hash(request.form["password"], method="sha256")
            new_user = Users(username=request.form["username"], password=hashed_pw)
            db.session.add(new_user)
            db.session.commit()
            flash("Datos insertados correctamente")
            return redirect (url_for('login.html'))
        return render_template('signup.html')

# inicio de sesion mediante formulario
@app.route("/login.html", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        user = Users.query.filter_by(username=request.form["username"]).first()
        if user and check_password_hash(user.password, request.form["password"]):
            return render_template ('index.html')
           # flash ("Error al iniciar sesion, vuelva a introducir los datos!!")
        return render_template ('login.html')

@app.route("/")
def index():
    return render_template('index.html')
if __name__=="__main__":
    db.create_all()
    app.run(debug=True)