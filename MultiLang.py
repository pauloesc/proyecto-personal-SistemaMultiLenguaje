import os

import hashlib
import time

from sqlalchemy import text

from flask import jsonify

from flask import Flask
from flask import render_template
from flask import request
from flask import redirect
from flask import url_for
from flask import flash
from flask import make_response

from config import DevelopmentConfig

from forms import SuperUser
from forms import DeleteUser
from forms import ChangeKeyUser
from forms import AdministradoresLogin
from forms import CargarIdioma
from forms import NuevaDocumentacion
from forms import HabilitarDocumentacion
from forms import Indice as IndiceF
from forms import Tecnologia as TecnologiaF

from models import base_datos_conexion

from models import db
from models import CookieSuperSuperUser
from models import Idioma
from models import Indice as IndiceM
from models import Documento,IndiceHabilitado
from models import Contenido
from models import Tecnologia as TecnologiaM
from models import CookieUsuario
from models import UsuarioIdiomas
from models import Usuario


app = Flask(__name__)
app.config.from_object(DevelopmentConfig)


@app.route('/SuperUser-Login',methods=['GET'])
def superUserGet_Login():

    if 'SessionSSU' in request.cookies:
        #compruebo que sea valida
        compruebo = CookieSuperSuperUser.query.filter_by(Valor_C = request.cookies.get('SessionSSU') ).first()
        if compruebo is not None:
            flash('Ya estas logeado')
            return redirect(url_for('SuperUser_PanelGet'))

    formulario = SuperUser()
    return render_template('SuperUser/superUserLogin.html', form = formulario)


@app.route('/SuperUser-Login',methods=['POST'])
def superUserPost_Login():

    if 'SessionSSU' not in request.cookies:

        formulario = SuperUser(request.form)

        if formulario.validate():

            try:
                usuario_en_sistema = os.environ["MultiLangUser"]
                llave_en_sistema = os.environ["MultiLangLlave"]

            except:
                flash('Error al acceder a la variable')
                return redirect(url_for('superUserGet_Login'))
            else:

                if formulario.Usuario.data == usuario_en_sistema and formulario.Llave.data == llave_en_sistema:

                    componente1 = ""+time.strftime("%H%M%S")+""
                    componente2 = ""+time.strftime("%S")+""
                    componente3 = ""+time.strftime("%M")+""
                    total = componente1 + componente2 + componente3
                    valorDeCookie = (hashlib.md5(total.encode('utf-8')).hexdigest())

                    nueva_cookie_en_db = CookieSuperSuperUser( Valor_C = valorDeCookie )
                    db.session.add(nueva_cookie_en_db)
                    db.session.commit()

                    respuesta = make_response( render_template('SuperUser/superUserPanel.html') )
                    respuesta.set_cookie('SessionSSU',valorDeCookie)

                    return respuesta

                else:
                    flash('Usuario o contraseña no valida')
                    return redirect(url_for('superUserGet_Login'))
        else:
            flash('Datos incompletos u/o incorrectos')
            return redirect(url_for('superUserGet_Login'))


    else:
        return redirect(url_for('superUserGet_Login'))


@app.route('/SuperUser-Panel',methods=['GET'])
def SuperUser_PanelGet():

    if 'SessionSSU' in request.cookies:
        #compruebo que sea valida
        compruebo = CookieSuperSuperUser.query.filter_by(Valor_C = request.cookies.get('SessionSSU') ).first()
        if compruebo is None:
            return redirect(url_for('superUserGet_Login'))
        else:
            return render_template('SuperUser/superUserPanel.html')
    else:
        return redirect(url_for('superUserGet_Login'))


@app.route('/SuperUser-CreateUser',methods=['GET'])
def SuperUserGet_CreateUser():

    if 'SessionSSU' in request.cookies:
        #compruebo que sea valida
        compruebo = CookieSuperSuperUser.query.filter_by(Valor_C = request.cookies.get('SessionSSU') ).first()
        if compruebo is not None:
            
            idiomas_en_el_sistema = Idioma.query.all()
            return render_template('SuperUser/createUser.html', idiomas=idiomas_en_el_sistema)
        
        else:
            return redirect(url_for('superUserGet_Login'))
    else:
        return redirect(url_for('superUserGet_Login'))


