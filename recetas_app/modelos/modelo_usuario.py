from recetas_app.config.mysqlconnection import MySQLConnection, connectToMySQL
from recetas_app.modelos.modelo_receta import Receta
from flask import flash
import re


EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]{3}$')

class Usuario:
    def __init__(self,id,first_name,last_name,email,password):
        self.id = id
        self.first_name=first_name
        self.last_name=last_name
        self.email=email
        self.password=password
    
    @classmethod
    def agregaUsuario( cls, nuevoUsuario ):
        query = "INSERT INTO usuario(first_name, last_name, email, password) VALUES(%(first_name)s, %(last_name)s, %(email)s, %(password)s);"
        resultado = connectToMySQL( "receta" ).query_db( query, nuevoUsuario )
        return resultado
    
    @classmethod
    def verificaUsuario( cls, usuario ):
        query = "SELECT * FROM usuario WHERE email = %(email)s;"
        resultado = connectToMySQL( "receta" ).query_db( query, usuario )
        if len( resultado ) > 0:
            usuarioResultado = Usuario(resultado[0]["id"], resultado[0]["first_name"], resultado[0]["last_name"], resultado[0]["email"], resultado[0]["password"] )
            return usuarioResultado
        else:
            return None
        
    @classmethod
    def listaRecetas(cls,usuario):
        query="SELECT* FROM usuario LEFT JOIN receta ON usuario.id=receta.id_usuario WHERE usuario.id= %(id)s;"
        resultado = connectToMySQL( "receta" ).query_db( query,usuario )
        listadeRecetas=[]
        for receta in resultado:
            receta = {
                "id" : receta["receta.id"],
                "name": receta["name"],
                "description": receta["description"],
                "instructions":receta["instructions"],
                "under_min":receta["under_min"],
                "date_made":receta["date_made"],
                "id_usuario":receta["id"]
            }
            listadeRecetas.append(Receta(receta["id"], receta["name"], receta["description"], receta["instructions"],
                                         receta["under_min"], receta["date_made"], receta["id_usuario"]))          
        return listadeRecetas

        
    @staticmethod
    def Validacion(nuevo):
        valida= True
        if len(nuevo['first_name']) <= 2:
            valida = False
            flash("El nombre debe tener mas de 3 caracteres","Registro")
        if len(nuevo['last_name']) <= 2:
            valida= False
            flash("El nombre debe tener mas de 3 caracteres","Registro")
        if len(nuevo['password'])<=0:
            valida= False
            flash("Agregar password","Registro")
        if not EMAIL_REGEX.match(nuevo['email']):
            flash("correo invalido,probar otra vez!!!","Registro")
            valida=False
        return valida
    
    