from recetas_app.modelos.modelo_usuario import Usuario
from recetas_app import app
from flask import render_template, request, redirect, session,flash
from flask_bcrypt import Bcrypt 

bcrypt=Bcrypt(app)

@app.route('/', methods=['GET'])
def despliegaPagina():
    return render_template( "inicio.html" )

@app.route('/dashboard',methods=['GET'])
def despliegaSesion():
    if 'id' in session:
        receta={
        "id":session["id"]
         }
        recetas=Usuario.listaRecetas(receta)
        return render_template( "plataforma.html",resto=recetas )
    else:
        return redirect( '/' )
    return render_template( "plataforma.html")
    
@app.route( '/registroUsuario', methods=["POST"] )
def registrarUsuario():
    nuevoUsuario = {
        "first_name" : request.form["first_name"],
        "last_name" : request.form["last_name"],
        "email" : request.form["email"],
        "password" : bcrypt.generate_password_hash(request.form["password"]),
    } 
    confirmacion= request.form["confirma_password"]
    validar=Usuario.Validacion(nuevoUsuario)
    if not validar:
        return redirect('/')
    else: 
        if not bcrypt.check_password_hash( nuevoUsuario["password"],confirmacion ):
            flash("password no coinciden","contraseña")
            return redirect('/')        
        else:
            resultado = Usuario.agregaUsuario(nuevoUsuario)
            session["first_name"] = request.form["first_name"]
            session["last_name"] = request.form["last_name"]
            return redirect( '/dashboard' )
        
@app.route( '/login', methods=["POST"] )
def loginUsuario():
    loginUsuario = request.form["loginUsuario"]
    passwordUsuario = request.form["passwordUsuario"]
    usuario = {
        "email" : loginUsuario,
    }
    resultado = Usuario.verificaUsuario(usuario)
    if resultado == None:
        flash( "El correo esta escrito incorrectamente", "login" )
        return redirect( '/' )
    else:
        if not bcrypt.check_password_hash( resultado.password,passwordUsuario):
            flash("password incorrecto","login")
            return redirect ('/')
        else:
            session["first_name"] = resultado.first_name
            session["last_name"] = resultado.last_name
            session["id"]=resultado.id
            return redirect( '/dashboard' )