@app.route('/SuperUser-CreateUser',methods=['POST'])
def SuperUserPost_CreateUser():

    if 'SessionSSU' in request.cookies:
        #compruebo que sea valida
        compruebo = CookieSuperSuperUser.query.filter_by(Valor_C = request.cookies.get('SessionSSU') ).first()
        if compruebo is not None:


            if  ( request.form.get('Usuario','None') != 'None' ) and ( request.form.get('Llave','None') != 'None' ) and ( request.form.get('Idiomas','None') != 'None' ):

                #compruebo que el usuario no este utilizado
                compruebo = Usuario.query.filter_by(Usuario_Usuario = request.form.get('Usuario','None') ).first()
                if compruebo is None:
                    nuevo_super_user = Usuario( Usuario_Usuario = request.form.get('Usuario','None'),
                                                Usuario_Llave = request.form.get('Llave','None') )

                    db.session.add(nuevo_super_user)
                    db.session.commit()

                    consultaUsuario = Usuario.query.filter_by( Usuario_Usuario = request.form.get('Usuario','None') ).first()

                    lista_idiomas_sabe_usuario = request.form.getlist('Idiomas');

                    for idiomas in lista_idiomas_sabe_usuario:

                        nuevo_idiom_en_usuario = UsuarioIdiomas(    UsuarioIdiomas_pk_de_usuario = consultaUsuario.Usuario_Pk,
                                                                    UsuarioIdiomas_Idiomas = idiomas )

                        db.session.add(nuevo_idiom_en_usuario)
                        db.session.commit()


                    flash('Listo')
                    return redirect(url_for('SuperUser_PanelGet'))

                else:
                    mensaje = 'El usuario {0} ya existe'.format( request.form.get('Usuario','None') )
                    flash(mensaje)
                    return redirect(url_for('SuperUserGet_CreateUser'))

            else:
                flash('El formulario no es valido')
                return redirect(url_for('SuperUserGet_CreateUser'))

        else:
            return redirect(url_for('superUserGet_Login'))

    else:
        return redirect(url_for('superUserGet_Login'))


@app.route('/SuperUser-DeleteUser',methods=['GET'])
def SuperUserGet_DeleteUser():

    if 'SessionSSU' in request.cookies:
        #compruebo que sea valida
        compruebo = CookieSuperSuperUser.query.filter_by(Valor_C = request.cookies.get('SessionSSU') ).first()
        if compruebo is not None:

            # traigo todos los usuario
            consulta = Usuario.query.all()
            lista_usuarios = []
            for i in consulta:
                clave = i.Usuario_Pk
                valor = i.Usuario_Usuario
                formato = (clave, valor)
                lista_usuarios.append(formato)
            formulario = DeleteUser()
            formulario.Usuario.choices = lista_usuarios

            return render_template('SuperUser/deleteUser.html', form=formulario)

        else:
            return redirect(url_for('superUserGet_Login'))
    else:
        return redirect(url_for('superUserGet_Login'))


@app.route('/SuperUser-DeleteUser',methods=['POST'])
def SuperUserPost_DeleteUser():

    if 'SessionSSU' in request.cookies:
        #compruebo que sea valida
        compruebo = CookieSuperSuperUser.query.filter_by(Valor_C = request.cookies.get('SessionSSU') ).first()
        if compruebo is not None:

            formulario = DeleteUser(request.form)

            # traigo todos los usuario
            consulta = Usuario.query.all()
            lista_usuarios = []
            for i in consulta:
                lista_usuarios.append(i.Usuario_Pk)

            try:
                int(formulario.Usuario.data)
            except:
                flash('Datos no validos')
                return redirect(url_for('SuperUserGet_DeleteUser'))

            if int(formulario.Usuario.data) in lista_usuarios:

                eliminar = Usuario.query.filter_by(Usuario_Pk = formulario.Usuario.data).first()
                eliminar.Usuario_Estado = 'no'
                db.session.commit()

                flash('Listo')
                return redirect(url_for('SuperUser_PanelGet'))

            else:
                flash('El formulario no es valido')
                return redirect(url_for('SuperUserGet_DeleteUser'))

        else:
            return redirect(url_for('superUserGet_Login'))

    else:
        return redirect(url_for('superUserGet_Login'))


@app.route('/SuperUser-ChangeKey',methods=['GET'])
def SuperUserGet_ChangeKey():

    if 'SessionSSU' in request.cookies:
        #compruebo que sea valida
        compruebo = CookieSuperSuperUser.query.filter_by(Valor_C = request.cookies.get('SessionSSU') ).first()
        if compruebo is not None:

            formulario = ChangeKeyUser()
            consulta = UsuarioSuperUser.query.all()
            lista_usuarios = []
            for i in consulta:
                clave = i.Pk_UsuarioSuperUser
                valor = i.Usuario
                formato = (clave, valor)
                lista_usuarios.append(formato)
            formulario.Usuario.choices = lista_usuarios
            return render_template('SuperUser/ChangeKeyUser.html', form=formulario)

        else:
            return redirect(url_for('superUserGet_Login'))
    else:
        return redirect(url_for('superUserGet_Login'))


