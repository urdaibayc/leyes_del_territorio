import os 

from forms import AddForm, DeleteForm

from flask import (Flask, redirect, url_for, 
	render_template, session)
from flask_sqlachemy import SQLAlchemy
from flask_migrate import Migrate 






########## SET & CONFIGURE FLASK ######################

app = Flask(__name__)
app.config['SECRET_KEY'] = ';LSDJ A;LSDJ'


########## SET & CONFIGURE DB #########################

basedir = os.path.abspath(os.path.dirname(__file__))
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///'+os.path.join(base_dir,'db.sqlite3') 
db = SQLAlchemy(app)
Migrate(app,db)



######### MODELS ##############################################################

class Estado(db.Model):
	__tablename__ = 'estados'
	
	id = db.Colum(db.Text, 
				primary_key = True
				)
	nombre = db.Colum(db.Text)
	leyes = db.relationship('leyes', 
							lazy='select',
							backref=db.backref('estados', lazy='joined'),
							)

	def __init__(self, id, nombre):
		self.abr = id
		self.name = nombre

	def __repr__(self):
		return f"abr -> {self.abr} -> {self.name} "

class Ley(db.Model):
	__tablename__ = 'leyes'
	
	id = db.Colum(db.Integer, 
				primary_key = True
				)
	prioridad = db.Colum(db.Float)
	nombre = db.Colum(db.Text)
	publicacion = db.Colum(db.Integer)
	reforma = db.Colum(db.Integer)
	url = db.Colum(db.Text)
	estado_id = db.Colum(db.Text,
						db.foreingnKey('estados.id'), 
						nullable=False,
						)
	materias_id = db.Colum(db.Text,
							db.foreingnKey('materias.id'), 
							nullable=False,
							)

	def __init__(self, id, prioridad, nombre, publicacion, reforma, url):
		self.id = id
		self.name = nombre
		self.pri = prioridad
		self.pub = publicacion
		self.ref = reforma
		self.url = url

	def __repr__(self):
		return f" -> {self.id} -> prioridad {self.pri} reforma {self.ref}"


class Materia(db.Model):
	__tablename__ = 'materias'

	id = db.Colum(db.Text,
				primary_key
				)
	nombre = db.Colum(db.Text)
	leyes = db.relationship('leyes', 
							lazy='select'
							backref=db.backref('materias', lazy='joined'),
							)

	def __init__(self, id, nombre):
		self.abr = id
		self.name=nombre

	def __repr__(self):
		return f"abr -> {self.abr} -> {self.name} "



########### VIEWS FUNCTIONS ###################################################


### CREATE HOME ROUTE #################################

@app.route("/", methods=["POST", "GET"])
def home():
	
	estado = False
	materia = False
	form = ConsultaForm()

	if form.validate_on_submit():
		session['estado'] = form.estado.data
		session['materia'] = form.materia.data
		form.estado.data = ''
		form.materia.data = ''
		return redirect(url_for('search', edo=session['estado']))
	return render_template("home.html", form=form)


######### CREATE RESULT ROUTE #########################

@app.route("/<edo>")
def search(edo):
	return render_template("search.html")

######### CREATE PRIVATE ROUTES ###############################################
# a = False

@app.route("/login")
def login():
	# if a:
	# 	return redirect(url_for("/login/<usr>"))
	# else:
	# 	return redirect(url_for("home"))
	# return redirect(url_for("home"))
	pass 

@app.route("/add", methods=['GET','POST'])
def add_str():

	form = AddForm()
	if form.validate_on_submit():
		str_to_add = 





######### RUN APP #############################################################

if __name__=="__main__":
	app.run(debug=True)