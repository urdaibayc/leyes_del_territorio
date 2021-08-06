import os 

from forms import AddForm, DelForm, ConsultaUsuario

from flask import (Flask, redirect, url_for, 
	render_template, session)
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate





###############################################################################
######### INSTANCIATE FLASK APP ###############################################
###############################################################################

########## SET & CONFIGURE FLASK ######################

app = Flask(__name__)
app.config['SECRET_KEY'] = ';LSDJ A;LSDJ'


########## SET & CONFIGURE DB #########################

basedir = os.path.abspath(os.path.dirname(__file__))
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///'+os.path.join(basedir,'db.sqlite3') 
db = SQLAlchemy(app)
Migrate(app,db)


###############################################################################
######### MODELS ##############################################################
###############################################################################

class Estado(db.Model):
	__tablename__ = 'estados'
	
	id = db.Column(db.Text, 
				primary_key = True
				)
	nombre = db.Column(db.Text)
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
	
	id = db.Column(db.Integer, 
				primary_key = True
				)
	prioridad = db.Column(db.Float)
	nombre = db.Column(db.Text)
	publicacion = db.Column(db.Integer)
	reforma = db.Column(db.Integer)
	url = db.Column(db.Text)
	estado_id = db.Column(db.Text,
						db.ForeignKey('estados.id'), 
						nullable=False,
						)
	materias_id = db.Column(db.Text, db.ForeignKey('materias.id'),
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

	id = db.Column(db.Text,
				primary_key = True
				)
	nombre = db.Column(db.Text)
	leyes = db.relationship('leyes', 
							lazy='select',
							backref=db.backref('materias', lazy='joined'),
							)

	def __init__(self, id, nombre):
		self.abr = id
		self.name=nombre

	def __repr__(self):
		return f"abr -> {self.abr} -> {self.name} "


###############################################################################
########### VIEWS FUNCTIONS ###################################################
###############################################################################

### HOME ROUTE ########################################

@app.route("/", methods=["POST", "GET"])
def home():
	
	
	# ---Y ESTO???---

	estado = False
	materia = False

	form = ConsultaUsuario()

	if form.validate_on_submit():
		session['estado'] = form.estado.data
		session['materia'] = form.materia.data
		form.estado.data = ''
		form.materia.data = ''
		return redirect(url_for('user_query', edo=session['estado']))
	return render_template("home.html", form=form)


### CREATE 	USER_QUERY ROUTE ##########################

@app.route("/<user_query>", methods=["GET"])
def search(estado):
	return render_template("search.html")


### CREATE PRIVATE ROUTES #############################
#-----------------------------------------------------#
# a = False

### LOGIN ROUTE #######################################

@app.route("/login")
def login():
	# if a:
	# 	return redirect(url_for("/login/<usr>"))
	# else:
	# 	return redirect(url_for("home"))
	# return redirect(url_for("home"))
	pass 


### ADD ROUTE #######################################

@app.route("/add", methods=['GET','POST'])
def add_estado():
	"""Partiendo de un str, Agrega un estado.
	Args: (str)
	"""
	form = AddForm()

	if form.validate_on_submit():
		str_to_add = form.name.data

		new_string = Estado(id, nombre)
		db.session.add(str_to_add)
		db.session.commit()

		return redirect(url_for('list_estados'))
	return render_template('add.html', form=form)


### LIST STATES ROUTE #######################################

@app.route("/list_ent ", methods=['GET'])
def get_states():
	"""Obtiene los estsdos existentes."""
	estados = Estado.query.all()
	return render_template('list_estados.html', estados=estados)



### DELETE ROUTE #######################################

@app.route("/delete", methods=['GET','POST'])
def del_estado():
	"""Borra un estado mediante una ID."""

	form = DelForm()
	if form.validate_on_submit():
		id = form.id.data
		estado = Estado.query.get(id)
		db.session.delete(estado)
		db.session.commit()
		return redirect(url_for('list_estados'))
	return render_template('delete.html', form=form)
	




######### RUN APP #############################################################

if __name__=="__main__":
	app.run(debug=True)