@app.route('/SuperUser-ChangeKey',methods=['POST'])
def SuperUserPost_ChangeKey():

    if 'SessionSSU' in request.cookies:
        #compruebo que sea valida
        compruebo = CookieSuperSuperUser.query.filter_by(Valor_C = request.cookies.get('SessionSSU') ).first()
        if compruebo is not None:

            formulario = ChangeKeyUser(request.form)
            try:
                int(formulario.Usuario.data)
            except:
                return redirect(url_for('SuperUserGet_ChangeKey'))

            if formulario.NuevaLlave.data != formulario.NuevaLlave2.data and len(formulario.NuevaLlave.data) >=8 :
                flash('Las llaves no coinciden o demasioado cortas... minimo 8 caracteres')
                return redirect(url_for('SuperUserGet_ChangeKey'))



            # traigo todos los usuario
            consulta = UsuarioSuperUser.query.all()
            lista_usuarios = []
            for i in consulta:
                lista_usuarios.append(i.Pk_UsuarioSuperUser)

            if int(formulario.Usuario.data) in lista_usuarios:

                usuario = UsuarioSuperUser.query.filter_by(Pk_UsuarioSuperUser=formulario.Usuario.data).first()
                usuario.Llave = formulario.NuevaLlave.data
                db.session.commit()

                flash('Listo')
                return redirect(url_for('SuperUserGet'))

            else:
                flash('Datos invalidos')
                return redirect(url_for('SuperUserGet_ChangeKey'))

        else:
            return redirect(url_for('superUserGet_Login'))

    else:
        return redirect(url_for('superUserGet_Login'))

#---------------------------------------------------------------------------

@app.route('/Administracion-CargarIdioma',methods=['GET'])
def Administracion_CargarIdiomaGet():

    if 'SessionSSU' in request.cookies:
        #compruebo que sea valida
        compruebo = CookieSuperSuperUser.query.filter_by(Valor_C = request.cookies.get('SessionSSU') ).first()
        if compruebo is not None:

            formularioi = CargarIdioma()
            return render_template('Administracion/cargarIdioma.html',form= formularioi)

        else:
            flash('No es valida la cookie')
    else:
        return redirect(url_for('superUserGet_Login'))


@app.route('/Administracion-CargarIdioma',methods=['POST'])
def Administracion_CargarIdiomaPost():

    if 'SessionSSU' in request.cookies:
        #compruebo que sea valida
        compruebo = CookieSuperSuperUser.query.filter_by(Valor_C = request.cookies.get('SessionSSU') ).first()
        if compruebo is not None:

            formularioi = CargarIdioma(request.form)
            if formularioi.validate():

                #Compruebo que no exista el idioma
                idioma = formularioi.Idioma.data
                idioma.lower()
                compruebo = Idioma.query.filter_by(Idioma=idioma).first()
                if compruebo is None:
                    nuevo_idioma = Idioma(Idioma=idioma)
                    db.session.add(nuevo_idioma)
                    db.session.commit()
                    flash('Listo')
                    return redirect(url_for('AdministracionGet'))
                else:
                    msg = 'Ya existe el idioma {}'.format(idioma)
                    flash(msg)
                    return redirect(url_for('AdministracionGet'))


            else:
                flash('El formulario no es valido')
                return redirect(url_for('Administracion_CargarIdiomaGet'))
        else:
            flash('No es valida la cookie')
            return redirect(url_for('superUserGet_Login'))
    else:
        return redirect(url_for('superUserGet_Login'))



@app.route('/Administracion-CargarTecnologia',methods=['GET'])
def Administracion_CargarTecnologiaGet():
    if 'SessionSSU' in request.cookies:
        #compruebo que sea valida
        compruebo = CookieSuperSuperUser.query.filter_by(Valor_C = request.cookies.get('SessionSSU') ).first()
        if compruebo is not None:

            formulario = TecnologiaF()
            return render_template('Administracion/cargarTecnologias.html',form = formulario)

        else:
            flash('No es valida la cookie')
            return redirect(url_for('Administracion_LoginGet'))
    else:
        return redirect(url_for('Administracion_LoginGet'))


