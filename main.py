from flask import Flask, render_template, session, redirect, url_for, flash
from flask_wtf import FlaskForm
from wtforms import (SelectField, SubmitField)
from wtforms.validators import DataRequired
import pandas as pd
from math import ceil


###############################################################################
######### INSTANCIATE FLASK APP ###############################################
###############################################################################

########## SET & CONFIGURE FLASK ######################

app = Flask(__name__)
app.config['SECRET_KEY'] = '.LSDJ#AknYhSCj6KHVqm4nL468SDJ'

###############################################################################
######### DATA LOADING ########################################################
###############################################################################

def data_loading():
    data=pd.read_json('./static/full_data.json')
    return data

def get_info(estado, materia):

    df = data_loading()
    resultado = df.loc[(df['estado'].str.lower()==estado.lower()) & (df['materia'].str.lower()==materia.lower())]
    return resultado



###############################################################################
######### FORMS ###############################################################
###############################################################################

class Consultar(FlaskForm):
    estado = SelectField(
                u'Entidad federativa',
                choices=[
                    ('Campeche', 'Campeche'),
                    ('Chiapas', 'Chiapas'),
                    ('Quintana Roo', 'Quintana Roo'),
                    ('Tabasco', 'Tabasco'),
                    ('Yucatan', 'Yucatán'),
                    ('Federal', 'Federal'),
                    ], 
                #coerce=unicode, 
                option_widget=None, 
                validate_choice=True,
                validators=[DataRequired()],
                )
    materia = SelectField(
                    u'Materia legislativa',
                    choices=[
                        ('Administrativa', 'Administrativa'),
                        ('Agrario', 'Agrario'),
                        ('Agua', 'Agua'),
                        ('Ambiental', 'Ambiental'),
                        ('Civil', 'Civil'),
                        ('Constitucional', 'Constitucional'),
                        ('D. urbano/obras p.', 'D. Urbano y obras p.'),
                        ('Derechos humanos', 'Derechos humanos'),
                        ('Desarrollo economico', 'Desarrollo económico'),
                        ('Fiscal', 'Fiscal'),
                        ('Municipal', 'Municipal'),
                        ('Patrimonio', 'Patrimonio'),
                        ('Planeacion', 'Planeación'),
                        ('Proteccion civil', 'Protección civil'),
                        ('Pueblos indigenas', 'Pueblos indígenas'),
                        ('Transporte', 'Transporte'),
                        ], 
                    #coerce=unicode, 
                    option_widget=None, 
                    validate_choice=True,
                    validators=[DataRequired()],
                    )
    submit = SubmitField('Enviar')


###############################################################################
########### VIEWS FUNCTIONS ###################################################
###############################################################################

### HOME ROUTE ########################################

@app.route('/', methods=['GET', 'POST'])
def home():

    form = Consultar()
    if form.validate_on_submit():
        uinput = [form.estado.data, form.materia.data]
        df = get_info(uinput[0], uinput[1])
        if df.index.any():
            session['uinput'] = uinput
            session['leyes'] = [str(e) for e in list(df.ley.keys())]
            session['data'] = df.to_dict()
            print(session['leyes'])
            return redirect(url_for('resultados'))
        
        else:
            flash('No existe la materia en la entidad seleccionada.', 'warning')
            return redirect(url_for('home'))


    return render_template('home.html', form=form)

@app.route('/resultados', methods=['GET'])
def resultados():
    return render_template('resultados.html')


if __name__ == '__main__':
    app.run(debug=False)

#############################################################
########## CREDITS ##########################################
#############################################################
# icons from:
# <div>Icons made by <a href="https://www.freepik.com" title="Freepik">Freepik</a> from <a href="https://www.flaticon.com/" title="Flaticon">www.flaticon.com</a></div>
