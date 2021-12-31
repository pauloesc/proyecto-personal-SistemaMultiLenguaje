from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text
import datetime

db = SQLAlchemy()

#***************************************************************************************
#***************************************************************************************

class base_datos_conexion():

    def __init__(self,sql):
        sel_procesado = text( sql )
        consult = db.engine.execute(sel_procesado)

        self.lista = []
        for resultado in consult:
            self.lista.append(resultado)

#***************************************************************************************
#***************************************************************************************

class Usuario(db.Model):
    __tablename__ = 'usuario'
    Usuario_Usuario = db.Column(db.String)
    Usuario_Llave = db.Column(db.String)
    Usuario_Estado = db.Column(db.String, default='si')
    Usuario_Pk = db.Column(db.Integer,primary_key=True)


class UsuarioIdiomas(db.Model):
    __tablename__ = 'usuario_idiomas'
    UsuarioIdiomas_pk_de_usuario = db.Column(db.Integer,db.ForeignKey('usuario.Usuario_Pk', ondelete='CASCADE'))
    UsuarioIdiomas_Idiomas = db.Column(db.Integer,db.ForeignKey('idioma.Idioma_Pk', ondelete='CASCADE'))
    UsuarioIdiomas_Pk = db.Column(db.Integer, primary_key=True)


class CookieUsuario(db.Model):
    __tablename__ = 'cookie_super_user'
    CookieUsuario_Valor_C = db.Column(db.String)
    CookieUsuario_Pk_usuario = db.Column(db.Integer,db.ForeignKey('usuario.Usuario_Pk', ondelete='CASCADE'))
    CookieUsuario_Pk = db.Column(db.Integer, primary_key=True)


class CookieSuperSuperUser(db.Model):
    __tablename__ = 'cookie_super_super_user'
    Valor_C = db.Column(db.String)
    pk_CookieSuperSuperUser = db.Column(db.Integer, primary_key=True)

class Idioma(db.Model):
    __tablename__ = 'idioma'
    Idioma_Idioma = db.Column(db.String)
    Idioma_Pk = db.Column(db.Integer, primary_key=True)

class Tecnologia(db.Model):
    __tablename__ = 'tecnologia'
    Tecnologia = db.Column(db.String)
    Pk_Tecnologia = db.Column(db.Integer, primary_key=True)

class Documento(db.Model):
    __tablename__ = 'documento'
    Documento_Nombre = db.Column(db.String)
    Documento_Tecnologia = db.Column(db.Integer, db.ForeignKey('tecnologia.Pk_Tecnologia', ondelete='CASCADE'))
    Documento_Version = db.Column(db.String)
    Documento_Idioma = db.Column(db.Integer, db.ForeignKey('idioma.Idioma_Pk'))
    Documento_Habilitada = db.Column(db.String, default='no')
    Documento_Pk = db.Column(db.Integer,primary_key=True)

class IndiceHabilitado(db.Model):
    __tablename__ = 'indice_habilitado'
    IndiceHabilitado_pk_de_documento = db.Column(db.Integer, db.ForeignKey('documento.Documento_Pk', ondelete='CASCADE'))
    IndiceHabilitado_Habilitado = db.Column(db.String, default='no')
    IndiceHabilitado_Pk = db.Column(db.Integer,primary_key=True)

class Indice(db.Model):
    __tablename__ = 'indice'
    Indice_pk_de_documento = db.Column(db.Integer, db.ForeignKey('documento.Documento_Pk', ondelete='CASCADE'))
    Indice_Nombre = db.Column(db.String)
    Indice_Numero = db.Column(db.String)
    Indice_Orden = db.Column(db.Integer)
    Indice_Pk = db.Column(db.Integer,primary_key=True)

class Contenido(db.Model):
    __tablename__ = 'contenido'
    Contenido_pk_de_articulo = db.Column(db.Integer, db.ForeignKey('indice.Indice_Pk', ondelete='CASCADE'))
    Contenido_Contenido = db.Column(db.Text)
    Contenido_Orden = db.Column(db.Integer)
    Contenido_Html_Apertura = db.Column(db.Text)
    Contenido_Html_Cierre = db.Column(db.Text)
    Contenido_Asignable = db.Column(db.String)
    Contenido_Pk = db.Column(db.Integer, primary_key=True)