@app.route('/Administracion-CargarTecnologia',methods=['POST'])
def Administracion_CargarTecnologiaPost():
    if 'SessionSSU' in request.cookies:
        #compruebo que sea valida
        compruebo = CookieSuperSuperUser.query.filter_by(Valor_C = request.cookies.get('SessionSSU') ).first()
        if compruebo is not None:

            formulario = TecnologiaF(request.form)

            if formulario.validate():

                #compruebo que no exista
                compruebo2 = TecnologiaM.query.filter_by(Tecnologia = formulario.Tecnologia.data).first()
                if compruebo2 is None:

                    nueva_tecno = TecnologiaM(Tecnologia = formulario.Tecnologia.data)
                    db.session.add(nueva_tecno)
                    db.session.commit()

                    flash('Listo')
                    return redirect(url_for('AdministracionGet'))

                else:
                    flash('Ya existe lo que quieres caergar')
                    return redirect(url_for('AdministracionGet'))

            else:
                flash('El formulario no es valido')
                return redirect(url_for('Administracion_CargarTecnologiaGet'))

        else:
            flash('No es valida la cookie')
            return redirect(url_for('superUserGet_Login'))
    else:
        return redirect(url_for('superUserGet_Login'))


@app.route('/Administracion-CrearDocumento',methods=['GET'])
def Administracion_CrearDocumentoGet():

    if 'SessionSSU' in request.cookies:
        #compruebo que sea valida
        compruebo = CookieSuperSuperUser.query.filter_by(Valor_C = request.cookies.get('SessionSSU') ).first()
        if compruebo is not None:

            formulario = NuevaDocumentacion()

            consulta = TecnologiaM.query.all()
            lista_De_Tecnologias = []
            for tec in consulta:
                lista_De_Tecnologias.append((tec.Pk_Tecnologia, tec.Tecnologia))
            formulario.Tecnologia.choices = lista_De_Tecnologias

            consulta2 = Idioma.query.all()
            lista_De_Idioma = []
            for tec in consulta2:
                lista_De_Idioma.append((tec.pk_idioma, tec.Idioma))
            formulario.Idioma.choices = lista_De_Idioma

            return render_template('Administracion/cargarDocumento.html', form=formulario)

        else:
            flash('No es valida la cookie')
            return redirect(url_for('superUserGet_Login'))
    else:
        return redirect(url_for('superUserGet_Login'))


@app.route('/Administracion-CrearDocumento',methods=['POST'])
def Administracion_CrearDocumentoPost():

    if 'SessionSSU' in request.cookies:
        # compruebo que sea valida
        compruebo = CookieSuperSuperUser.query.filter_by(Valor_C = request.cookies.get('SessionSSU') ).first()
        if compruebo is not None:

            formulario_valido = True
            lista_de_elementos_a_comprobar = ['Nombre','Tecnologia','Version','Idioma']
            for i in lista_de_elementos_a_comprobar:
                if i not in request.form or request.form.get(i,'None') == 'None' :
                    formulario_valido = False

            if formulario_valido:

                #compruebo que idioma sea valida
                idiomas = Idioma.query.filter_by(pk_idioma=request.form.get('Idioma')).first()
                if idiomas is None:
                    flash('El idioma es incorrecto')
                    return redirect(url_for('Administracion_CrearDocumentoGet'))

                # compruebo que tecno sea valida
                tecnologia = TecnologiaM.query.filter_by(Pk_Tecnologia = request.form.get('Tecnologia')).first()
                if tecnologia is None:
                    flash('La tecnologia es incorrecta')
                    return redirect(url_for('Administracion_CrearDocumentoGet'))


                #compruebo que no ingrese unadocumentacion identica a una ya exsistente
                consulta = Documento.query.filter_by(   Documento_Nombre = request.form.get('Nombre'),
                                                        Documento_Tecnologia = request.form.get('Tecnologia'),
                                                        Documento_Version = request.form.get('Version'),
                                                        Documento_Idioma = request.form.get('Idioma') ).first()

                if consulta is None:

                    nueva_docu = Documento( Documento_Nombre = request.form.get('Nombre'),
                                            Documento_Tecnologia = request.form.get('Tecnologia'),
                                            Documento_Version = request.form.get('Version'),
                                            Documento_Idioma = request.form.get('Idioma') )

                    db.session.add(nueva_docu)
                    db.session.commit()

                    traigo = Documento.query.filter_by(
                                            Documento_Nombre = request.form.get('Nombre'),
                                            Documento_Tecnologia = request.form.get('Tecnologia'),
                                            Documento_Version = request.form.get('Version'),
                                            Documento_Idioma = request.form.get('Idioma')).first()

                    indiceDesabilitado = IndiceHabilitado( IndiceHabilitado_pk_de_documento = traigo.Documento_Pk )
                    db.session.add(indiceDesabilitado)
                    db.session.commit()

                    flash('Listo')
                    return redirect(url_for('Administracion_CrearDocumentoGet'))



                else:
                    flash('Ya exsiste esta documentacion tal cual.')
                    return redirect(url_for('Administracion_CrearDocumentoGet'))



            else:
                flash('El formulario no es valido')
                return redirect(url_for('Administracion_CrearDocumentoGet'))


        else:
            flash('No es valida la cookie')
            return redirect(url_for('superUserGet_Login'))
    else:
        return redirect(url_for('superUserGet_Login'))


