from recetas_app.config.mysqlconnection import MySQLConnection, connectToMySQL
from flask import flash

class Receta:
    def __init__(self,id,name,description,instructions,under_min,date_made,id_usuario):
        self.id=id
        self.name=name
        self.description=description
        self.instructions=instructions
        self.under_min=under_min
        self.date_made=date_made
        self.id_usuario=id_usuario
        
    @classmethod
    def agregarReceta(cls,receta):
        query = "insert into receta(name,description,instructions,under_min,date_made,id_usuario) VALUES (%(name)s,%(description)s,%(instructions)s,%(under_min)s,%(date_made)s,%(id_usuario)s);"
        resultado = connectToMySQL("receta").query_db(query,receta)
        return resultado
    
    @classmethod
    def eliminarReceta(cls,receta):
        query = "DELETE FROM receta WHERE id= %(id)s;"
        resultado = connectToMySQL( "receta" ).query_db( query, receta )
        return resultado
    
    @classmethod
    def obtenerDatosReceta( cls, receta ):
        query = "SELECT * FROM receta WHERE id = %(id)s;"
        resultado = connectToMySQL( "receta" ).query_db( query, receta )
        return resultado
    
    @classmethod
    def editarReceta(cls,receta):
        query = "UPDATE receta SET name=%(name)s ,description=%(description)s,instructions=%(instructions)s,under_min=%(under_min)s,date_made=%(date_made)s WHERE id= %(id)s;"
        #print("Verificar si llega al metodo editarPelicula",query)
        resultado = connectToMySQL( "receta" ).query_db( query, receta )
        return resultado
    
    @staticmethod
    def Validacion(nuevo):
        valida= True
        print("esto es nuevo['under_min']",len(nuevo['under_min']))
        if len(nuevo['name']) <= 2:
            valida = False
            flash("El nombre debe tener mas de 3 caracteres","rece")
        if len(nuevo['description']) <= 2:
            valida= False
            flash("la descripción debe tener mas de 3 caracteres","rece")
        if len(nuevo['instructions']) <= 2:
            flash("Las instrucciopnes debe tener mas de 3 caracteres","rece")
            is_valid= False
        if len(nuevo['date_made']) <= 0:
            flash("llenar el casillero de la fecha","rece")
            is_valid= False
        return valida
    
    