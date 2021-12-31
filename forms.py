from wtforms import Form, StringField, validators, SelectField, PasswordField, SubmitField

class SuperUser(Form):
    Usuario = StringField('Usuario',[validators.DataRequired()])
    Llave = PasswordField('Contraseña',[validators.DataRequired()])

class DeleteUser(Form):
    Usuario = SelectField('Usuario')

class ChangeKeyUser(Form):
    Usuario = SelectField('Usuario')
    NuevaLlave = StringField('Llave',[validators.DataRequired('Campo requerido'),validators.Length(min=8)])
    NuevaLlave2 = StringField('Llave', [validators.DataRequired('Campo requerido'),validators.Length(min=8)])

class AdministradoresLogin(Form):
    Usuario = StringField('Usuario',[validators.DataRequired('Campo requerido')])
    Llave = PasswordField('Contraseña',[validators.DataRequired('Campo requerido'),validators.Length(min=8)])

class CargarIdioma(Form):
    Idioma = StringField('Idioma',[validators.DataRequired(),validators.Length(min=2,max=2)])

class Tecnologia(Form):
    Tecnologia = StringField('Tecnologia',[validators.DataRequired()])

class NuevaDocumentacion(Form):
    Nombre = StringField('Nombre',[validators.DataRequired('Campo requerdio')])
    Tecnologia = SelectField('Tecnologia')
    Version = StringField('Version',[validators.DataRequired('Campo requerdio')])
    Idioma = SelectField('Idioma')

class HabilitarDocumentacion(Form):
    Documento = SelectField('Documento')

def es_entero(form, field):

    try:
        int(field.data)
    except:
        raise validators.ValidationError()

class Indice(Form):
    Nombre_tecnologia = SelectField('Nombre de la tecnologia', [validators.DataRequired('Campo requerdio')])