@app.route('/Administracion-HabilitarDocumento',methods=['GET'])
def Administracion_HabilitarDocumentoGet():

    if 'SessionSSU' in request.cookies:
        #compruebo que sea valida
        compruebo = CookieSuperSuperUser.query.filter_by(Valor_C = request.cookies.get('SessionSSU') ).first()
        if compruebo is not None:
            formulario = HabilitarDocumentacion()
            lista_documentos = []
            consulta = Documento.query.filter_by(Documento_Habilitada = 'no' )
            for docu in consulta:
                texto = "Nombre: {} - - Version: {}".format(docu.Documento_Nombre, docu.Documento_Version)
                lista_documentos.append((docu.Documento_Pk,texto))

            formulario.Documento.choices = lista_documentos
            return render_template('Administracion/habilitarDocumento.html',form = formulario)

        else:
            flash('No es valida la cookie')
            return redirect(url_for('superUserGet_Login'))
    else:
        return redirect(url_for('superUserGet_Login'))


@app.route('/Administracion-HabilitarDocumento',methods=['POST'])
def Administracion_HabilitarDocumentoPost():

    if 'SessionSSU' in request.cookies:
        #compruebo que sea valida
        compruebo = CookieSuperSuperUser.query.filter_by(Valor_C = request.cookies.get('SessionSSU') ).first()
        if compruebo is not None:

            if 'Documento' in request.form:

                consulta = Documento.query.filter_by(Documento_Habilitada='no',Documento_Pk = request.form.get('Documento') ).first()
                if consulta is not None:

                    consulta.Documento_Habilitada = 'si'
                    db.session.commit()

                    flash('Lito')
                    return redirect(url_for('AdministracionGet'))

                else:
                    flash('Error inesperado')
                    return redirect(url_for('Administracion_HabilitarDocumentoGet'))


            else:
                flash('Error en el formularion')
                return redirect(url_for('Administracion_HabilitarDocumentoGet'))

        else:
            flash('No es valida la cookie')
            return redirect(url_for('superUserGet_Login'))
    else:
        return redirect(url_for('superUserGet_Login'))


@app.route('/Administracion-Indice',methods=['GET'])
def Administracion_IndiceGet():

    if 'SessionSSU' in request.cookies:
        #compruebo la cookie
        compruebo = CookieSuperSuperUser.query.filter_by(Valor_C = request.cookies.get('SessionSSU') ).first()
        if compruebo is not None:

            sql = """ select "Documento_Nombre", "Documento_Version", "Documento_Pk" from (select * from documento where "Documento_Habilitada" = 'no') as documento inner join (select * from indice_habilitado where "IndiceHabilitado_Habilitado" = 'no') as indices_habi on "Documento_Pk" = "IndiceHabilitado_pk_de_documento" """
            consulta_indices_no_habilitados = base_datos_conexion(sql).lista

            class pro():
                def __init__(self, elemento):
                    self.Documento_Nombre = elemento[0]
                    self.Documento_Version = elemento[1]
                    self.Documento_Pk = elemento[2]

            lista_documentos_con_indices_des = []
            for elementos in consulta_indices_no_habilitados:
                lista_documentos_con_indices_des.append(pro(elementos))

            return render_template('Administracion/Indices.html',info = lista_documentos_con_indices_des)

        else: # cookie SuperUser invalida
            flash('No es valida la cookie')
            return redirect(url_for('superUserGet_Login'))
    else: # no hay cookie
        return redirect(url_for('superUserGet_Login'))


