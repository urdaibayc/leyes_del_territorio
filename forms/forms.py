from flask_wtf import FlaskForm
from wtforms import SubmitField, SelectField, StringField
from wtforms.validators import DataRequired

class ConsultaForm(FlaskForm):
	estado = SelectField(
				'Entidad federativa',
				choices=[
					('','Seleccionar entidad'),
					('cam', 'Campeche'),
					('chp', 'Chiapas'),
					('roo', 'Quintana Roo'),
					('tab', 'Tabasco'),
					('yuc', 'Yucatán'),
					('mex', 'Mexico'),
					], 
				#coerce=unicode, 
				option_widget=None, 
				validate_choice=True,
				validators=[DataRequired()],
				)
	materia = SelectField(
					'Materia legislativa',
					choices=[
						('','Seleccionar materia'),
						('adm', 'Administrativa'),
						('agu', 'Agua'),
						('amb', 'Ambiental'),
						('civ', 'Civil'),
						('con', 'Constitucional'),
						('duo', 'Desarrollo urbano y obras públicas'),
						('dhu', 'Derechos humanos'),
						('dec', 'Desarrollo Económico'),
						('fis', 'Fiscal'),
						('mun', 'Municipal'),
						('pat', 'Patrimonio'),
						('pla', 'Planeación'),
						('pci', 'Protección Civil'),
						('pin', 'Pueblos indígenas'),
						('tra', 'Transporte'),
						], 
					#coerce=unicode, 
					option_widget=None, 
					validate_choice=True,
					validators=[DataRequired()],
					)
	submit = SubmitField('Enviar')


class AddForm(FlaskForm):

	name = StringField('str to add:')
	submit = SubmitField('Add str')


class DelForm(FlaskForm):

	id = IntegerField('Id int to delete:')
	# name = StringField('str to del:')
	submit = SubmitField('Delete Id')
