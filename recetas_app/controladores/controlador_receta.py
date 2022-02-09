from flask import Flask, render_template, request, redirect, session
from recetas_app import app
from recetas_app.modelos.modelo_receta import Receta

@app.route('/recipes/new' , methods=['GET'])
def paginaRegistor():
    return render_template("agregareceta.html")

@app.route('/registrar',methods=['POST'])
def añadirReceta():
    nuevaReceta = {
        "name" : request.form["name"],
        "description" : request.form["description"],
        "instructions" : request.form["instructions"],
        "under_min": request.form["under_min"],
        "date_made": request.form["date_made"],
        "id_usuario": session["id"]
    }   
    print("esto es date_made", nuevaReceta["under_min"])
    validar=Receta.Validacion(nuevaReceta)
    if validar == True :
        resultado=Receta.agregarReceta(nuevaReceta)
        return redirect('/dashboard')
    else:
        return redirect('/recipes/new')
    
@app.route( '/eliminar/<int:id>', methods=["POST"] )
def eliminarReceta( id ):
    eliminado= {
        "id" : id
    }
    resultado=Receta.eliminarReceta(eliminado)
    return redirect( '/dashboard' )

@app.route('/recipes/<int:id>', methods=['GET'])
def verReceta(id):
    obtenerReceta={
        "id": id
    }
    resultado=Receta.obtenerDatosReceta(obtenerReceta)
    print("ver usuario",resultado)
    return render_template( "show.html", receta=resultado[0] )

@app.route('/recipes/edit/<int:id>',methods=['GET'])
def editarReceta(id):
    receta_editar={
        "id": id
    }
    resultado=Receta.obtenerDatosReceta(receta_editar)
    return render_template ("editar.html", receta=resultado[0])
    
@app.route( '/edit/<int:id>', methods=["POST"] )
def cambiodeDatos( id ):
    RecetaEditar = {
        "id" : id,
        "name" : request.form["name"],
        "description" : request.form["description"],
        "instructions" : request.form["instructions"],
        "under_min": request.form["under_min"],
        "date_made": request.form["date_made"]
    }
    resultado=Receta.editarReceta(RecetaEditar)
    return redirect( '/dashboard' )