@app.route('/Administracion-Indice/<int:pk_D>',methods=['GET'])
def Administracion_IndiceNumeroGet(pk_D):
    #compruebo meediante la cookie que quien este accediendo sea un SuperUser
    if 'SessionSSU' in request.cookies:
        #compruebo la cookie
        compruebo = CookieSuperSuperUser.query.filter_by(Valor_C = request.cookies.get('SessionSSU') ).first()
        if compruebo is not None:

            #compruevo pk de indice sea valida
            consulta = IndiceHabilitado.query.filter_by( IndiceHabilitado_pk_de_documento = pk_D).first()
            if consulta is not None:

                if consulta.IndiceHabilitado_Habilitado == 'no':

                    sql = """select "Indice_Nombre", "Indice_Numero" from indice where "Indice_pk_de_documento" = '{}' order by "Indice_Orden" """.format(pk_D)
                    datos_de_indice = base_datos_conexion(sql).lista

                    class ObjIndice():
                        def __init__(self, datos):
                            self.Indice_Nombre = datos[0]
                            self.Indice_Numero = datos[1]

                    lista_datos_de_indice = []

                    for dato in datos_de_indice:
                        lista_datos_de_indice.append(ObjIndice(datos=dato))
                        print(dato)

                    return render_template('Administracion/cargarSeccion.html',datos = lista_datos_de_indice,pkpk=pk_D )

                else:
                    return "No se pude mdificar este indice porque esta habilitado"
            else:
                return "Error"

        else: # cookie SuperUser invalida
            flash('No es valida la cookie')
            return redirect(url_for('superUserGet_Login'))
    else: # no hay cookie
        return redirect(url_for('superUserGet_Login'))


@app.route('/Administracion-CargarIndice',methods=['POST'])
def Administracion_IndicePost():

    #compruebo meediante la cookie que quien este accediendo sea un SuperUser
    if 'SessionSSU' in request.cookies:
        #compruebo la cookie
        compruebo = CookieSuperSuperUser.query.filter_by(Valor_C = request.cookies.get('SessionSSU') ).first()
        if compruebo is not None:

            if request.form.get('Nombre_tecnologia',''):
                tecno_valida = Documento.query.filter_by(Documento_Habilitada = 'no',Documento_Pk = request.form.get('Nombre_tecnologia','') ).first()
                if tecno_valida is not None:

                    IndiceM.query.filter_by( Indice_pk_de_documento = request.form.get('Nombre_tecnologia','') ).delete()

                    indice = 1
                    while 'indice['+str(indice)+']' in request.form:

                        nuevo_registro = IndiceM(   Indice_pk_de_documento = request.form.get('Nombre_tecnologia','') ,
                                                    Indice_Nombre = request.form.get( 'nombre['+str(indice)+']', '' ) ,
                                                    Indice_Numero  = request.form.get( 'indice['+str(indice)+']', '' ) ,
                                                    Indice_Orden = indice )

                        db.session.add(nuevo_registro)
                        db.session.commit()

                        indice = indice + 1

                    flash("Listo")
                    return redirect(url_for('Administracion_IndiceNumeroGet',pk_D=request.form.get('Nombre_tecnologia','')))

                else:
                    flash("El identificador de la tecnologia no es valido")
                    return redirect(url_for('Administracion_IndiceNumeroGet',pk_D=request.form.get('Nombre_tecnologia','')))

            else:
                flash("No ha seleccionado una tecnologia")
                return redirect(url_for('Administracion_IndiceNumeroGet',pk_D=request.form.get('Nombre_tecnologia','')))


        else: # cookie SuperUser invalida
            flash('No es valida la cookie')
            return redirect(url_for('superUserGet_Login'))
    else: # no hay cookie
        return redirect(url_for('superUserGet_Login'))


@app.route('/Administracion-HabilitarIndice',methods=['GET'])
def Administracion_HabilitarIndiceGet():

    if 'SessionSSU' in request.cookies:
        #compruebo que sea valida
        compruebo = CookieSuperSuperUser.query.filter_by(Valor_C = request.cookies.get('SessionSSU') ).first()
        if compruebo is not None:

            sql = """select "IndiceHabilitado_Pk", "Documento_Nombre", "Documento_Version" from (select * from indice_habilitado where "IndiceHabilitado_Habilitado" = 'no') as IndiceDes inner join indice on "IndiceHabilitado_pk_de_documento" = "Indice_pk_de_documento" inner join documento on "Documento_Pk" = "Indice_pk_de_documento" """
            resul = base_datos_conexion(sql).lista

            class sol7():
                def __init__(self, lista):
                    self.IndiceHabilitado_Pk = lista[0]
                    self.Documento_Nombre = lista[1]
                    self.Documento_Version = lista[2]

            lista = []
            for datos in resul:
                lista.append(sol7(datos))

            return render_template('Administracion/habilitarIndice.html',lista=lista)

        else:
            flash('No es valida la cookie')
            return redirect(url_for('superUserGet_Login'))
    else:
        return redirect(url_for('superUserGet_Login'))


@app.route('/Administracion-HabilitarIndice',methods=['POST'])
def Administracion_HabilitarIndicePost():
    if 'SessionSSU' in request.cookies:
        #compruebo que sea valida
        compruebo = CookieSuperSuperUser.query.filter_by(Valor_C = request.cookies.get('SessionSSU') ).first()
        if compruebo is not None:

            if request.form.get('indice'):

                infoPkdeIndiceDes = request.form.get('indice','')
                cambioEstado = IndiceHabilitado.query.filter_by(IndiceHabilitado_Pk = infoPkdeIndiceDes ).first()
                cambioEstado.IndiceHabilitado_Habilitado = 'si'
                db.session.commit()

            else:
                return 'Error'

            return redirect(url_for('AdministracionGet'))

        else:
            flash('No es valida la cookie')
            return redirect(url_for('superUserGet_Login'))
    else:
        return redirect(url_for('superUserGet_Login'))


@app.route('/Administracion-CrearContenido',methods=['GET'])
def Administracion_CrearContenidoGet():
    if 'SessionSSU' in request.cookies:
        #compruebo que sea valida
        compruebo = CookieSuperSuperUser.query.filter_by(Valor_C = request.cookies.get('SessionSSU') ).first()
        if compruebo is not None:

            sql = """ select "Documento_Nombre", "Documento_Version", "Indice_Nombre", "Indice_Numero", "Indice_Pk" from (select * from documento where "Documento_Habilitada"='no') as docu inner join (select * from indice_habilitado where "IndiceHabilitado_Habilitado" = 'si') as indi_habi on "Documento_Pk"="IndiceHabilitado_pk_de_documento" inner join Indice on "Documento_Pk"="Indice_pk_de_documento" order by "Documento_Nombre", "Documento_Version", "Indice_Orden" """
            consulta = base_datos_conexion(sql).lista

            class pro():
                def __init__(self, lista):
                    self.Documento_Nombre=lista[0]
                    self.Documento_Version=lista[1]
                    self.Indice_Nombre=lista[2]
                    self.Indice_Numero = lista[3]
                    self.Indice_Pk = lista[4]

            lista = []
            for datos in consulta:
                lista.append(pro(datos))

            return render_template("Administracion/ElejirIndice.html",lista=lista)

        else:
            flash('No es valida la cookie')
            return redirect(url_for('superUserGet_Login'))
    else:
        return redirect(url_for('superUserGet_Login'))   


@app.route('/Administracion-CrearContenido/<int:pk>',methods=['GET'])
def Administracion_CrearContenidoPkGet(pk):

    if 'SessionSSU' in request.cookies:
        #compruebo que sea valida
        compruebo = CookieSuperSuperUser.query.filter_by(Valor_C = request.cookies.get('SessionSSU') ).first()
        if compruebo is not None:

            consulta = IndiceM.query.filter_by(Indice_Pk=pk).first()
            if consulta is not None:

                consulta2 = IndiceHabilitado.query.filter_by(IndiceHabilitado_pk_de_documento = consulta.Indice_pk_de_documento ).first()

                if consulta2.IndiceHabilitado_Habilitado == 'si':

                    #consulta3 = Contenido.query.filter_by( Contenido_pk_de_articulo = pk ).first()
                    if True: #consulta3 is None:

                        lista_estilos = ['p','em','strong','h1','h2','h3','h4']

                        return render_template('Administracion/cargarContenido.html',pk=pk,estilos= lista_estilos)

                    else:
                        return "Este indice ya tiene contenido"


                else:
                    return "No esta habilitado"

            else:
                return 'Pk invalida'

        else:
            flash('No es valida la cookie')
            return redirect(url_for('superUserGet_Login'))
    else:
        return redirect(url_for('superUserGet_Login'))


@app.route('/Administracion-CrearContenido',methods=['POST'])
def Administracion_CrearContenidoPost():
    if 'SessionSSU' in request.cookies:
        #compruebo que sea valida
        compruebo = CookieSuperSuperUser.query.filter_by(Valor_C = request.cookies.get('SessionSSU') ).first()
        if compruebo is not None:

            consulta = IndiceM.query.filter_by(Indice_Pk = request.form.get("pk")).first()
            if consulta is not None:

                consulta2 = IndiceHabilitado.query.filter_by(IndiceHabilitado_pk_de_documento = consulta.Indice_pk_de_documento ).first()

                if consulta2.IndiceHabilitado_Habilitado == 'si':

                    consulta3 = Contenido.query.filter_by( Contenido_pk_de_articulo = request.form.get("pk") ).first()
                    if consulta3 is None:

                        #print(request.form.getlist('estilo[1]'))

                        ii = 1
                        while request.form.get('tipo['+str(ii)+']'):

                            if request.form.get('tipo['+str(ii)+']') == 'Texto':
                            
                                nuevoContenido = Contenido(
                                                        Contenido_pk_de_articulo = request.form.get("pk"),
                                                        Contenido_Contenido = request.form.get('contenido['+str(ii)+']'),
                                                        Contenido_Orden = ii,
                                                        Contenido_Html_Apertura = request.form.get('htmlAp['+str(ii)+']'),
                                                        Contenido_Html_Cierre = request.form.get('htmlCi['+str(ii)+']'),
                                                        Contenido_Asignable = request.form.get('asignable['+str(ii)+']')
                                                        )

                                db.session.add(nuevoContenido)
                                db.session.commit()

                            #contenido que no es texto
                            else:
                                
                                f = request.files['contenido['+str(ii)+']']

                                f.filename = 'hola.{0}'.format( f.mimetype.split('/')[1] )
                                f.save('C:/Users/Paulo/Desktop/MultiLang/static/vv/'+f.filename)

                                nuevoContenido = Contenido(
                                                        Contenido_pk_de_articulo = request.form.get("pk"),
                                                        Contenido_Contenido = str(f.filename),
                                                        Contenido_Orden = ii,
                                                        Contenido_Html_Apertura = request.form.get('htmlAp['+str(ii)+']'),
                                                        Contenido_Html_Cierre = request.form.get('htmlCi['+str(ii)+']'),
                                                        Contenido_Asignable = request.form.get('asignable['+str(ii)+']')
                                                        )

                                db.session.add(nuevoContenido)
                                db.session.commit()



                            ii = ii+1

                        return "Listo"

                    else:
                        return "Lo lamentamos este indice ya tiene contenido"

                else:
                    return "No esta habilitado"

            else:
                return 'Pk invalida'

        else:
            flash('No es valida la cookie')
            return redirect(url_for('superUserGet_Login'))
    else:
        return redirect(url_for('superUserGet_Login'))

#---------------------------------------------------------------------------------------------------------


@app.route('/Administracion-Login',methods=['GET'])
def Administracion_LoginGet():

    if 'SessionSU' in request.cookies:
        #compruebo que sea valida
        compruebo = CookieUsuario.query.filter_by(CookieUsuario_Valor_C = request.cookies.get('SessionSU') ).first()
        if compruebo is not None:
            flash('Ya estas logeado')
            return redirect(url_for('AdministracionGet'))
        else:
            formulario = AdministradoresLogin()
            return render_template('Administracion/AdminLogin.html', form=formulario)
    else:
        formulario = AdministradoresLogin()
        return render_template('Administracion/AdminLogin.html', form=formulario)

#agregar cuestiones de cookies
@app.route('/Administracion-Login',methods=['POST'])
def Administracion_LoginPost():

    formulario = AdministradoresLogin(request.form)

    if formulario.validate():

        # compruebo que existe el usuario
        existe = UsuarioSuperUser.query.filter_by(Usuario=formulario.Usuario.data).first()
        if existe is not None:
            # compruebo que existe el usuario y la llave
            existe2 = UsuarioSuperUser.query.filter_by(Usuario=formulario.Usuario.data,
                                                       Llave=formulario.Llave.data).first()
            if existe2 is not None:

                componente1 = "" + time.strftime("%H%M%S") + ""
                componente2 = "" + time.strftime("%S") + ""
                componente3 = "" + time.strftime("%M") + ""
                total = componente1 + componente2 + componente3
                valorDeCookie = (hashlib.md5(total.encode('utf-8')).hexdigest())

                nueva_cookie_en_db = CookieSuperUser(Valor_C=valorDeCookie, Pk_usuario=existe2.Pk_UsuarioSuperUser)
                db.session.add(nueva_cookie_en_db)
                db.session.commit()

                flash('Listo')
                respuesta = make_response(render_template('Administracion/administracion.html'))
                respuesta.set_cookie('SessionSU', valorDeCookie)

                return respuesta

            else:
                flash('La contraseña es incorrecta')
                return redirect(url_for('Administracion_LoginGet'))
        else:
            flash('No existe el usuario')
            return redirect(url_for('Administracion_LoginGet'))
    else:
        flash('Formulario no valido')
        return redirect(url_for('Administracion_LoginGet'))

@app.route('/Administracion',methods=['GET'])
def AdministracionGet():

    if 'SessionSU' in request.cookies:
        #compruebo que sea valida
        compruebo = CookieSuperUser.query.filter_by(Valor_C = request.cookies.get('SessionSU') ).first()
        if compruebo is not None:
            return render_template('Administracion/administracion.html')
        else:
            return redirect(url_for('Administracion_LoginGet'))
    else:
        return redirect(url_for('Administracion_LoginGet'))



#---------------------------------------------------------------------------------------------------------







if __name__ == '__main__':

    db.init_app(app)
    with app.app_context():
        db.create_all()

    app.run()
